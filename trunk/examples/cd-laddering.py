#!/usr/bin/env python

from zibopt import scip
import json
import sys

# TODO: verify that the output is correct
# TODO: write a post explaining this. 
# TODO: try without 1 and 2 pd CDs.  causes an LP solver error (?!?)

# Assumptions:
# 1. APYs stay the same from one period to the next
# 2. All investments are compounded monthly

class CD(object):
    '''Represents an option for CD investment'''
    def __init__(self, periods_per_year, periods, apy, min_invest):
        self.periods    = periods
        self.apy        = apy / 100.0
        self.min_invest = min_invest

        # We need the inverse of:
        # APY = (1 + periodic rate)^(# periods per year) - 1
        self.periodic_rate = (1 + self.apy)**(1.0/periods_per_year) - 1

    def __repr__(self):
        return '[%2d pd. | %.2f APY (%.4f%% pd) | %5d min]' % (
            self.periods,
            self.apy * 100,
            self.periodic_rate * 100,
            self.min_invest
        )

if __name__ == '__main__':
    # Make sure we are provided with a CD laddering data file
    try:
        data = json.load(open(sys.argv[1]))
    except IndexError:
        print('usage: %s data.json' % sys.argv[0])
        sys.exit()

    solver = scip.solver(quiet=False)

    # CD options: (months, APY, minimum investment)
    cd_options = [
        CD(data['periods per year'], *row)
        for row in data['cd options']
    ]

    # Construct variables saying whether or not to invest in each
    # CD each period, and how much we should invest per fund & period.
    investment_made  = []
    amount_to_invest = []
    for _ in range(data['total periods']):
        investment_made.append({
            cd:solver.variable(scip.BINARY)
            for cd in cd_options
        })        
        amount_to_invest.append({
            cd:solver.variable(upper=data['max investment'])
            for cd in cd_options
        })

    # Add constraints to guarantee minimum investment amounts
    for im, ai in zip(investment_made, amount_to_invest):
        for cd in cd_options:
            solver += ai[cd] - im[cd] * cd.min_invest >= 0
            solver += ai[cd] - im[cd] * data['max investment'] <= 0
    
    # Variables and constraints that tell how much expires at the end of
    # each month.  A 1-month CD expires the same month it is purchased.
    expirations_by_period = [[] for _ in range(data['total periods'])]
    for i in range(data['total periods']):
        for cd, invest_var in amount_to_invest[i].items():
            expires = i + cd.periods - 1

            # Ignore any that expire after the end of our model
            try:
                expirations_by_period[expires].append((cd, invest_var))
            except IndexError:
                pass
        
    expires = [solver.variable() for _ in range(data['total periods'])]
    for e, by_period in zip(expires, expirations_by_period):
        if by_period:
            solver += e - sum(
                (1 + cd.periodic_rate)**cd.periods * invest_var
                for cd, invest_var in by_period
            ) == 0

    # Add variables that describe how much uninvested cash we have
    # during each period (after making investments).
    cash_on_hand = [solver.variable() for _ in range(data['total periods'])]

    for i in range(data['total periods']):
        if not i:
            solver += cash_on_hand[i] \
                + sum(amount_to_invest[i].values()) == data['initial cash']
        else:
            solver += cash_on_hand[i] \
                - cash_on_hand[i-1] \
                - expires[i-1] \
                + sum(amount_to_invest[i].values()) == 0

    # Constraints for cash_on_hand + current expirations >= something
    for e, c in zip(expires, cash_on_hand):
        solver += e + c >= data['min available']

    # Maximize ending cash on hand + final expirations
    solution = solver.maximize(
        objective=cash_on_hand[-1] + expires[-1],
        gap=0.01
    )
    
    if solution:
        for i in range(data['total periods']):
            print('=' * 80)
            print('[period %d]' % i)
            print('cash on hand:         % 10.2f' % solution[cash_on_hand[i]])
            print('investments made:     % 10.2f' % sum(
                solution[x] for x in amount_to_invest[i].values()
            ))
            print('investments expiring: % 10.2f' % solution[expires[i]])

            if [im for im in investment_made[i].values() if solution[im] > 0]:
                print('investment plan:')
                for cd, im in investment_made[i].items():
                    if solution[im] > 0:
                        print('  cd: %s   amount: % 10.2f' % (
                            cd, 
                            solution[amount_to_invest[i][cd]]
                        ))

            print()

        print('=' * 80)
        print('initial cash:   % 10.2f' % data['initial cash'])
        print('final cash:     % 10.2f' % solution.objective)

        gain = solution.objective - data['initial cash']
        print('amount gained:  % 10.2f' % gain)

        overall_apy = 100 * ((solution.objective / data['initial cash']) ** \
            (float(data['periods per year']) / data['total periods']) - 1)
        print('overall apy:   % 10.4f%%' % overall_apy)

        periodic_rate = 100 * ((solution.objective / data['initial cash']) ** \
            (1.0 / data['total periods']) - 1)
        print('periodic rate: % 10.4f%%' % periodic_rate) 

        print('=' * 80)

    else:
        print('infeasible')


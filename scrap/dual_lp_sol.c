#include <scip/scip.h>

void main() {
    SCIP *scip;
    SCIPcreate(&scip);
    
    // Build an LP:
    //   max  x
    //   s.t. x <= 1 
    //        x >= 0
    SCIP_Real obj[1] = {1.0};
    SCIP_Real lb[1] = {0.0};
    SCIP_Real ub[1] = {SCIPinfinity(scip)};
    SCIP_Real lhs[1] = {-SCIPinfinity(scip)};
    SCIP_Real rhs[1] = {1.0};
    const int beg[1] = {0};
    const int ind[1] = {0};
    const SCIP_Real val[1] = {1.0};

    SCIP_LPI *lpi;
    SCIPlpiCreate(&lpi, "test lpi", SCIP_OBJSENSE_MAXIMIZE);
    SCIPlpiLoadColLP(
        lpi, 
        SCIP_OBJSENSE_MAXIMIZE,
        1,    // ncols
        obj,
        lb,
        ub,
        NULL, // colnames
        1,    // nrows
        lhs,
        rhs,
        NULL, // rownames
        1,    // nnonz
        beg,
        ind,
        val
    );
    
    // Tell simplex about the known optimal basis.
    int cstat[1] = {1};
    int rstat[1] = {2};
    SCIPlpiSetBase(lpi, cstat, rstat);
    
    // This will make the LP solver think it's found an optimal solution
    // without actually performing any pivots.
    SCIPlpiSetIntpar(lpi, SCIP_LPPAR_LPITLIM, 0);
    SCIPlpiSolvePrimal(lpi);

    // Get out dual value for our single constraint.
    SCIP_Real duals[1] = {0};
    SCIPlpiGetSol(lpi, NULL, NULL, duals, NULL, NULL);
    printf("dual price: %.2f\n", duals[0]);
}

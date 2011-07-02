#include <scip/scip.h>

void main() {
    // Init solver and create problem
    SCIP *scip;
    SCIPcreate(&scip);
    SCIPincludeDefaultPlugins(scip);
    SCIPcreateProb(scip, "dual lop sol", NULL, NULL, NULL, NULL, NULL, NULL, NULL);

    // Turn off presolving
    SCIPsetPresolving(scip, SCIP_PARAMSETTING_OFF, TRUE);
    
    // Create a single continuous variable with lower bound 0
    // and objective coefficient 1
    SCIP_VAR *variable;
    SCIPcreateVar(scip, &variable, NULL, 0, SCIPinfinity(scip), 1, 
        SCIP_VARTYPE_CONTINUOUS, TRUE, FALSE, NULL, NULL, NULL, NULL, NULL);
    SCIPaddVar(scip, variable);

    // Create a single constraint: 0 <= variable <= 1
    SCIP_CONS *constraint;
    SCIP_VAR *vars[1] = {variable};
    SCIP_Real coef[1] = {1.0};
    SCIPcreateConsLinear(scip, &constraint, "dual lp sol constraint", 
        1, vars, coef, -SCIPinfinity(scip), 1.0, 
        TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE);
    SCIPaddCons(scip, constraint);

    // Solve the LP
    SCIPsetObjsense(scip, SCIP_OBJSENSE_MAXIMIZE);
    SCIPsolve(scip);

    // Get dual price for the constraint
    SCIP_CONS *transformed;
    SCIPgetTransformedCons(scip, constraint, &transformed);
    if (transformed == NULL) {
        puts("could not get transformed constraint");
    } else {
        SCIP_Real dual = SCIPgetDualsolLinear(scip, transformed);
        printf("dual price = %.2f\n", dual);
    }
}

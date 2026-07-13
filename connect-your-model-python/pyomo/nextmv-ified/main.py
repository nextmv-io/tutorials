#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2015-2025
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________


#!/usr/bin/env python
# -*- coding: utf-8 -*-


import nextmv

# Import
from pyomo.environ import *

# Duration parameter for the solver.
SUPPORTED_PROVIDER_DURATIONS = {
    "cbc": "sec",
    "glpk": "tmlim",
    "scip": "limits/time",
}

# Creation of a Concrete Model
model = ConcreteModel()

nextmv.redirect_stdout()
input = nextmv.load()
options = input.options

## Define sets ##
#  Sets
#       i   canning plants   / seattle, san-diego /
#       j   markets          / new-york, chicago, topeka / ;
sets = input.data["sets"]
model.i = Set(initialize=sets["i"], doc="Canning plants")
model.j = Set(initialize=sets["j"], doc="Markets")

## Define parameters ##
#   Parameters
#       a(i)  capacity of plant i in cases
#         /    seattle     350
#              san-diego   600  /
#       b(j)  demand at market j in cases
#         /    new-york    325
#              chicago     300
#              topeka      275  / ;
params = input.data["parameters"]
model.a = Param(
    model.i,
    initialize=params["a"],
    doc="Capacity of plant i in cases",
)
model.b = Param(
    model.j,
    initialize=params["b"],
    doc="Demand at market j in cases",
)
#  Table d(i,j)  distance in thousands of miles
#                    new-york       chicago      topeka
#      seattle          2.5           1.7          1.8
#      san-diego        2.5           1.8          1.4  ;
dtab = {(edge["from"], edge["to"]): edge["cost"] for edge in params["d"]}
model.d = Param(model.i, model.j, initialize=dtab, doc="Distance in thousands of miles")
#  Scalar f  freight in dollars per case per thousand miles  /90/ ;
model.f = Param(
    initialize=params["f"], doc="Freight in dollars per case per thousand miles"
)


#  Parameter c(i,j)  transport cost in thousands of dollars per case ;
#            c(i,j) = f * d(i,j) / 1000 ;
def c_init(model, i, j):
    return model.f * model.d[i, j] / 1000


model.c = Param(
    model.i,
    model.j,
    initialize=c_init,
    doc="Transport cost in thousands of dollar per case",
)

## Define variables ##
#  Variables
#       x(i,j)  shipment quantities in cases
#       z       total transportation costs in thousands of dollars ;
#  Positive Variable x ;
model.x = Var(model.i, model.j, bounds=(0.0, None), doc="Shipment quantities in case")


## Define constraints ##
# supply(i)   observe supply limit at plant i
# supply(i) .. sum (j, x(i,j)) =l= a(i)
def supply_rule(model, i):
    return sum(model.x[i, j] for j in model.j) <= model.a[i]


model.supply = Constraint(
    model.i, rule=supply_rule, doc="Observe supply limit at plant i"
)


# demand(j)   satisfy demand at market j ;
# demand(j) .. sum(i, x(i,j)) =g= b(j);
def demand_rule(model, j):
    return sum(model.x[i, j] for i in model.i) >= model.b[j]


model.demand = Constraint(model.j, rule=demand_rule, doc="Satisfy demand at market j")


## Define Objective and solve ##
#  cost        define objective function
#  cost ..        z  =e=  sum((i,j), c(i,j)*x(i,j)) ;
#  Model transport /all/ ;
#  Solve transport using lp minimizing z ;
def objective_rule(model):
    return sum(model.c[i, j] * model.x[i, j] for i in model.i for j in model.j)


model.objective = Objective(
    rule=objective_rule, sense=minimize, doc="Define objective function"
)


## Display of the output ##
# Display x.l, x.m ;
def pyomo_postprocess(options=None, instance=None, results=None):
    model.x.display()


# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python transport.py
if __name__ == "__main__":
    # This emulates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory

    opt = SolverFactory(options.solver)
    opt.options[SUPPORTED_PROVIDER_DURATIONS[options.solver]] = options.duration
    results = opt.solve(model)
    # sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + "-" * 60)
    pyomo_postprocess(None, model, results)

    shipments = [
        {"from": ix[0], "to": ix[1], "quantity": x()}
        for ix, x in model.x.items()
        if x() > 0.01
    ]
    solution = {"shipments": shipments}
    metrics = {
        "duration": results.solver.time,
        "value": value(model.objective, exception=False),
        "variables": model.nvariables(),
        "constraints": model.nconstraints(),
        "num_edges_used": len(shipments),
    }
    nextmv.write(solution=solution, metrics=metrics)

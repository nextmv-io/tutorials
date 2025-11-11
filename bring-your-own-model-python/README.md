# Bring your own model - Python

Code for the bring your own model (Python) tutorial. There are two examples:

* [Pyomo](./pyomo/): [Transport problem authored by Pyomo][pyomo-example].
* [HiGHS](./highs/): [Shortest path network flow authored by HiGHS][highs-example].

For each of the examples, you will find two directories:

* `original`: the original example without any modifications.
* `nextmv-ified`: the example converted into a Nextmv Application.

Go into each directory for instructions about running the decision model.

[pyomo-example]: https://github.com/Pyomo/pyomo-gallery/blob/main/transport/transport.py
[highs-example]: https://github.com/ERGO-Code/HiGHS/blob/master/examples/network_flow.py

# Connect your model - CLI

Code for the connect your model (CLI) tutorial. There are three examples:

* [HiGHS](./highs/): [Simple LP problem authored by HiGHS in
  C++][highs-example]. Uses C++.
* [OR-Tools](./ortools/): [Vehicle Routing Problem with Pickups and Deliveries
  authored by OR-Tools in Java][ortools-example]. Uses Java.
* [Xpress](./xpress/): [Sudoku authored by FICO® Xpress][xpress-example]. Uses Python.

For each of the examples, you will find two directories:

* `original`: the original example without any modifications.
* `nextmv-ified`: the example converted into a Nextmv application.

Go into each directory for instructions about running the decision model.

[ortools-example]: https://developers.google.com/optimization/routing/pickup_delivery#complete_programs
[highs-example]: https://github.com/ERGO-Code/HiGHS/blob/master/examples/call_highs_from_cpp.cpp
[xpress-example]: https://www.fico.com/fico-xpress-optimization/docs/latest/solver/optimizer/python/HTML/chExamples.html

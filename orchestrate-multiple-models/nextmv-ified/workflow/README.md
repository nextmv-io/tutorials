# Avocado price optimization - Workflow model

This is the code for the workflow of the [Avocado price optimization
example authored by Gurobi][gurobi-example]. This workflow orchestrates the
regression and decision models.

* Install requirements.

  ```bash
  pip install -r requirements.txt
  ```

* Export your Nextmv Cloud API key, as it is required.

  ```bash
  export NEXTMV_API_KEY="<YOUR_NEXTMV_API_KEY>"
  ```

* Run the example.

  ```bash
  cat input.json | python main.py
  ```

[gurobi-example]: https://www.gurobi.com/jupyter_models/avocado-price-optimization/

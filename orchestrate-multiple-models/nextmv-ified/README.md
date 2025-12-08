# Orchestrate multiple models - Nextmv-ified

This is the code for the [Avocado price optimization example authored by
Gurobi][gurobi-example] turned into multiple Nextmv applications.

There are three applications:

1. [`workflow`](./workflow/): decision workflow orchestrating multiple models.
2. [`regression`](./regression/): regression model predicting avocado sales.
3. [`decision`](./decision/): decision model optimizing avocado prices and supply.

Each directory contains a `README.md` with instructions on how to run the
application locally. Run the following scripts to see how to orchestrate the
multiple models using Nextmv.

* Run the scripts individually.

  * `app1.sh`: Create the `regression` Nextmv Cloud application.

    ```bash
    bash app1.sh
    ```

  * `app2.sh`: Create the `decision` Nextmv Cloud application.

    ```bash
    bash app2.sh
    ```

  * `app3.sh`: Push the local executable code of the `regression` model to a
    Nextmv Cloud application.

    ```bash
    bash app3.sh
    ```

  * `app4.sh`: Push the local executable code of the `decision` model to a
    Nextmv Cloud application.

    ```bash
    bash app4.sh
    ```

  * `app5.sh`: Create the `workflow` Nextmv Cloud application.

    ```bash
    bash app5.sh
    ```

  * `app6.sh`: Push the local executable code of the `workflow` model to a
    Nextmv Cloud application.

    ```bash
    bash app6.sh
    ```

  * `app7.sh`: Run the `workflow` Nextmv Cloud application remotely.

    ```bash
    bash app7.sh
    ```

[gurobi-example]: https://www.gurobi.com/jupyter_models/avocado-price-optimization/

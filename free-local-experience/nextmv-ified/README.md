# OR-Tools vehicle routing problem with capacity constraints - Nextmv-ified

This is the code for the [Vehicle routing problem with capacity
constraints by OR-Tools][or-tools-example] turned into a Nextmv application.

* Sync the project.

  ```bash
  uv sync
  ```

* Run the example.

  ```bash
  cat inputs/input.json | uv run main.py
  ```

* Run the scripts individually.

  * `app1.sh`: runs the Nextmv application locally, printing run IDs.

    ```bash
    ./app1.sh
    ```

  * `app2.sh`: gets the results of the local Nextmv application runs.

    ```bash
    ./app2.sh
    ```

  * `app3.sh`: gets the information of the local Nextmv application runs.

    ```bash
    ./app3.sh
    ```

  * `app4.sh`: runs the Nextmv application locally, polling for results.

    ```bash
    ./app4.sh
    ```

  * `app5.sh`: runs the Nextmv application locally, polling for results and
    visualizing them.

    ```bash
    ./app5.sh
    ```

[or-tools-example]: https://developers.google.com/optimization/routing/cvrp

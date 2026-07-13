# Pyomo transport problem - Nextmv-ified

This is the code for the [Transport problem authored by
Pyomo][pyomo-example] turned into a Nextmv application.

* Sync the project.

  ```bash
  uv sync
  ```

* Run the example.

  ```bash
  cat inputs/problem.json | uv run main.py
  ```

* Run the scripts individually.

  * `app1.py`: runs the Nextmv application locally, sleeping and waiting for
      results.

    ```bash
    uv run app1.py
    ```

  * `app2.py`: runs the Nextmv application locally, polling for results.

    ```bash
    uv run app2.py
    ```

  * Export your Nextmv Cloud API key for convenience, as it is required in the upcoming
    scripts.

    ```bash
    export NEXTMV_API_KEY="<YOUR_NEXTMV_API_KEY>"
    ```

  * `app3.py`: creates a new Nextmv Cloud application. Requires a valid Nextmv
    Cloud API key.

    ```bash
    uv run app3.py
    ```

  * `app4.py`: syncs the local application runs to a Nextmv Cloud
    application.

    ```bash
    uv run app4.py
    ```

  * `app5.py`: pushes the local executable code to a Nextmv Cloud application.

    ```bash
    uv run app5.py
    ```

  * `app6.py`: runs the Nextmv Cloud application, polling for results.

    ```bash
    uv run app6.py
    ```

  * `app7.py`: creates an input set from the last runs.

    ```bash
    uv run app7.py
    ```

  * `app8.py`: creates a scenario test using the input set.

    ```bash
    uv run app8.py
    ```

[pyomo-example]: https://github.com/Pyomo/pyomo-gallery/blob/main/transport/transport.py

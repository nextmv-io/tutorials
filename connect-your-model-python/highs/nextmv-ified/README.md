# HiGHS shortest path network flow - Nextmv-ified

This is the code for the [Shortest path network flow authored by
HiGHS][highs-example] turned into a Nextmv application.

* Install requirements.

  ```bash
  pip install -r requirements.txt
  ```

* Run the example.

  ```bash
  python main.py
  ```

* Run the scripts individually.

  * `app1.py`: runs the Nextmv application locally, sleeping and waiting for
      results.

    ```bash
    python app1.py
    ```

  * `app2.py`: runs the Nextmv application locally, polling for results.

    ```bash
    python app2.py
    ```

  * Export your Nextmv Cloud API key for convenience, as it is required in the upcoming
    scripts.

    ```bash
    export NEXTMV_API_KEY="<YOUR_NEXTMV_API_KEY>"
    ```

  * `app3.py`: creates a new Nextmv Cloud application. Requires a valid Nextmv
    Cloud API key.

    ```bash
    python app3.py
    ```

  * `app4.py`: syncs the local application runs to a Nextmv Cloud
    application.

    ```bash
    python app4.py
    ```

  * `app5.py`: pushes the local executable code to a Nextmv Cloud application.

    ```bash
    python app5.py
    ```

  * `app6.py`: runs the Nextmv Cloud application, polling for results.

    ```bash
    python app6.py
    ```

  * `app7.py`: creates an input set from the last runs.

    ```bash
    python app7.py
    ```

  * `app8.py`: creates a scenario test using the input set.

    ```bash
    python app8.py
    ```

[highs-example]: https://github.com/ERGO-Code/HiGHS/blob/master/examples/network_flow.py

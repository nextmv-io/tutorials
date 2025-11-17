# HiGHS shortest path network flow - Nextmv-ified

This is the code for the [Shortest path network flow authored by
HiGHS][highs-example] turned into a Nextmv Application.

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

  * `app3.py`: syncs the local application runs to a Nextmv Cloud
    application. Requires a valid Nextmv Cloud API key.

    ```bash
    export NEXTMV_API_KEY="<YOUR_NEXTMV_API_KEY>"
    python app3.py
    ```

  * `app4.py`: pushes the local executable code to a Nextmv Cloud Application.
    Requires a valid Nextmv Cloud API key.

    ```bash
    export NEXTMV_API_KEY="<YOUR_NEXTMV_API_KEY>"
    python app4.py
    ```

[highs-example]: https://github.com/ERGO-Code/HiGHS/blob/master/examples/network_flow.py

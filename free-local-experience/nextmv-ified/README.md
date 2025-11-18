# OR-Tools vehicle routing problem with capacity constraints - Nextmv-ified

This is the code for the [Vehicle routing problem with capacity
constraints by OR-Tools][or-tools-example] turned into a Nextmv Application.

* Install requirements.

```bash
pip install -r requirements.txt
```

* Run the example.

```bash
python main.py -input inputs/input.json
```

* Run the scripts individually.

  * `app1.py`: runs the Nextmv Application locally, printing run IDs.

    ```bash
    python app1.py
    ```

  * `app2.py`: gets the results of the local Nextmv Application runs.

    ```bash
    python app2.py
    ```

  * `app3.py`: gets the metadata of the local Nextmv Application runs.

    ```bash
    python app3.py
    ```

  * `app4.py`: runs the Nextmv Application locally, polling for results.

    ```bash
    python app4.py
    ```

  * `app5.py`: runs the Nextmv Application locally, polling for results and
    visualizing them.

    ```bash
    python app5.py
    ```

[or-tools-example]: https://developers.google.com/optimization/routing/cvrp

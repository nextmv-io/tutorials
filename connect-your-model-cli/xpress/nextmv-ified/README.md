# Xpress sudoku - Nextmv-ified

This is the code for the [Sudoku authored by FICO® Xpress][xpress-example]
turned into a Nextmv application.

* Sync the project.

    ```bash
    uv sync
    ```

* Run the example.

    ```bash
    uv run main.py
    ```

* Run the scripts individually.

  * `app1.sh`: Create a Nextmv Cloud application.

    ```bash
    bash app1.sh
    ```

  * `app2.sh`: Push the local executable code to a Nextmv Cloud application.

    ```bash
    bash app2.sh
    ```

  * `app3.sh`: Run the Nextmv Cloud application.

    ```bash
    bash app3.sh
    ```

  * `app4.sh`: Create an input set.

    ```bash
    bash app4.sh
    ```

  * `app5.sh`: Create a scenario test.

    ```bash
    bash app5.sh
    ```

[xpress-example]: https://www.fico.com/fico-xpress-optimization/docs/latest/solver/optimizer/python/HTML/chExamples.html

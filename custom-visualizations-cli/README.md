# Custom visualizations - CLI

Code for the custom visualizations (CLI) tutorial. The following [community
app][community-apps] is used:

* [Python HiGHS Knapsack][python-highs-knapsack-comm-app]: use the HiGHS solver
  to solve a knapsack problem defined in JSON format.

You will find two directories:

* `original`: the original example without any modifications.
* `visualization`: the example modified to include visuals.

* Run the scripts individually.

  * `app1.sh`: Clones the `python-highs-knapsack` community app twice, once in
    the `original` directory and once in the `visualization` directory.

    ```bash
    bash app1.sh
    ```

  * `app2.sh`: Creates a local run. Use this command in both the `original` and
    `visualization` dirs.

    ```bash
    bash app2.sh
    ```

  * `app3.sh`: Visualizes the local run. Use this command in the
    `visualization` dir.

    ```bash
    bash app3.sh
    ```

  * `app4.sh`: Creates a Nextmv Cloud application. This command must be run
    from the `visualization` directory.

    ```bash
    bash app4.sh
    ```

  * `app5.sh`: Push the app to Nextmv Cloud. This command must be run from the
    `visualization` directory.

    ```bash
    bash app5.sh
    ```

  * `app6.sh`: Creates a remote run in Nextmv Cloud. This command must be run
    from the `visualization` directory.

    ```bash
    bash app6.sh
    ```

[community-apps]: https://github.com/nextmv-io/community-apps
[python-highs-knapsack-comm-app]: https://github.com/nextmv-io/community-apps/tree/develop/python-highs-knapsack

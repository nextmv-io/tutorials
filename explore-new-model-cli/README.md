# Explore new model - CLI

Code for the explore new model (CLI) tutorial. The following [community
app][community-apps] is used:

* [Python HiGHS Knapsack][python-highs-knapsack-comm-app]: use the HiGHS solver
  to solve a knapsack problem defined in JSON format.

Go into the [`python-highs-knapsack`](./python-highs-knapsack/) directory for
instructions on how to run the app itself.

* Run the scripts individually.

  * `app1.sh`: List available community apps.

    ```bash
    bash app1.sh
    ```

  * `app2.sh`: Clone the `python-highs-knapsack` community app locally.

    ```bash
    bash app2.sh
    ```

  * `app3.sh`: Create a Nextmv Cloud application.

    ```bash
    bash app3.sh
    ```

  * `app4.sh`: Push the local executable code to a Nextmv Cloud application.
    This command must be run from the `python-highs-knapsack` directory.

    ```bash
    bash app4.sh
    ```

  * `app5.sh`: Run the Nextmv Cloud application. This command must be run from
    the `python-highs-knapsack` directory.

    ```bash
    bash app5.sh
    ```

  * `app6.sh`: Create an input set.

    ```bash
    bash app6.sh
    ```

[community-apps]: https://github.com/nextmv-io/community-apps
[python-highs-knapsack-comm-app]: https://github.com/nextmv-io/community-apps/tree/develop/python-highs-knapsack

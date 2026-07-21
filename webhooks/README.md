# Webhooks

Code for the webhooks tutorial. The following [community
app][community-apps] is used:

* [Python Hello World][python-hello-world-comm-app]: a simple Python Hello
  World app.

Go into the [`python-hello-world`](./python-hello-world/) directory for
instructions on how to run the app itself.

* Set up the FastAPI server locally to receive webhooks:

  ```bash
  uv run fastapi dev --port 8000
  ```

* Run the scripts individually.

  * `app1.sh`: Clone the `python-hello-world` community app locally.

    ```bash
    bash app1.sh
    ```

  * `app2.sh`: Create a Nextmv Cloud application.

    ```bash
    bash app2.sh
    ```

  * `app3.sh`: Push the local executable code to a Nextmv Cloud application.

    ```bash
    bash app3.sh
    ```

  * `app4.sh`: Run the Nextmv Cloud application.

    ```bash
    bash app4.sh
    ```

[community-apps]: https://github.com/nextmv-io/community-apps
[python-hello-world-comm-app]: https://github.com/nextmv-io/community-apps/tree/develop/python-hello-world

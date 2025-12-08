# OR-Tools Vehicle Routing Problem with Pickups and Deliveries in Java - Nextmv-ified

This is the code for the [Vehicle Routing Problem with Pickups and
Deliveries authored by OR-Tools][ortools-example] turned into a Nextmv Application.

* Compile the code with Maven:

    ```bash
    mvn clean package
    ```

* Run the code with `java -jar`:

    ```bash
    java -jar main.jar
    ```

* Run the scripts individually.

  * `app1.sh`: Create a Nextmv Cloud Application.

    ```bash
    bash app1.sh
    ```

  * `app2.sh`: Push the local executable code to a Nextmv Cloud Application.

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

[ortools-example]: https://developers.google.com/optimization/routing/pickup_delivery#complete_programs

# HiGHS simple LP problem in C++ - Nextmv-ified

This is the code for the [Simple LP problem authored by
HiGHS][highs-example] turned into a Nextmv application.

* Build the HiGHS solver itself. You only need to do this once.

  * Clone HiGHS from GitHub.

      ```bash
      git clone https://github.com/ERGO-Code/HiGHS.git
      ```

  * Build HiGHS.

      ```bash
      cd HiGHS
      cmake -S. -B build 
      cmake --build build --parallel
      cd ..
      ```

* Get the `nlohmann/json` header-only library.

    ```bash
    mkdir -p nlohmann
    curl -L https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp \
      -o nlohmann/json.hpp
    ```

* Compile the example. The following command uses `g++` to compile.

    ```bash
    g++ -std=c++11 main.cpp -o main \
      -I. \
      -I./HiGHS/highs \
      -I./HiGHS/build \
      -L./HiGHS/build/lib -lhighs
    ```

* Run the example. The problem is streamed from `stdin`.

  * MacOS:

    ```bash
    cat inputs/problem.json | DYLD_LIBRARY_PATH=./HiGHS/build/lib ./main
    ```

  * Linux:

    ```bash
    cat inputs/problem.json | LD_LIBRARY_PATH=./HiGHS/build/lib ./main
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

  * `app3.sh`: Create a secrets collection to set the env var.

    ```bash
    bash app3.sh
    ```

  * `app4.sh`: Run the Nextmv Cloud application.

    ```bash
    bash app4.sh
    ```

  * `app5.sh`: Create an input set.

    ```bash
    bash app5.sh
    ```

  * `app6.sh`: Update the `latest` instance with the secrets collection.

    ```bash
    bash app6.sh
    ```

  * `app7.sh`: Create a scenario test.

    ```bash
    bash app7.sh
    ```

[highs-example]: https://github.com/ERGO-Code/HiGHS/blob/master/examples/call_highs_from_cpp.cpp

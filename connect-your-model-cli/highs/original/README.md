# HiGHS simple LP problem in C++ - original

This is the original code for the [Simple LP problem authored by
HiGHS][highs-example].

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

* Compile the example. The following command uses `g++` to compile.

    ```bash
    g++ -std=c++11 main.cpp -o main \
        -I./HiGHS/highs \
        -I./HiGHS/build \
        -L./HiGHS/build/lib -lhighs
    ```

* Run the example.

  * MacOS:

    ```bash
    DYLD_LIBRARY_PATH=./HiGHS/build/lib ./main
    ```

  * Linux:

    ```bash
    LD_LIBRARY_PATH=./HiGHS/build/lib ./main
    ```

[highs-example]: https://github.com/ERGO-Code/HiGHS/blob/master/examples/call_highs_from_cpp.cpp

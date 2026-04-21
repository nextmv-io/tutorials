# CI/CD with GitHub Actions

Code for the CI/CD with GitHub Actions tutorial, using the
[`setup-nextmv`][setup-nextmv] GitHub Action.

* Run the scripts individually.

  * `app1.sh`: Clone the `python-nextroute` community app.

      ```bash
      bash app1.sh
      ```

  * `app2.sh`: Create a new Nextmv Cloud app.

      ```bash
      bash app2.sh
      ```

  * `app3.sh`: Push the app to Nextmv Cloud.

      ```bash
      bash ../app3.sh
      ```

  * `app4.sh`: Create a new version of the app.

      ```bash
      bash app4.sh
      ```

  * `app5.sh`: Create `production` and `staging` instances of the app.

      ```bash
      bash app5.sh
      ```

  * `app6.sh`: Execute a remote run on the `staging` instance.

      ```bash
      bash app6.sh
      ```

  * `app7.sh`: Create an input set based on the `staging` instance and the latest
    runs.

      ```bash
      bash app7.sh
      ```

  * `app8.sh`: Create an acceptance test comparing the `production` and `staging`
    instances, using the input set created in the previous step.

      ```bash
      bash app8.sh
      ```

* Create the `.github/workflows/nextmv.yml` GitHub Actions workflow file at the
  root of the repo, and add the content found in [the corresponding file of
  this repo][nextmv-ci-cd].

[setup-nextmv]: https://github.com/nextmv-io/setup-nextmv
[nextmv-ci-cd]: /.github/workflows/nextmv.yml

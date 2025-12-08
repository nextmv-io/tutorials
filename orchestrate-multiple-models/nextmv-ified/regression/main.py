import nextmv
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split


def fit(input: nextmv.Input) -> nextmv.Output:
    options = input.options
    avocado = input.data["avocado"]

    # Add the index for each year from 2015 through 2022
    avocado["date"] = pd.to_datetime(avocado["date"])
    avocado["year"] = pd.DatetimeIndex(avocado["date"]).year
    avocado["year_index"] = avocado["year"] - input.data["input"]["initial_year"]
    avocado = avocado.sort_values(by="date")

    # Define the peak season
    avocado["month"] = pd.DatetimeIndex(avocado["date"]).month
    pm = input.data["input"]["peak_months"]
    peak_months = range(pm[0], pm[1])  # <--------- Set the months for the "peak season"

    def peak_season(row):
        return 1 if int(row["month"]) in peak_months else 0

    avocado["peak"] = avocado.apply(lambda row: peak_season(row), axis=1)

    # Scale the number of avocados to millions
    avocado["units_sold"] = avocado["units_sold"] / 1_000_000

    # Select only conventional avocados
    avocado = avocado[avocado["type"] == "Conventional"]

    avocado = avocado[
        ["date", "units_sold", "price", "region", "year", "month", "year_index", "peak"]
    ].reset_index(drop=True)

    regions = input.data["input"]["regions"]
    df = avocado[avocado.region.isin(regions)]

    # Split the data for training and testing
    train, test = train_test_split(
        df, train_size=options.train_size, random_state=options.random_state
    )
    df_train = pd.DataFrame(train, columns=df.columns)
    df_test = pd.DataFrame(test, columns=df.columns)

    # Train the model
    formula = "units_sold ~ price + year_index + C(region)+ peak"
    mod = smf.ols(formula, data=df_train)
    result = mod.fit()

    # Get R^2 from test data
    y_true = df_test["units_sold"]
    y_pred = result.predict(df_test)
    r2_test = r2_score(y_true, y_pred)
    print("The R^2 value in the test set is", r2_test)

    formula = "units_sold ~ price + year_index + C(region)+ peak"
    mod_full = smf.ols(formula, data=df)
    result_full = mod_full.fit()

    y_true_full = df["units_sold"]
    y_pred_full = result_full.predict(df)
    r2_full = r2_score(y_true_full, y_pred_full)
    print("The R^2 value in the full dataset is", r2_full)

    # Get the weights and store it
    coef_dict = result_full.params.to_dict()
    coef_dict["C(region)[T.Great_Lakes]"] = 0

    return nextmv.Output(
        output_format=nextmv.OutputFormat.MULTI_FILE,
        options=options,
        solution_files=[nextmv.json_solution_file("coefficients.json", data=coef_dict)],
        statistics=nextmv.Statistics(
            result=nextmv.ResultStatistics(
                custom={
                    "r2_test": r2_test,
                    "r2_full": r2_full,
                },
            ),
        ),
    )


if __name__ == "__main__":
    manifest = nextmv.Manifest.from_yaml(".")
    options = manifest.extract_options()

    def loader(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

    input = nextmv.load(
        input_format=nextmv.InputFormat.MULTI_FILE,
        options=options,
        path="inputs",
        data_files=[
            nextmv.json_data_file(name="input", input_data_key="input"),
            nextmv.DataFile(
                name="avocado.csv",
                loader=loader,
                input_data_key="avocado",
            ),
        ],
    )
    output = fit(input)
    nextmv.write(output=output, path="outputs")

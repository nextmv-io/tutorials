import gurobipy as gp
import nextmv
import pandas as pd
from gurobipy import GRB


def solve(input: nextmv.Input) -> nextmv.Output:
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

    m = gp.Model("Avocado_Price_Allocation")

    # Sets and parameters
    R = regions  # set of all regions

    B = input.data["input"]["B"]  # total amount ot avocado supply

    # 1 if it is the peak season; 1 if isn't
    peak_or_not = input.data["input"]["peak_or_not"]
    year = input.data["input"]["year"]

    c_waste = input.data["input"]["cost_waste"]  # the cost ($) of wasting an avocado
    c_transport = input.data["input"]["cost_transport"]
    # the cost of transporting an avocado

    # Get the lower and upper bounds from the dataset for the price and the number of products to be stocked
    # minimum avocado price in each region
    a_min = {r: input.data["input"]["a_min"] for r in R}
    # maximum avocado price in each region
    a_max = {r: input.data["input"]["a_max"] for r in R}
    b_min = dict(
        df.groupby("region")["units_sold"].min()
    )  # minimum number of avocados allocated to each region
    b_max = dict(
        df.groupby("region")["units_sold"].max()
    )  # maximum number of avocados allocated to each region

    p = m.addVars(R, name="p", lb=a_min, ub=a_max)  # price of avocados in each region
    x = m.addVars(R, name="x", lb=b_min, ub=b_max)  # quantity supplied to each region
    s = m.addVars(
        R, name="s", lb=0
    )  # predicted amount of sales in each region for the given price
    w = m.addVars(R, name="w", lb=0)  # excess wasteage in each region

    coef_dict = input.data["coefficients"]
    d = {
        r: (
            coef_dict["Intercept"]
            + coef_dict["price"] * p[r]
            + coef_dict["C(region)[T.%s]" % r]
            + coef_dict["year_index"] * (year - 2015)
            + coef_dict["peak"] * peak_or_not
        )
        for r in R
    }
    for r in R:
        print(d[r])

    m.setObjective(sum(p[r] * s[r] - c_waste * w[r] - c_transport[r] * x[r] for r in R))
    m.ModelSense = GRB.MAXIMIZE

    m.addConstr(sum(x[r] for r in R) == B)
    m.update()

    m.addConstrs((s[r] <= x[r] for r in R))
    m.addConstrs((s[r] <= d[r] for r in R))
    m.update()

    m.addConstrs((w[r] == x[r] - s[r] for r in R))
    m.update()

    m.Params.NonConvex = 2
    m.optimize()

    solution = pd.DataFrame()
    solution["Region"] = R
    solution["Price"] = [p[r].X for r in R]
    solution["Allocated"] = [round(x[r].X, 8) for r in R]
    solution["Sold"] = [round(s[r].X, 8) for r in R]
    solution["Wasted"] = [round(w[r].X, 8) for r in R]
    solution["Pred_demand"] = [
        (
            coef_dict["Intercept"]
            + coef_dict["price"] * p[r].X
            + coef_dict["C(region)[T.%s]" % r]
            + coef_dict["year_index"] * (year - 2015)
            + coef_dict["peak"] * peak_or_not
        )
        for r in R
    ]

    opt_revenue = m.ObjVal
    print("\n The optimal net revenue: $%f million" % opt_revenue)
    solution

    return nextmv.Output(
        output_format=nextmv.OutputFormat.MULTI_FILE,
        options=options,
        solution_files=[
            nextmv.json_solution_file(
                name="solution.json",
                data={"solution": solution.to_dict(orient="records")},
            )
        ],
        statistics=nextmv.Statistics(
            result=nextmv.ResultStatistics(
                value=opt_revenue,
                duration=m.Runtime,
                custom={
                    "status": m.Status,
                    "variables": m.NumVars,
                    "constraints": m.NumConstrs,
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
            nextmv.json_data_file(name="coefficients", input_data_key="coefficients"),
            nextmv.json_data_file(name="input", input_data_key="input"),
            nextmv.DataFile(
                name="avocado.csv",
                loader=loader,
                input_data_key="avocado",
            ),
        ],
    )
    output = solve(input)
    nextmv.write(output=output, path="outputs")

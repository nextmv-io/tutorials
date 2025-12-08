import warnings

import gurobipy as gp
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from gurobipy import GRB
from ipywidgets import interact
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

avocado = pd.read_csv(
    "https://raw.githubusercontent.com/Gurobi/modeling-examples/master/price_optimization/HABdata_2019_2022.csv"
)  # dataset downloaded directly from HAB
# avocado = pd.read_csv('HABdata_2019_2022.csv') # dataset downloaded directly from HAB
avocado_old = pd.read_csv(
    "https://raw.githubusercontent.com/Gurobi/modeling-examples/master/price_optimization/kaggledata_till2018.csv"
)  # dataset downloaded from Kaggle
# avocado_old = pd.read_csv('kaggledata_till2018.csv') # dataset downloaded from Kaggle
avocado = pd.concat([avocado, avocado_old], ignore_index=True)
avocado

# Add the index for each year from 2015 through 2022
avocado["date"] = pd.to_datetime(avocado["date"])
avocado["year"] = pd.DatetimeIndex(avocado["date"]).year
avocado["year_index"] = avocado["year"] - 2015
avocado = avocado.sort_values(by="date")

# Define the peak season
avocado["month"] = pd.DatetimeIndex(avocado["date"]).month
peak_months = range(2, 8)  # <--------- Set the months for the "peak season"


def peak_season(row):
    return 1 if int(row["month"]) in peak_months else 0


avocado["peak"] = avocado.apply(lambda row: peak_season(row), axis=1)

# Scale the number of avocados to millions
avocado["units_sold"] = avocado["units_sold"] / 1000000

# Select only conventional avocados
avocado = avocado[avocado["type"] == "Conventional"]

avocado = avocado[
    ["date", "units_sold", "price", "region", "year", "month", "year_index", "peak"]
].reset_index(drop=True)

avocado

df_Total_US = avocado[avocado["region"] == "Total_US"]

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))

mean = df_Total_US.groupby("year")["units_sold"].mean()
std = df_Total_US.groupby("year")["units_sold"].std()
axes.errorbar(mean.index, mean, xerr=0.5, yerr=2 * std, linestyle="")
axes.set_ylabel("Units Sold (millions)")
axes.set_xlabel("Year")

fig.tight_layout()

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))

mean = df_Total_US.groupby("month")["units_sold"].mean()
std = df_Total_US.groupby("month")["units_sold"].std()

axes.errorbar(mean.index, mean, xerr=0.5, yerr=2 * std, linestyle="")
axes.set_ylabel("Units Sold (millions)")
axes.set_xlabel("Month")

fig.tight_layout()

plt.xlabel("Month")
axes.set_xticks(range(1, 13))
plt.ylabel("Units sold (millions)")
plt.show()

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))
sns.heatmap(
    df_Total_US[["units_sold", "price", "year", "peak"]].corr(),
    annot=True,
    center=0,
    ax=axes,
)

axes.set_title("Correlations for conventional avocados")
plt.show()

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 5))

regions = [
    "Great_Lakes",
    "Midsouth",
    "Northeast",
    "Northern_New_England",
    "SouthCentral",
    "Southeast",
    "West",
    "Plains",
]
df = avocado[avocado.region.isin(regions)]

mean = df.groupby("region")["units_sold"].mean()
std = df.groupby("region")["units_sold"].std()

axes.errorbar(range(len(mean)), mean, xerr=0.5, yerr=2 * std, linestyle="")

fig.tight_layout()

plt.xlabel("Region")
plt.xticks(range(len(mean)), pd.DataFrame(mean)["units_sold"].index, rotation=20)
plt.ylabel("Units sold (millions)")
plt.show()


# Split the data for training and testing
train, test = train_test_split(df, train_size=0.8, random_state=1)
df_train = pd.DataFrame(train, columns=df.columns)
df_test = pd.DataFrame(test, columns=df.columns)

# Train the model
formula = "units_sold ~ price + year_index + C(region)+ peak"
mod = smf.ols(formula, data=df_train)
result = mod.fit()
result.summary()

# Get R^2 from test data
y_true = df_test["units_sold"]
y_pred = result.predict(df_test)
print("The R^2 value in the test set is", r2_score(y_true, y_pred))

formula = "units_sold ~ price + year_index + C(region)+ peak"
mod_full = smf.ols(formula, data=df)
result_full = mod_full.fit()

y_true_full = df["units_sold"]
y_pred_full = result_full.predict(df)
print("The R^2 value in the full dataset is", r2_score(y_true_full, y_pred_full))

# Get the weights and store it
coef_dict = result_full.params.to_dict()
coef_dict["C(region)[T.Great_Lakes]"] = 0
print(coef_dict)

m = gp.Model("Avocado_Price_Allocation")

# Sets and parameters
R = regions  # set of all regions

B = 30  # total amount ot avocado supply

peak_or_not = 1  # 1 if it is the peak season; 1 if isn't
year = 2022

c_waste = 0.1  # the cost ($) of wasting an avocado
c_transport = {
    "Great_Lakes": 0.3,
    "Midsouth": 0.1,
    "Northeast": 0.4,
    "Northern_New_England": 0.5,
    "SouthCentral": 0.3,
    "Southeast": 0.2,
    "West": 0.2,
    "Plains": 0.2,
}
# the cost of transporting an avocado

# Get the lower and upper bounds from the dataset for the price and the number of products to be stocked
a_min = {r: 0 for r in R}  # minimum avocado price in each region
a_max = {r: 2 for r in R}  # maximum avocado price in each region
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

fig, ax = plt.subplots(1, 1)
plot_sol = sns.scatterplot(data=solution, x="Price", y="Sold", hue="Region", s=100)
plot_waste = sns.scatterplot(
    data=solution, x="Price", y="Wasted", marker="x", hue="Region", s=100, legend=False
)

plot_sol.legend(loc="center left", bbox_to_anchor=(1.25, 0.5), ncol=1)
plot_waste.legend(loc="center left", bbox_to_anchor=(1.25, 0.5), ncol=1)
plt.ylim(0, 5)
plt.xlim(1, 2.2)
ax.set_xlabel("Price per avocado ($)")
ax.set_ylabel("Number of avocados sold (millions)")
plt.show()
print(
    "The circles represent sales quantity and the cross markers represent the wasted quantity."
)


peak_or_not = 1  #
year = 2021

# Sets and parameters
R = regions
c_waste = 0.1
c_transport = {
    "Great_Lakes": 0.3,
    "Midsouth": 0.1,
    "Northeast": 0.4,
    "Northern_New_England": 0.5,
    "SouthCentral": 0.3,
    "Southeast": 0.2,
    "West": 0.2,
    "Plains": 0.2,
}

# Get the lower and upper bounds for price (p) and amount to be stocked (x) from the dataset
price_min = dict(df.groupby("region")["price"].min())
price_max = dict(df.groupby("region")["price"].max())
sold_min = dict(df.groupby("region")["units_sold"].min())
sold_max = dict(df.groupby("region")["units_sold"].max())


def solve_MIQP(x):
    B = x

    # Initialize Model
    m = gp.Model("Avocado_Price_Allocation")

    # Variables. Adjust the bounds here
    x = m.addVars(R, name="x", lb=sold_min, ub=sold_max)
    p = m.addVars(R, name="p", lb=0, ub=2)
    s = m.addVars(R, name="s", lb=0)
    w = m.addVars(R, name="w", lb=0)
    _ = m.addVars(R, name="i", vtype=GRB.BINARY)

    # Predictor expression for demand
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

    # Set the objective
    m.ModelSense = GRB.MAXIMIZE
    m.setObjective(sum(p[r] * s[r] - c_waste * w[r] - c_transport[r] * x[r] for r in R))

    # Add the constraints
    m.addConstrs((s[r] <= x[r] for r in R))
    m.addConstrs((s[r] <= d[r] for r in R))
    m.addConstrs((x[r] == w[r] + s[r] for r in R))
    m.addConstr(sum(x[r] for r in R) == B)

    # Solve
    m.setParam("OutputFlag", 0)
    m.Params.NonConvex = 2
    m.update()
    m.optimize()
    if m.status == 4:
        print("The problem is infeasible. Try changing the parameter values.")
    else:
        global solution, opt_revenue
        solution = pd.DataFrame()
        solution["Region"] = R
        solution["Price"] = [p[r].X for r in R]
        solution["Allocated"] = [round(x[r].X, 8) for r in R]
        solution["Sold"] = [round(s[r].X, 8) for r in R]
        solution["Wasted"] = [round(w[r].X, 8) for r in R]
        solution["Demand"] = [
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
        if display_figures:
            print("\n Net revenue: $%f million" % opt_revenue)
            print(
                "\nThe optimal solution is as follows. Price per avocado in dollars. Allocated avocados, wasted avocados, and predicted demand in millions.\n"
            )
            print(solution)

            print(
                "\n Scatter plot of price vs number of avocados sold (millions) for the eight regions:"
            )
            fig, ax = plt.subplots(1, 1)
            plot_sol = sns.scatterplot(
                data=solution, x="Price", y="Sold", hue="Region", s=100
            )
            plot_waste = sns.scatterplot(
                data=solution,
                x="Price",
                y="Wasted",
                marker="x",
                hue="Region",
                s=100,
                legend=False,
            )

            plot_sol.legend(loc="center left", bbox_to_anchor=(1.25, 0.5), ncol=1)
            plot_waste.legend(loc="center left", bbox_to_anchor=(1.25, 0.5), ncol=1)
            plt.ylim(0, 5)
            plt.xlim(1, 2.2)
            ax.set_xlabel("Price per avocado ($)")
            ax.set_ylabel("Number of avocados sold (millions)")
            plt.show()
            print(
                "The circles represent sales quantity and the cross markers represent the wasted quantity."
            )

        return m.ObjVal, solution


display_figures = 1
print("Select a value for the available inventory (B) (in millions):\n")
interact(solve_MIQP, x=(15, 40, 1))


df_subset = df[(df["year"] == year) & (df["peak"] == peak_or_not)]
df_subset["price_minus_transport"] = df_subset["price"] - df_subset["region"].map(
    c_transport
)
dates = sorted(list(set(df_subset.date)))

# Run the optimizer for each week
actual, optimal, display_figures = [], [], 0
for date in dates:
    df_date = df_subset[df_subset["date"] == date]
    weekly_sold = (df_date["units_sold"]).values.sum()
    optimal.append(solve_MIQP(weekly_sold)[0])

    actual_weekly_revenue = (
        df_date["units_sold"] * (df_date["price_minus_transport"])
    ).values.sum()
    actual.append(actual_weekly_revenue)

# Plot the two scatter plots
fig_comparison, ax_comparison = plt.subplots(1, 1)
actual_plot = plt.scatter(dates, actual)
optimal_plot = plt.scatter(dates, optimal)
plt.legend(
    (optimal_plot, actual_plot),
    ("Optimal weekly net revenue", "Actual weekly net revenue"),
    loc="center left",
    bbox_to_anchor=(1.25, 0.5),
    ncol=1,
)
x_ticks_labels = list(dict.fromkeys([date.strftime("%B") for date in dates]))
ax_comparison.set_xticklabels(x_ticks_labels, rotation=20, fontsize=12)
ax_comparison.set_xlabel("Date")
ax_comparison.set_ylabel("Net revenue in $million")

plt.show()

difference = [(i - j) / j for i, j in zip(optimal, actual)]
print(
    "For the average peak season week in %i, the optimal solution yields %f %% more net revenue than the actual supply chain."
    % (year, 100 * sum(difference) / len(difference))
)


def compare_with_actual(x):
    df_date = df_subset[df_subset["date"] == x]
    weekly_sold = (df_date["units_sold"]).values.sum()
    print(weekly_sold)
    opt_revenue, opt_solution = solve_MIQP(weekly_sold)
    df_comparison = df_date.merge(opt_solution, left_on="region", right_on="Region")
    df_comparison = df_comparison[["Region", "price", "Price", "units_sold", "Sold"]]
    df_comparison = df_comparison.rename(
        {
            "price": "Actual price",
            "Price": "Optimal price",
            "units_sold": "Actual sold",
            "Sold": "Optimal sold",
        },
        axis=1,
    )
    print(df_comparison.sort_values(by="Region").reset_index(drop=True))


display_figures = 0
print("Select a value for the available inventory (B) (in millions):\n")
interact(compare_with_actual, x=dates)

gp.disposeDefaultEnv()

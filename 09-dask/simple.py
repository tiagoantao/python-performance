import numpy as np
import dask.dataframe as dd

taxes = dd.read_csv("FY2016-STC-Category-Table.csv", sep="\t")
taxes["Amount"] = taxes["Amount"].str.replace(",", "").replace("X", np.nan).astype(float)
taxes["Tax_Type"] = taxes["Tax_Type"].astype("category").cat.as_known()  # XXX
pivot = taxes.pivot_table(index="Geo_Name", columns="Tax_Type", values="Amount")
has_property_info = pivot[~pivot["Property Taxes"].isna()].index

pivot_clean = pivot.loc[has_property_info]
frac_property = pivot_clean["Property Taxes"] / pivot_clean["Total Taxes"]

print(frac_property)
frac_property.visualize(filename="09-property.svg", rankdir="LR")#, collapse_output=True)

frac_property_result = frac_property.compute()






frac_property.sort_values()
frac_property.compute().sort_values()


pivot_clean["frac_property"] = pivot_clean["Property Taxes"] / pivot_clean["Total Taxes"]

no_property_states = taxes[taxes["Amount"] == "X"].Geo_Name
has_property_info = taxes[
    (taxes["Tax_Type"] == "Property Taxes") &
    (taxes["Amount"] != "X")][["Geo_Name"]]

taxes_clean = taxes.join(
    has_property_info.set_index("Geo_Name"),
    on="Geo_Name",
    how="inner"
)

taxes.pivot


taxes_clean
tc.pivot()
no_property_states
tc = taxes.compute()
pivot = tc.pivot(index="Geo_Name", columns="Tax_Type", values="Amount")
pivot.loc["Texas"]
taxes.head()
type(taxes)
type(tc)
taxes
taxes.iloc[:,0].compute()
taxes_clean.visualize(filename="x.svg")
list(no_property_states)

no_property_states


taxes_clean.Geo_Name.unique().compute()

taxes_clean = taxes[~taxes.Geo_Name.isin(no_property_states)]
taxes_clean = taxes[~taxes.Geo_Name.isin(list(no_property_states))]

pivot

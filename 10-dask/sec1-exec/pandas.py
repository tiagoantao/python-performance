import numpy as np
import pandas as pd

taxes = pd.read_csv("FY2016-STC-Category-Table.csv", sep="\t")
taxes["Amount"] = taxes["Amount"].str.replace(",", "").replace("X", np.nan).astype(float)
pivot = taxes.pivot_table(index="Geo_Name", columns="Tax_Type", values="Amount")
has_property_info = pivot[pivot["Property Taxes"].notna()].index
pivot
pivot_clean = pivot.loc[has_property_info]
frac_property = pivot_clean["Property Taxes"] / pivot_clean["Total Taxes"]
frac_property.sort_values()

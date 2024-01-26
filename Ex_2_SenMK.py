import pandas as pd
import pymannkendall as mk

df = pd.read_excel(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\pm25df.xlsx")
df["slope"]=0
df["p_value"]=0
for i in range(len(df)):
    result = mk.original_test(df[list(range(2010,2021))].iloc[i])
    print(result)
    df["slope"].iloc[i] = result.slope
    df[ "p_value"].iloc[i] = result.p

df.export_csv("SenMK.csv")
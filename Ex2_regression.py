import statsmodels.api as sm
import pandas as pd
from dbfread import DBF

# Step 2: Load the Data
pmdf=pd.read_csv(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\pm25df.csv",index_col="PAC")
metelist=['DEWP',  'MXSPD','PRCP', 'TEMP', 'VISIB', 'WDSP']
df_list=[]
for mete in metelist:
    for year in range(2000,2021):
        print(year,mete)
        Kriging_df = pd.DataFrame(iter(DBF(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\kri_zonal_table\kri_table_%d%s.dbf" % (year,mete))))
        # Kriging_df = Kriging_df.set_index("PAC")
        Kriging_df=Kriging_df[["PAC","MEAN"]]
        Kriging_df=Kriging_df.rename(columns={"MEAN" : "%d%s" % (year,mete)})
        df_list.append(Kriging_df)
# df = pd.concat(df_list)
df=df_list[0]
for df_ in df_list[1:]:
    df = pd.merge(df,df_,on="PAC")

print(df.head())

df=df.set_index("PAC")
df = df.T
df['year'] = df.index.str[:4].astype(int)
df['mete']= df.index.str[4:]
pvaluelist , prelist = [],[]
for pac in df.columns[:-2]:
    print(pac)
    pac_df = df[[pac,'year','mete']]
    groups = pac_df.groupby("mete")
    gr_list = []
    for mete,group in groups:


        group=group.rename(columns={pac:mete})
        group.index = list(range(2000,2021))
        gr_list.append(group[mete])
        print(group.head(2))
    pac_df_all = pd.concat(gr_list, axis=1)
    pm_se = pmdf.loc[pac].T
    pm_se.index = pm_se.index.astype(int)
    pac_df_all["PM"] = pm_se

    """Least Squares in Python"""
    # define response variable
    y = pac_df_all['PM']

    # define predictor variables
    x = pac_df_all.iloc[:,:6]

    # add constant to predictor variables
    x = sm.add_constant(x)

    # fit linear regression model
    model = sm.OLS(y, x).fit()

    # view model summary
    print(model.summary())
    ols_df= pd.concat([model.params,model.pvalues],axis=1)
    ols_df.columns=[str(pac)+'params',str(pac)+'pvalue']
    pvaluelist.append(ols_df)

ols_out_df = pd.concat(pvaluelist,axis=1)
pvalue_df = ols_out_df[[str(c)+'pvalue' for c in df.columns[:-2]]]
param_df = ols_out_df[[str(c)+'params' for c in df.columns[:-2]]]

param_df.columns = df.columns[:-2]
pvalue_df.columns = df.columns[:-2]

tested_df = (param_df * (pvalue_df<0.05)).T

tested_df["factor"] = tested_df.abs().idxmax(axis=1)
tested_df.to_csv(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\\OLSR.csv")




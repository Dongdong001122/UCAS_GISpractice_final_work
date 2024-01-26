import esda
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import libpysal as lps
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from pylab import figure, scatter, show
# %matplotlib inline

gdf = gpd.read_file(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\Shandong_PM2.5_1998_2020.shp")

gdf.columns.values
gdf.head(1) #
alphabetlist =  [chr(i) for i in range(97,123)]

i=0
for c in ["F"+str(x) for x in range(1999,2021)]:
    ax=gdf.plot(figsize=(8,8),column=c)
    ax.set_axis_off()
    ax.title("("+alphabetlist[i]+") "+c[1:])

    ax.savefig(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\\"+c+".png")
    show()


import pandas as pd
from pykrige.ok import OrdinaryKriging
import numpy as np
import plotnine
from plotnine import *
import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
# import cmaps
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from shapely.geometry import Point

# read raw data
sh = gpd.read_file('G:\geodata\SpatialAnalysisUCAS\Output\Ex2\Shandong_province.shp')
station_meta = pd.read_csv(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\stations.csv")
raw_df= pd.read_csv(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\3569455.csv")
raw_df["DATE"] = pd.to_datetime(raw_df["DATE"])
raw_df["year"]=raw_df["DATE"].dt.year
# calculate annual meteorological data
metelist=['DEWP', 'FRSHTT', 'GUST', 'MAX', 'MIN', 'MXSPD','PRCP', 'SLP', 'SNDP', 'STP', 'TEMP', 'VISIB', 'WDSP']
metedict = dict(zip(metelist, ["mean"]*len(metelist)))
ann_df = raw_df.groupby(['STATION', 'year']).agg(metedict)

# Krigging
annual_groups = ann_df.groupby(['year'])
for year,group in annual_groups:
    print(year)
    group = group.merge(station_meta[['STATION_ID', 'LATITUDE', 'LONGITUDE']], left_on='STATION',
                          right_on='STATION_ID')

    # # Lon and Lat
    # grid_lon = np.linspace(144.5, 123, 1300)
    # grid_lat = np.linspace(34, 38.5, 1300)
    #
    # lons,lats,metedata = group['LONGITUDE'], group['LATITUDE'],group['DEWP']
    # OK = OrdinaryKriging(lons, lats, metedata, variogram_model='gaussian', nlags=6)
    # z1, ss1 = OK.execute('grid', grid_lon, grid_lat)
    # z1.shape
    #
    # # 转换成网格
    # xgrid, ygrid = np.meshgrid(grid_lon, grid_lat)
    # # 将插值网格数据整理
    # df_grid = pd.DataFrame(dict(long=xgrid.flatten(), lat=ygrid.flatten()))
    # # 添加插值结果
    # df_grid["Krig_gaussian"] = z1.flatten()

    geometry = [Point(xy) for xy in zip(group['LONGITUDE'], group['LATITUDE'])]
    gdf = gpd.GeoDataFrame(group, geometry=geometry, crs='EPSG:4326')
    gdf = gdf.to_file("G:\geodata\SpatialAnalysisUCAS\Output\Ex2\mete"+str(year)+".shp")

# arcpy.Tmp.BatchKriging1(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\mete2021.shp", "DEWP;FRSHTT;GUST;MAX;MIN;MXSPD;PRCP;SLP;SNDP;STP;TEMP;VISIB", r"C:\Users\dell\AppData\Local\Temp\ArcGISProTemp19700\7cbe12d6-f4ec-4fc2-ac01-08878d148db4\Default.gdb\Kriging_OutSurfaceRaster_%Name%", r"C:\Users\dell\AppData\Local\Temp\ArcGISProTemp19700\7cbe12d6-f4ec-4fc2-ac01-08878d148db4\Default.gdb\Kriging_OutVariancePredictionRaster_%Name%", "Spherical # # # #", 0.013722744, "VARIABLE 12")
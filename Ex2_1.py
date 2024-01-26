import pandas as pd
import os
from shapely.geometry import Point
import geopandas as gpd
file_list = os.listdir('G:\BaiduNetdiskDownload\\1998-2020县级PM2.5年度均值')
for file in file_list:
    year = int(file[3:7])
    print(year)
    if year == 1998:
        pm25df= pd.read_excel('G:\BaiduNetdiskDownload\\1998-2020县级PM2.5年度均值\\'+file , index_col="PAC")
        pm25df = pm25df.rename(columns={"MEAN":year})
    else:
        pm25df1= pd.read_excel('G:\BaiduNetdiskDownload\\1998-2020县级PM2.5年度均值\\'+file , index_col="PAC")
        pm25df[year]=pm25df1["MEAN"]

# # Step 2: Create a geometry column using the Point constructor from Shapely
# geometry = [Point(lon, lat) for lon, lat in zip(pm25df['Lon'], pm25df['Lat'])]
# # Step 3: Create a GeoDataFrame
# gdf = gpd.GeoDataFrame(pm25df, geometry=geometry, crs='EPSG:4326')
# 
# #load shandong province shapefile
# sd_gdf= gpd.read_file("G:\geodata\SpatialAnalysisUCAS\Output\Ex2\Shandong_province.shp")
# sd_PM25_gdf = gpd.overlay(sd_gdf, gdf, how='intersection')
# 
# sd_PM25_gdf.export("G:\geodata\SpatialAnalysisUCAS\Output\Ex2\sd_PM25_gdf.shp")
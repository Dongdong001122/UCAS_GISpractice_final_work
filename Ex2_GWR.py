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

for c in ["F2010","F2015","F2020"]:
    ax=gdf.plot(figsize=(8,8),column=c)
    ax.set_axis_off()
    show()

    df = gdf
    wq =  lps.weights.Queen.from_dataframe(df)# 使用Quuen式邻接矩阵
    wq.transform = 'r' # 标准化矩阵

    centroids = gdf.geometry.centroid # 计算多边形几何中心
    fig = figure(figsize=(8,14))

    plt.plot(np.array(centroids.x), np.array(centroids.y),'.')
    for k,neighs in wq.neighbors.items():
        print(k,neighs)
        origin = centroids[k]
        for neigh in neighs:
            segment = centroids[[k,neigh]]
            plt.plot(np.array(segment.x), np.array(segment.y),'-')
    plt.title('Queen Neighbor Graph')
    plt.axis('off')
    plt.show()

    wr =  lps.weights.Rook.from_dataframe(df) # 使用Rook式邻接矩阵
    # wr.transform = 'r' # 标准化矩阵
    fig = figure(figsize=(8,8))


    plt.plot(np.array(centroids.x), np.array(centroids.y),'.')
    for k,neighs in wq.neighbors.items():
        print(k,neighs)
        origin = centroids[k]
        for neigh in neighs:
            segment = centroids[[k,neigh]]
            plt.plot(np.array(segment.x), np.array(segment.y),'-')
    plt.title('Rook Neighbor Graph')
    plt.axis('off')
    plt.show()

    wr =  lps.weights.Rook.from_dataframe(df) # 使用Rook式邻接矩阵
    # wr.transform = 'r' # 标准化矩阵
    fig = figure(figsize=(16,8))

    # Calculate Moran's Index
    y=gdf[c]
    mi = esda.moran.Moran(y, wq)

    print("Moran's I 值为：",mi.I)
    print("随机分布假设下Z检验值为：",mi.z_rand)
    print("随机分布假设下Z检验的P值为：",mi.p_rand)
    print("正态分布假设下Z检验值为：",mi.z_norm)
    print("正态分布假设下Z检验的P值为：",mi.p_norm)

    from splot.esda import plot_moran
    plot_moran(mi, zstandard=True, figsize=(10,4))
    plt.savefig(r"G:\geodata\SpatialAnalysisUCAS\Output\Ex2\\global_Moran"+c+".svg")
    plt.show()

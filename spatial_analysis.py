import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KernelDensity

def calculate_kde(gdf, bandwidth=0.01):
    # 核密度估计
    coords = np.array([[point.x, point.y] for point in gdf.geometry])
    kde = KernelDensity(bandwidth=bandwidth, metric='haversine')
    kde.fit(np.radians(coords))
    
    return kde

def cluster_analysis(gdf, eps=0.02, min_samples=10):
    # DBSCAN聚类
    coords = np.array([[point.x, point.y] for point in gdf.geometry])
    db = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine').fit(np.radians(coords))
    
    gdf['cluster'] = db.labels_
    return gdf

def classify_zone(cluster_gdf):
    # 功能区分类
    def _classify_cluster(group):
        counts = group['category'].value_counts()
        if counts.get('商业', 0) > 50:
            return '商业区'
        elif counts.get('居住', 0) > 30:
            return '居住区'
        else:
            return '综合区'
    
    return cluster_gdf.groupby('cluster').apply(_classify_cluster)

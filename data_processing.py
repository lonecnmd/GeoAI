import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def preprocess_poi(data_path):
    # 读取原始数据
    df = pd.read_csv(data_path)
    
    # 分类映射字典
    category_mapping = {
        '餐饮': '商业',
        '购物': '商业',
        '公司': '办公',
        '住宅区': '居住',
        '工厂': '工业',
        '学校': '教育',
        '医院': '医疗'
    }
    
    # 数据清洗
    df = df.dropna(subset=['latitude', 'longitude'])
    df['category'] = df['type'].map(category_mapping).fillna('其他')
    
    # 创建地理数据框架
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = gpd.GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)
    
    return gdf

if __name__ == "__main__":
    raw_data = "data/raw_poi.csv"
    processed_gdf = preprocess_poi(raw_data)
    processed_gdf.to_file("data/processed_data.geojson", driver='GeoJSON')

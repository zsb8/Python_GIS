# Python_GIS
Input coordinate and get the Geocode from Statistics Canada.    

My developed Python program uses geographical information from a shapefile and a data frame with coordinates to identify the geographical area that a given coordinate belongs to. This analysis is performed using the Shapely library, which helps to determine the relevant geocode (a unique identifier for the geographical area) and add it as a new column to the original data frame. The output of this program associates a set of coordinates with a specific geographical area, providing valuable information for mapping and spatial analysis purposes.

# Main code
```
value = df.loc[:, [df_point_column]].iat[0, 0]
if isinstance(value, str) or isinstance(value, list):
    # Convert the data of df_point_column from str format into the list format.
    if isinstance(value, str):
        df = df.fillna('')
        df['point_list'] = df[df_point_column].apply(
            lambda x: [float(x[1:len(x) - 1].split(',')[0]), float(x[1:len(x) - 1].split(',')[1])] if x else [])
        df.drop(df_point_column, axis=1, inplace=True)
        df.rename(columns={'point_list': df_point_column}, inplace=True)
    df[boundary_columns] = df[df_point_column].apply(lambda x: Point(x[0], x[1]) if x else None)
    # Convert df into geo format as geo_df, it was user inputted.
    geo_df = geopandas.GeoDataFrame(df)
    geo_df = geo_df.set_crs('EPSG:4326')
    # EPSG:3347 is the standard statistics canada projection.
    geo_df = geo_df.to_crs('EPSG:3347')
    # Get the data set from boundary file as gdf.
    gdf = geopandas.read_file(boundary_path)

    def _get_geo(point):
        """
        Different .shp has different column name of uid. For example:
        lcsd000a16a_e.shp's uid is 'CSDUID',
        lcma000a16a_e.shp's uid is 'CMAUID'

        :param shapely.geometry.point.Point point: Such as (5354427.099462914 1881290.5749068991)
        :return str geo: Such as '539'.
        """
        gdf['geocode'] = gdf[boundary_columns].apply(lambda x: True if x.contains(point) else False)
        try:
            uid = gdf.columns[0]
            geo_row = gdf.loc[gdf["geocode"] == True][uid]
        except Exception as error:
            print(f"Error! \n {error}")
            print(traceback.format_exc())
            return None
        geo = '' if geo_row.empty else str(geo_row.values[0])
        return geo

    geo_df['geocode'] = geo_df[boundary_columns].apply(lambda x: _get_geo(x) if x else '')
    result = geo_df
```
# Resilt product
I developed and provided various data tools that were utilized in data analysis projects. These tools were designed to gather, clean, transform, and store large amounts of data in a centralized location. This allowed data analysts and scientists to easily access and analyze the data, using a variety of visualization and reporting tools.     

![image](https://user-images.githubusercontent.com/75282285/222921777-71a3baca-d046-4741-8e28-d6e3e3b1d424.png)

One key aspect of these data tools was their ability to display the analyzed data in maps and reports, providing key insights and visualizations for stakeholders. This was accomplished through the use of mapping and reporting tools such as Tableau, Power BI, and ArcGIS, among others.    
![image](https://user-images.githubusercontent.com/75282285/222921794-d2da7291-78c5-4ed7-857d-3fe97cff875d.png)



# Data Source
![image](https://user-images.githubusercontent.com/75282285/218524464-67f4b510-03ad-4732-afa0-0b89d7b0a89b.png)

# How to use
![image](https://user-images.githubusercontent.com/75282285/218524658-688163a6-22f0-43f2-b65e-e2a76b9b2be3.png)

my data tool
![image](https://user-images.githubusercontent.com/75282285/218524740-369a7233-25b8-4574-8397-6569973cfa4f.png)

# Test result
![image](https://user-images.githubusercontent.com/75282285/218524966-8774bdaa-45b4-4d4b-8389-51fba44a379e.png)


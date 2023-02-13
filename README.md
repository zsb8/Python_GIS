# Python_GIS
input coordinate and get the Geocode from Statistics Canada.    

The developed Python program uses geographical information from a shapefile and a data frame with coordinates to identify the geographical area that a given coordinate belongs to. This analysis is performed using the Shapely library, which helps to determine the relevant geocode (a unique identifier for the geographical area) and add it as a new column to the original data frame. The output of this program associates a set of coordinates with a specific geographical area, providing valuable information for mapping and spatial analysis purposes.

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

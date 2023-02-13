import geopandas
import traceback
import pandas as pd
from shapely.geometry import Point


def point_areadata(df='', df_point_column='', boundary_path='', boundary_columns='geometry'):
    """ Main program.
    The purpose of the function is to submit a data frame with a coordinate, a string that leads to a shapefile -
    then the function returns any data from the shape file that is requested(could be a geocode, but could be other data).
    (1) Input one data set, such as the data get from listing_lat_long() of es.py of wbdt private package. -
    This data set includes coordinates, such as [-79.246943, 42.985294], -
    because we need this info to search in the boundary file.
    (2) Boundary file is the digital boundary file in shapefile format, can download from statcan.gc.ca or by other way)
    (3) Input the names of the fields in the boundary file, because we need to know where to find the useful info.

    :param Dataframe df: The data set is get from listing_lat_long() of es.py of wbdt private package.
    :param str df_point_column:
        Column name from the dataframe that contains the coordinates([-79.246943, 42.985294]).
        This column name is in the df. Such as 'point'.
        Please note, the data of this column can be str such as '[-79.246943, 42.985294]', also can be a really list.
    :param str boundary_path:
        The path of the boundary file. Such as 'D:/waybase_gis_functions/data/lcsd000a16a_e.shp'.
    :param list of string boundary_columns:
        Default is 'geometry'.
        In the boundary file that contains the geocode or any column associate to the shapefile.
        It determines what columns get returned from the shapefile.
        This column name is in the boundary file.
    :return DataFrame result:
        The original dataframe and add a new column that contains the geocode or any column associated to the shapefile.
        Geocode, such as ['pr-35']  or ['ada-47140007', 'cd-4714'].
        Return whatever was used in the df param.
    """
    try:
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
        else:
            print("If df_point_column is not str or list, can't get the geocode.")
            result = None
    except Exception as error:
        print(f"Error! \n {error}")
        print(traceback.format_exc())
        result = None
    return result


if __name__ == '__main__':
    data1 = [
        {"a": 1, "b": 5, "point": [-104.497882, 52.328702]},
        {"a": 2, "b": 6, "point": [-79.246943, 42.985294]},
        {"a": 3, "b": 7, "point": [-73.759167, 45.363935]}
    ]
    data2 = [
        {"a": 1, "b": 5, "point": '[-104.497882, 52.328702]'},
        {"a": 2, "b": 6, "point": '[-79.246943, 42.985294]'},
        {"a": 3, "b": 7, "point": '[-73.759167, 45.363935]'}
    ]
    index = [0, 1, 2]
    columns = ["a", "b", "point"]
    mydf = pd.DataFrame(data2, index, columns)
    # mydf = pd.read_csv('d:/entire_points_and_geocode20220210.csv')
    print(f"\n{mydf}")
    print("Query geocode result is".center(60, '-'))
    my_df_point_column = 'point'
    my_boundary_path = 'D:/waybase_gis_functions/data/lcma000a16a_e.shx'   # lcma000a16a_e  lcsd000a16a_e
    result_test = point_areadata(mydf, my_df_point_column, my_boundary_path)
    print(result_test)

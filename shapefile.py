import shapefile
import matplotlib.pyplot as plt


def point_areadata(df='', df_point_column='', boundary_path='', boundary_columns=''):
    """
    The purpose of the function is to submit a data frame with a coordinate, a string that leads to a shapefile -
    then the function returns any data from the shape file that is requested(could be a geocode, but could be other data).
    (1) Input one data set, such as the data get from listing_lat_long() of es.py of wbdt private package. -
    This data set includes coordinates, such as [-79.246943, 42.985294], -
    because we need this info to search in the boundary file.
    (2) Boundary file is the digital boundary file in shapefile format, can download from statcan.gc.ca or by other way)
    (3) Input the names of the fields in the boundary file, because we need to know where to find the useful info.

    Parameters
    ----------
    df: Dataframe
        The data set is get from listing_lat_long() of es.py of wbdt private package.
    df_point_column: str
        Column name from the dataframe that contains the coordinates([-79.246943, 42.985294]).
        This column name is in the df. Such as 'point'.
    boundary_path: str
         The path of the boundary file. Such as 'd:/lpr_000b16a_e.shp' or other boundary file.
    boundary_columns: list of string
        In the boundary file that contains the geocode or any column associate to the shapefile.
        It determines what columns get returned from the shapefile.
        This column name is in the boundary file.

    Returns
    -------
    result: DataFrame
        The original dataframe and add a new column that contains the geocode or any column associated to the shapefile.
        Geocode, such as ['pr-35']  or ['ada-47140007', 'cd-4714'].
        Return whatever was used in the df param.

    """
    print("人口细分".center(30, "-"))
    sf = shapefile.Reader('D:/waybase_gis_functions/data/lcsd000a16a_e.shp')
    shapes = sf.shapes()
    print(f"{len(shapes)}")
    print(f"{shapes[0:2]}")
    pts = shapes[0].points
    prt = shapes[0].parts
    print(f"pts列表长度=={len(pts)}")
    print(f"prt样例=={pts[0:2]}")
    print(f"prt列表长度=={len(prt)}")
    print(f"prt样例=={prt}")
    # shapeType 数据类型(点，shapeType=1，线，shapeType=3，多边形，shapeType=5)
    print(f"类型=={shapes[0].shapeType}")
    # bbox 数据范围(bbox)：就是经纬度的最大最小值，四个，上下左右
    print(f"经纬度最大最小数值即上下左右={shapes[0].bbox}")
    # parts 数据块(parts) : 边界会出现断开的现象，那从哪开始断开呢，就在这个属性里面记录。parts属性是一个列表，记录了每个区块第一个点的索引值，即下标
    print(f"下标=={shapes[0].parts}")



    print("省份".center(30, "-")) # 12个shape
    sf = shapefile.Reader('D:/waybase_gis_functions/data/lpr_000b16a_e.shp')
    shapes = sf.shapes()
    print(f"{len(shapes)}")
    print(f"{shapes[0:2]}")
    pts = shapes[0].points
    prt = shapes[0].parts
    print(f"pts=={len(pts)}")
    print(f"prt=={pts[0:2]}")
    print(f"prt=={len(prt)}")
    print(f"prt=={prt[0:2]}")
    draw(pts)


def draw(pts):
    x, y = zip(*pts)  # 把经纬度分别给到x,y
    fig = plt.figure(figsize=[12, 18])
    ax = fig.add_subplot(111)
    ax.plot(x, y, '-', lw=1, color='k')
    plt.show()


if __name__ == '__main__':
    point_areadata()


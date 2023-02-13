import psycopg2
import sys
import time
import pandas as pd
import numpy as np
import traceback
from utils.setting import Setting
PARAM_DIC = Setting.PARAM_DIC


def connect():
    """
    Connect to the PostgreSQL database server.
    :return: conn or None
    """
    try:
        conn = psycopg2.connect(**PARAM_DIC)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"error:{error},PARAM_DIC:{PARAM_DIC}")
        sys.exit(1)
        return None
    return conn


def execute_sql(sql):
    """
    Query any sql in one table
    :param sql: str
    :return: results:  list, such as [('A',), ('AA',), ('AAAIF',), ('AAALF',)]
    You should be get the value such as return_value[0][0] in your coding.
    """
    conn_db = connect()
    cursor = conn_db.cursor()
    try:
        cursor.execute(sql)
    except Exception as error:
        print(f"error:{error}")
        print(traceback.format_exc())
        cursor.close()
        conn_db.close()
        return None
    results = cursor.fetchall()
    conn_db.commit()
    cursor.close()
    conn_db.close()
    return results


def get_geom(dic):
    keys = list(dic.keys())
    print(keys)
    geom = dic['geom']
    print(type(geom))
    keys = list(geom.keys())
    print(keys)
    coordinates = geom['coordinates']
    print(type(coordinates))
    print(len(coordinates[0][0]))  # 18680
    list_result = coordinates[0][0]
    return dic, geom, list_result


def get_geom_by_st_asgeojson(dic):
    keys = list(dic.keys())
    print(keys)
    geom = dic['geometry']
    print(type(geom))
    keys = list(geom.keys())
    print(keys)
    coordinates = geom['coordinates']
    print(type(coordinates))
    print(len(coordinates[0][0]))  # 18680
    list_result = coordinates[0][0]
    return dic, geom, list_result


def creat_polygon(data):
    """
    输入一个Polygon，转成list列表类型。
    :param data:  (shapely.geometry.polygon.Polygon)
        such as POLYGON ((7239903.86857 950427.5171450004, 7239920.95143 950390.6485700011,...))
    :return:
    """
    x, y = data.exterior.coords.xy
    print(f"x长度是=={len(x)}")
    print(x)
    print(f"y长度是=={len(y)}")
    print(y)
    lst = []
    for s in range(len(x)):
        xy = (x[s], y[s])
        lst.append(xy)
    return lst


def create_point_obj(lst):
    for i in lst:
        x, y = i


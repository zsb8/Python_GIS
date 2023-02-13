import gis as gpd
from utils import functions
import json
# import fiona
# print(gpd.__version__)
# gdf = gpd.read_file('D:/waybase_gis_functions/data/lcsd000a16a_e.shp')
# print(gdf.shape)

#----------查询JSON里面的内容----------

# sql = 'select row_to_json(a.*)  from lpr_000b16a_e as a limit 1'
# sql = 'select row_to_json(a.*)  from lct_000a16a_e as a limit 1'
# lst = functions.execute_sql(sql)
# data = dict(lst[0][0])
# dic = functions.get_geom(data)[0]
# geom = functions.get_geom(data)[1]
# print(dic)


# sql = 'select st_asgeojson(a.*)  from lct_000a16a_e as a limit 1'
# lst = functions.execute_sql(sql)
# data = eval(lst[0][0])
# print(lst[0][0])
# dic = functions.get_geom_by_st_asgeojson(data)[0]
# geom = functions.get_geom_by_st_asgeojson(data)[1]
# print(dic)


# sql = 'select row_to_json(fields) as json_row from ' \
#       '(select a.gid,a.prname,a.geom from  lct_000a16a_e as a limit 1) as fields'
# lst = functions.execute_sql(sql)
# print(lst)
# data = lst[0][0]
# dic = functions.get_geom(data)[0]
# print(dic)


# 判断是否落在区间内
sql = "SELECT ST_Contains((SELECT geom FROM lct_000a16a_e WHERE gid = 1),st_geometryfromtext('POINT(8980216 2151065)', 26918));"
result_sql = functions.execute_sql(sql)
result = result_sql[0][0]
print(result)

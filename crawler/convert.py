import sqlite3
old_conn = sqlite3.connect('equipment.db')
old_conn.text_factory = str
old_cur = old_conn.cursor()
new_conn = sqlite3.connect('new.db')
new_conn.text_factory = str
new_cur = new_conn.cursor()


old_cur.execute('select * from equipment')
res = old_cur.fetchall()

for item in res:
    (id,attr_496,attr_556,attr_557,attr_7,attr_277,attr_334,attr_255,attr_279,attr_278,attr_256,attr_511,attr_332,attr_314,attr_312,attr_399,attr_315,attr_313,attr_539,attr_401,attr_345,attr_285,attr_405,attr_286,attr_287,attr_505,attr_289,attr_351,attr_355,attr_292,attr_295,attr_353,attr_352,attr_288,attr_309,attr_307,attr_305,attr_297,attr_298,attr_301,attr_303,attr_335,attr_336,attr_337,attr_404,attr_340,attr_342,attr_341,attr_522,attr_343,attr_273,attr_274,attr_275,attr_281,attr_412,attr_413,attr_414,attr_310,attr_488,attr_491,attr_489,attr_321,attr_323,attr_490,attr_328,attr_368,attr_494,attr_548,attr_283,attr_397,attr_398,attr_5,attr_13,attr_15,attr_16,attr_21,attr_333,attr_24,attr_25,attr_26,attr_27,attr_540,attr_754,attr_31,attr_329,attr_499,attr_492,item_name,item_brand,item_type,item_image) = item
    for i in (attr_496,attr_556,attr_557,attr_7,attr_277,attr_334,attr_255,attr_279,attr_278,attr_256,attr_511,attr_332,attr_314,attr_312,attr_399,attr_315,attr_313,attr_539,attr_401,attr_345,attr_285,attr_405,attr_286,attr_287,attr_505,attr_289,attr_351,attr_355,attr_292,attr_295,attr_353,attr_352,attr_288,attr_309,attr_307,attr_305,attr_297,attr_298,attr_301,attr_303,attr_335,attr_336,attr_337,attr_404,attr_340,attr_342,attr_341,attr_522,attr_343,attr_273,attr_274,attr_275,attr_281,attr_412,attr_413,attr_414,attr_310,attr_488,attr_491,attr_489,attr_321,attr_323,attr_490,attr_328,attr_368,attr_494,attr_548,attr_283,attr_397,attr_398,attr_5,attr_13,attr_15,attr_16,attr_21,attr_333,attr_24,attr_25,attr_26,attr_27,attr_540,attr_754,attr_31,attr_329,attr_499,attr_492,item_name,item_brand,item_type,item_image):
        try:
            i = i.decode('gbk').encode('utf-8')
        except:
            continue
        i = i.replace("'","\'")
    sql = "insert into equipment(attr_496,attr_556,attr_557,attr_7,attr_277,attr_334,attr_255,attr_279,attr_278,attr_256,attr_511,attr_332,attr_314,attr_312,attr_399,attr_315,attr_313,attr_539,attr_401,attr_345,attr_285,attr_405,attr_286,attr_287,attr_505,attr_289,attr_351,attr_355,attr_292,attr_295,attr_353,attr_352,attr_288,attr_309,attr_307,attr_305,attr_297,attr_298,attr_301,attr_303,attr_335,attr_336,attr_337,attr_404,attr_340,attr_342,attr_341,attr_522,attr_343,attr_273,attr_274,attr_275,attr_281,attr_412,attr_413,attr_414,attr_310,attr_488,attr_491,attr_489,attr_321,attr_323,attr_490,attr_328,attr_368,attr_494,attr_548,attr_283,attr_397,attr_398,attr_5,attr_13,attr_15,attr_16,attr_21,attr_333,attr_24,attr_25,attr_26,attr_27,attr_540,attr_754,attr_31,attr_329,attr_499,attr_492,item_name,item_brand,item_type,item_image) values (\""
    sql += "\",\"".join(map(str, (attr_496,attr_556,attr_557,attr_7,attr_277,attr_334,attr_255,attr_279,attr_278,attr_256,attr_511,attr_332,attr_314,attr_312,attr_399,attr_315,attr_313,attr_539,attr_401,attr_345,attr_285,attr_405,attr_286,attr_287,attr_505,attr_289,attr_351,attr_355,attr_292,attr_295,attr_353,attr_352,attr_288,attr_309,attr_307,attr_305,attr_297,attr_298,attr_301,attr_303,attr_335,attr_336,attr_337,attr_404,attr_340,attr_342,attr_341,attr_522,attr_343,attr_273,attr_274,attr_275,attr_281,attr_412,attr_413,attr_414,attr_310,attr_488,attr_491,attr_489,attr_321,attr_323,attr_490,attr_328,attr_368,attr_494,attr_548,attr_283,attr_397,attr_398,attr_5,attr_13,attr_15,attr_16,attr_21,attr_333,attr_24,attr_25,attr_26,attr_27,attr_540,attr_754,attr_31,attr_329,attr_499,attr_492,item_name,item_brand,item_type,item_image)))
    sql += "\")"
    new_cur.execute(sql)

new_conn.commit()







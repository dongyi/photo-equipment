#coding=utf8
import urllib2
import re
import sqlite3
import sys

conn = sqlite3.connect('equipment.db')
cur = conn.cursor()


page_number_pattern = re.compile("""(?<=/)\d(?=</span>)""")
item_pattern = re.compile("""(?<=<td class="t-name"><a href=").*(?=" target="_blank">)""")
item_id_pattern = re.compile("(?<=id=)\d+")
item_name_pattern = re.compile("""(?<=alt=").*?(?=">)""")
item_type_pattern = re.compile("""(?<=category_2=\d">).*?(?=</a>)""")
item_brand_pattern = re.compile("""(?<=brand_from=.">).*?(?=</a>)""")
item_image_pattern = re.compile("""(?<=img\ src=\")uploads.*jpg""")


attr_ids = [496,556,557,7,277,334,255,279,278,256,511,332,
            314,312,399,315,313,539,401,345,285,405,286,287,
            505,289,351,355,292,295,353,352,288,309,307,305,
            297,298,301,303,335,336,337,404,340,342,341,522,
            343,273,274,275,281,412,413,414,310,488,491,489,
            321,323,490,328,368,494,548,283,397,398,
            5,13,15,16,21,333,24,25,26,27,540,754,
            31,329,499,492]

attr_patterns = {}

for i in attr_ids:
    attr_patterns[str(i)] = """(?<=attr_id\=\"%d\"\ union\=\".\"\ content=\").*?(?=")"""%i

category_page = """
http://www2.xitek.com/production/post.php?a=list&parent=2&cid=3&show=1
http://www2.xitek.com/production/post.php?a=list&parent=2&cid=4&show=1
http://www2.xitek.com/production/post.php?a=list&parent=2&cid=5&show=1
http://www2.xitek.com/production/post.php?a=list&parent=2&cid=7&show=1
http://www2.xitek.com/production/post.php?a=list&parent=2&cid=6&show=1
http://www2.xitek.com/production/post.php?a=list&parent=56&cid=8&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=12&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=10&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=11&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=13&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=14&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=15&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=16&show=1
http://www2.xitek.com/production/post.php?a=list&parent=9&cid=18&show=1
http://www2.xitek.com/production/post.php?a=list&parent=19&cid=20&show=1
http://www2.xitek.com/production/post.php?a=list&parent=19&cid=22&show=1
http://www2.xitek.com/production/post.php?a=list&parent=19&cid=23&show=1
http://www2.xitek.com/production/post.php?a=list&parent=19&cid=21&show=1
http://www2.xitek.com/production/post.php?a=list&parent=19&cid=24&show=1
""".split()


def process_category(category_link):
    page_code = urllib2.urlopen(category_link).read()
    page_number = re.findall(page_number_pattern, page_code)
    if len(page_number) > 0:
        page_number = str(page_number[0])
    else:
        page_number = 0
    pages = [category_link + "&order=title&sort=ASC&s_p_a=&page=" + str(link) for link in range(1, int(page_number)+1)]

    for p in pages:
        try:
            process_page(p)
        except:
            print "fuck 1"
            continue

def process_page(page_link):
    page_code = urllib2.urlopen(page_link).read()
    item_link = re.findall(item_pattern, page_code)
    for i in item_link:
        try:
            process_item(i)
        except:
            print "fuck 2"
            continue

def process_item(item_link):
    item_id = re.findall(item_id_pattern, item_link)[0]
    item_detail_link = "http://www2.xitek.com/production/product.php?a=basic&id="+str(item_id)
    page_code = urllib2.urlopen(item_detail_link).read()
    item_name = re.findall(item_name_pattern, page_code),
    item_type = re.findall(item_type_pattern, page_code),
    item_brand = re.findall(item_brand_pattern, page_code),
    item_image = re.findall(item_image_pattern, page_code),
    item = dict()

    item['item_name'] = item_name[0][0] if len(item_name)>0 else 'no name'
    item['item_type'] = item_type[0][0] if len(item_type)>0 else 'no type'
    item['item_brand'] = item_brand[0][0] if len(item_brand)>0 else 'no brand'
    item['item_image'] = item_image[0][0] if len(item_image)>0 else 'no image'

    for attr, p in attr_patterns.items():
        try:
            res = re.findall(p, page_code)
            if len(res) > 0:
                item['attr_'+str(attr)] = res[0]
        except:
            continue
    fields = []
    values = []
    table_name = 'equipment'
    for f, v in item.iteritems():
        if type(v) in [str, unicode]:
            v = "'%s'"%v
        fields.append(str(f))
        values.append(str(v))
        fields_txt = ','.join(fields)
        values_txt = ','.join(values)
    sql = 'INSERT INTO %s (%s) VALUES (%s)'%(table_name, fields_txt, values_txt)
    with open('sql_record.txt', 'a') as f:
        f.write(sql)
        cur.execute(sql)
    conn.commit()

def main(cnt):
    process_category(category_page[cnt])

    #for category in category_page:
    #    process_category(category)

if __name__ == '__main__':
    main(int(sys.argv[1]))

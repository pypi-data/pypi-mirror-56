# Insert your code here.
# _*_coding:utf-8_*_
# Insert your code here.
# _*_coding:utf-8_*_
import hashlib,json,re,os
import time
import datetime
import redis,execjs
from os import listdir
import jieba.posseg as pseg
import arrow
import math,pymysql
from scrapy import Selector
import pytesseract,requests
from PIL import Image
from io import BytesIO

#红色输出
def red_print(str):
    print('\033[31m{}\033[0m'.format(str))

class Auto_indb():
    def __init__(self,host='',username='',password='',db='',table_name='',comment='',create_tables=True):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.comment = comment  #表注释
        self.table_name = table_name
        self.create_tables = create_tables  #是否创建表
        try:
            self.conn = pymysql.connect(self.host, self.username, self.password, self.db,charset='utf8')
            self.cursor = self.conn.cursor()
            print("连接数据库成功")
        except:
            raise ('连接数据库失败')
        self.columns = self.get_columns()
        if create_tables:
            self.table_exists()

    def table_exists(self):
        hassql = ' show tables where Tables_in_%s ="%s"' % (self.db, self.table_name)
        has = self.cursor.execute(hassql)
        if has:
            print("该{}表已经存在".format(self.table_name))
            judge = input("是否需要删除表重新建表 y/n:")
            if judge == 'y':
                drop_table = "drop table if exists {}".format(self.table_name)
                self.cursor.execute(drop_table)
                self.conn.commit()
                self.create_table()
            else:
                print("未创建表")
        else:
            self.create_table()

    def create_table(self):
        newtab = '''
                   CREATE TABLE `%s` (
                   	`id` INT(11) NOT NULL AUTO_INCREMENT primary key ,
                   	`url` TEXT not NULL,
                   	`updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
                   )
                   COMMENT='%s'
                   ENGINE=MyISAM;
                   ''' % (self.table_name, self.comment)
        self.cursor.execute(newtab)
        self.conn.commit()
        print("创建{}表成功".format(self.table_name))

    def get_columns(self):
        result = []
        sql = "select COLUMN_NAME from information_schema.columns where table_name='%s'" % self.table_name
        self.cursor.execute(sql)
        for res in self.cursor.fetchall():
            res = res[0]
            result.append(res)
        return result

    def insert_data(self,items):
        keys = ''
        vals = []
        s = ''
        for item in items.keys():
            if not item in self.get_columns():
                sql = 'alter table %s add %s text' % (self.table_name, item)
                self.cursor.execute(sql)
                self.conn.commit()
                self.columns.append(item)
            if item:
                keys += item + ','
                s += '%s,'
                vals.append(items.get(item))
        keys = keys[:-1]
        indbsrt = 'insert ignore into %s(%s) VALUES (%s)' % (self.table_name, keys, ','.join(pymysql.escape_string('%r') % str(i) for i in vals))
        print(indbsrt)
        self.cursor.execute(indbsrt)
        self.conn.commit()
        print("###################  insert data success ################")

# 使用说明:
# create_tables为是否自动建表,默认为True
# i = In_db(host='192.168.4.201',username='root',password='mysql',db="storm",table_name='',comment='表注释',create_tables=True)
# item要插入的字典
# i.insert_data(item)
class Auto_sinsert():
    def __init__(self,host='',username='',password='',db='',drop_column=["id","update"]):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.drop_column = drop_column  #表删除字段
        try:
            self.conn = pymysql.connect(self.host, self.username, self.password, self.db,charset='utf8')
            self.cursor = self.conn.cursor()
            print("连接数据库成功")
        except:
            raise ValueError('连接数据库失败')
        self.table_name_list = self.get_db_name()

    def get_db_name(self):
        sql = "select table_name from information_schema.tables where table_schema='{}'".format(self.db)
        self.cursor.execute(sql)
        db_list = self.cursor.fetchall()
        db_list = [i[0] for i in db_list]
        return db_list

    def get_columns(self):
        item = {}
        for table_name in self.table_name_list:
            sql = "select column_name from information_schema.columns where table_name=%r and table_schema=%r"%(table_name,self.db)
            self.cursor.execute(sql)
            column_list = self.cursor.fetchall()
            column_list = [i[0] for i in column_list]
            insert_columns = [i for i in column_list if i not in self.drop_column]
            item[table_name] = insert_columns
        return item

    def insert_data(self,item,table_name):
        if item:
            insert_tables_key = self.get_columns()
            item_key = insert_tables_key.get(table_name)
            if item_key:
                item_values = [item.get(i) for i in item_key]
                sql = 'insert ignore into {}('.format(table_name)+','.join(item_key)+')values('+','.join([pymysql.escape_string('%r') %str(i) for i in item_values])+')'
                self.cursor.execute(sql)
                self.conn.commit()
                print("###################  insert data success ################")
            else:
                raise ValueError("没有{}表".format(table_name))
        else:
            print("item is None")

# 使用说明:
# item = {'key':'none'}
# # drop_column 为所有表中不插入的字段
# a = Auto_sinsert(host='192.168.4.201',username='root',password='mysql',db='zhijianju',drop_column=["id","jid","update","entid"])
# a.insert_data(item,'aqsiq_biaozhun_basic')

#执行sql语句
class Execute_sql():
    def __init__(self,host='',username='',password='',db=''):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        try:
            self.conn = pymysql.connect(self.host, self.username, self.password, self.db,charset='utf8')
            self.cursor = self.conn.cursor()
            print("连接数据库成功")
        except:
            raise ValueError('连接数据库失败')

    def select_sql(self,cloumns= '*',table_name='',limit='10'):
        sql = 'select {} from {} limit {}'.format(cloumns,table_name,limit)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def get_scrapy_filed(self,table_name):
        sql = '''
        select column_name,column_comment from information_schema.columns where table_name='{}' and table_schema='{}'
        '''.format(table_name,self.db)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            red_print('----------------------------------------------------------')
            for item in result:
                item = '{} = scrapy.Field() #{}'.format(item[0],item[1])
                print(item)
            red_print('----------------------------------------------------------')
            for item in result:
                item = "item['{}'] = get_column(response,'') #{}".format(item[0], item[1])
                print(item)
            red_print('----------------------------------------------------------')
            os._exit(0)

        else:
            red_print('no result')
            return None


    def custom(self,sql,state='commit'):
        self.cursor.execute(sql)
        if state=='commit':
            self.conn.commit()
        elif state == 'fetchall':
            result = self.cursor.fetchall()
            if result:
                return result
            else:
                red_print('no result')
                return None
        else:
            red_print("no practice way,please appoint commit or fetchall")


# execute_sql = Execute_sql(host='192.168.4.201',username='root',password='mysql',db='zhijianju')

class Debug_code():
    def __init__(self,url):
        self.url = url
    def get(self,headers, xpath=''):
        res = requests.get(url=self.url, headers=headers, timeout=5)
        try:
            text = res.json()
            print(text)
            result = get_column(text, xpath)
            print(result)
        except:
            text = res.text
            print(text)
            result = get_column(text, xpath)
            print(result)

    def post(self, headers, data, xpath=''):
        res = requests.post(url=self.url, headers=headers, data=data, timeout=5)
        try:
            text = res.json()
            print(text)
            result = get_column(text, xpath)
            print(result)
        except:
            text = res.text
            print(text)
            result = get_column(text, xpath)
            print(result)

class Redis_handle():
    def __init__(self,host='127.0.0.1',password='',db='1',decode_responses=True):
        self.db = db
        self.r = redis.Redis(host=host, port=6379, password=password, db=db, decode_responses=decode_responses)
        red_print("链接redis成功")

    def push_queue(self):
        for i in range(10):
            print(i)
            self.r.rpush(self.db, i)

    def get_out(self):
        while True:
            if self.r.llen(1) == 0:
                print("redis队列值为空,程序退出")
                os._exit(0)
                self.r.lpop(self.db)

def str2dict(headers_raw):
    if headers_raw is None:
        return None
    headers = headers_raw.splitlines()
    headers_tuples = [header.split(':', 1) for header in headers]
    result_dict = {}
    for header_item in headers_tuples:
        if not len(header_item) == 2:
            continue
        item_key = header_item[0].strip()
        item_value = header_item[1].strip()
        result_dict[item_key] = item_value
    return result_dict
#列表分组
def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) *children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list

def get_column(response, xpath,str_add='',Auto_wash=True):
    if xpath:
        if isinstance(response,dict):
            return response.get(xpath)
        if isinstance(response, str):
            response = Selector(text=response)
        if isinstance(xpath,list):
            value = ''.join(xpath).replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0','').replace('\t', '')
            return value
        value_list = response.xpath(xpath).getall()
        if Auto_wash:
            result = []
            for value in value_list:
                value = value.replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\t', '').replace('\u3000', '')
                result.append(value)
            return str_add + ''.join(set(result))
        else:
            return str_add + ''.join(set(value_list))
    else:
        return None

def get_column_div_list(response, xpath):
    if isinstance(response, str):
        response = Selector(text=response)
    value_list = response.xpath(xpath)
    return value_list

def get_column_list(response, xpath,str_add='',Auto_wash=True):
    if isinstance(response, str):
        response = Selector(text=response)
    value_list = response.xpath(xpath).getall()
    if Auto_wash:
        value_new_list = []
        for value in value_list:
            value = value.replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\t', '')
            value_new_list.append(str_add+value)
        return list(set(value_new_list))
    else:
        return value_list

def get_column_re_list(rule, text,str_add='',Auto_wash=True):
    value_list = re.findall(rule,text,re.S)
    if Auto_wash:
        value_new_list = []
        for value in value_list:
            value = value.replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\t', '')
            value_new_list.append(str_add+value)
        return list(set(value_new_list))
    else:
        value_new_list = []
        for value in value_list:
            value_new_list.append(str_add + value)
        return list(set(value_new_list))

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

def get_md5_sz(url):
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# url去重MD5
def get_md5(url):
    if isinstance(url, list) or isinstance(url, tuple) or isinstance(url, str):
        url = str(url)
    m = hashlib.md5()
    if isinstance(url, str):
        url = url.encode('utf-8')
    m.update(url)
    return m.hexdigest()

def get_md5_by_sql(sql, cursor, key):
    # key 代表sql中 字段名。
    try:
        cursor.execute(sql)
        rst = cursor.fetchone()
        md55 = rst[key]
        return md55
    except Exception as ex:
        raise Exception(ex)

# 字符串转元组
def str2tuple(str):
    return tuple(eval(str.split('(')[-1].split(')')[0]))

def cn2en(url):
    md = get_md5(url)[8:24].replace('0', 'g').replace('1', 'h').replace('2', 'i').replace('3', 'j').replace('4',
                                                                                                          'k').replace(
        '5', 'l').replace('6', 'm').replace('7', 'n').replace('8', 'o').replace('9', 'p')
    return md

def get_dict_key(dict, value):
    for i, j in dict.items():
        if j == value:
            return i

def collect_filename(path):
    filenames = listdir(path)
    return filenames

def running_days(amount=10, unit=3):
    """
    此for循环表示：往前推amount个三天;
    :param amount:
    :param unit:
    :return:
    """
    unit = unit - 1
    temp = 0
    for i in range(1, amount + 1):
        h = temp
        q = h + unit
        temp = q + 1
        searchDate = datetime.datetime.now() - datetime.timedelta(days=q)
        startdate = searchDate.strftime("%Y-%m-%d")
        enddate = datetime.datetime.now() - datetime.timedelta(days=h)
        if searchDate > enddate:
            raise Exception('12333')
        enddate = enddate.strftime("%Y-%m-%d")
        yield [startdate, enddate]

def partition_days(TimeStart=None, TimeEnd=None, number=None):
    # TimeStart='2018-08-16'
    # TimeEnd='2018-08-16'
    # number=2
    """
      方法含义：在时间区间划分多少分;

      :param amount:
      :param unit:
      :return:
      """
    TimeStart = arrow.get(TimeStart).datetime
    TimeEnd = arrow.get(TimeEnd).datetime
    days = TimeEnd - TimeStart
    days = days.days
    unit = int(math.ceil(days / float(number)))
    temp = 0
    for i in range(number):
        q = temp
        w = (i + 1) * unit
        temp = w + 1
        searchDate = TimeEnd - datetime.timedelta(days=0 + w)
        startdate = searchDate.strftime("%Y-%m-%d")
        enddate_ = TimeEnd - datetime.timedelta(days=0 + q)
        if searchDate > enddate_:
            raise Exception('12333')
        enddate = enddate_.strftime("%Y-%m-%d")
        if searchDate < TimeStart:
            startdate = TimeStart.strftime("%Y-%m-%d")
        yield [startdate, enddate]

def getAllName(messageContent):
    words = pseg.cut(messageContent)
    names = []
    for word, flag in words:
        # print('%s,%s' % (word, flag))
        if flag == 'nr':  # 人名词性为nr
            print(word, '*' * 50)
            names.append(word)
    return names
#识别验证码或者电话号码
def image_recognize_url(url,max_lenth=None,max_try=10,headers=None):
    n = 0
    while n<max_try:
        res = requests.get(url,headers=headers,timeout=5)
        image = BytesIO(res.content)
        image = Image.open(image)
        im = image.convert('L')
        text = pytesseract.image_to_string(im)
        if max_lenth and len(text)==max_lenth:
            return text
        elif not max_lenth:
            if text:
                return text
            else:
                print("识别失败")
        else:
            print("识别失败")
            n+=1
    if n==max_try:
        print("无法识别该验证码")
        return None

def image_recognize_path(image_path):
    im = Image.open('{}'.format(image_path))
    auth = pytesseract.image_to_string(im)
    return auth


def get_photo(url,image_path,headers={}):
    path = '/'.join(image_path.split('\\')[:-1])
    if not os.path.exists(path):
        os.makedirs(path)
        red_print("创建{}文件夹".format(path))
    res = requests.get(url, headers=headers, timeout=5)
    with open(image_path,'wb')as f:
        f.write(res.content)
    red_print("{}download_success".format(image_path))

def get_pdf(url,image_path,headers={}):
    path = '/'.join(image_path.split('\\')[:-1])
    if not os.path.exists(path):
        os.makedirs(path)
        red_print("创建{}文件夹".format(path))
    res = requests.get(url, headers=headers, timeout=5)
    with open(image_path,'wb')as f:
        for i in res.iter_content():
            f.write(i)
            red_print("{}downloading...".format(image_path))
    red_print("{}download_success".format(image_path))

def get_item_field(items):
    red_print("复制item字段列表值")
    red_print('----------------------------------------------------------')
    for item in items.keys():
        item = '{} = scrapy.Field()'.format(item)
        print(item)
    red_print('----------------------------------------------------------')
    os._exit(0)

def excute_js(js_code_path,func,args):
    with open(js_code_path,'r')as f:
        js_code = f.read()
    js_code = execjs.compile(js_code)
    result = js_code.call(func,args)
    return result




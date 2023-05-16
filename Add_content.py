import os

import pymysql


def get_data():
    db = pymysql.connect(host='118.31.246.139', user='wh3000', password='dGhKcm8EBEMwAhSj', database='wh3000')
    db.set_charset('utf8')
    cursor = db.cursor()

    sql = f'select id,Name,Content,Class_ from wh3001'
    cursor.execute(sql)

    text_ls = []
    for l in cursor.fetchall():
        name = l[1]
        text_ls.append(name)
    # print(text_ls)
    return text_ls


def insert_data(Name, Content, Class_):
    db = pymysql.connect(host='118.31.246.139', user='wh3000', password='dGhKcm8EBEMwAhSj', database='wh3000')
    db.set_charset('utf8')
    cursor = db.cursor()

    sql = f'insert into wh3001(Name,Content,Class_) values ("{Name}","{Content}","{Class_}")'
    cursor.execute(sql)
    db.commit()


basedir = r'C:\Users\Wangshaoyu\Desktop\wh3001'
dir1 = os.listdir(basedir)
for class_name in dir1:
    class_path = basedir + '\\' + class_name
    Class_ = class_name
    dir_class = os.listdir(class_path)
    for filename in dir_class:
        if '文本文档' in filename:
            continue
        filename_path = class_path + '\\' + filename
        Name = filename.replace('.txt', '')

        with open(filename_path, 'r', encoding='utf-8') as f:
            Content = f.read()
        # print(Class_, ' | ', Name, ' | ', Content)
        # input()
        exist_data = get_data()
        if Name in exist_data:
            print(Name, 'exist_data')
        else:
            insert_data(Name, Content, Class_)
            print(Name, 'success_add_data')
        # input()

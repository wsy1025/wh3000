from pprint import pprint

import pymysql
from flask import Flask, render_template,request,redirect
app = Flask(__name__)

def mk_data():
    db = pymysql.connect(host='118.31.246.139', user='wh3000', password='dGhKcm8EBEMwAhSj', database='wh3000')
    db.set_charset('utf8')
    cursor = db.cursor()

    sql = f'select id,Name,Content,Class_ from wh3001'

    cursor.execute(sql)

    text_dic = {}
    for l in cursor.fetchall():
        name = l[1]
        content = l[2]
        class_ = l[3]
        if not text_dic.get(class_):
            text_dic[class_] = []
        text_dic[class_].append({'name': name, 'content': content})
    # pprint(text_dic)
    db.close()
    return text_dic

def serch_o(class_,name_,fg):
    db = pymysql.connect(host='118.31.246.139', user='wh3000', password='dGhKcm8EBEMwAhSj', database='wh3000')
    db.set_charset('utf8')
    cursor = db.cursor()
    if class_ == None:
        if name_ == None:
            sql1 = f'select id,Name,Content,Class_ from wh3001'

        else:
            sql1 = f'select * from wh3001 where Name like "%{name_}%"'
    else:
        if name_ == None:
            sql1 = f'select * from wh3001 where Class_ like "%{class_}%"'
        else:
            sql1 = f'select * from wh3001 where Name like "%{name_}%"AND Class_ like "%{class_}%"'

    cursor.execute(sql1)
    text_dic = {}
    for l in cursor.fetchall():
        name = l[1]
        content = l[2]
        class_ = l[3]
        if not text_dic.get(class_):
            text_dic[class_] = []
            text_dic[class_].append({'name': name, 'content': content})
    pprint(text_dic)
    db.close()
    return text_dic

def search_data(word):
    db = pymysql.connect(host='118.31.246.139', user='wh3000', password='dGhKcm8EBEMwAhSj', database='wh3000')
    db.set_charset('utf8')
    cursor = db.cursor()
    result_ls = []
    text_dic = {}
    sql1 = f'select * from wh3001 where Name like "%{word}%"'
    sql2 = f'select * from wh3001 where Content like "%{word}%"'
    sql3 = f'select * from wh3001 where Class_ like "%{word}%"'
    for sql in [sql3, sql2, sql1]:
        cursor.execute(sql)
        results_1 = cursor.fetchall()
        for result in results_1:
            result_ls.append(result)
    results = list(set(result_ls))
    res = []
    for result in results:
        name = result[1]
        content = result[2]
        class_ = result[3]
        res.append({'name': name, 'content': content, 'class_':class_})
    # pprint(text_dic)
    db.close()
    return res

def search_all(fg=0):
    '''
    fg=0    根目录
    fg=1    文学篇-欧阳修
    fg=2    详细
    :param fg:
    :return:
    '''
    if fg == None:
        fg = 0
    db = pymysql.connect(host='118.31.246.139', user='wh3000', password='dGhKcm8EBEMwAhSj', database='wh3000')
    db.set_charset('utf8')
    cursor = db.cursor()
    ls = []
    sql1 = f'select Name,Class_,Content from wh3001'
    cursor.execute(sql1)
    results = cursor.fetchall()
    for result in results:
        if fg == 0:
            ls.append(result[1])
        elif fg == 1:
            ls.append({'name': result[0], "class_": result[1]})
        else:
            ls.append({'name': result[0], "class_": result[1], 'content': result[2]})
    if fg == 0:
        ls = list(set(ls))
        res = []
        for l in ls:
            res.append({"class_": l})
        return res
    return ls

def search_all_Class():
    db = pymysql.connect(host='118.31.246.139', user='wh3000', password='dGhKcm8EBEMwAhSj', database='wh3000')
    db.set_charset('utf8')
    cursor = db.cursor()
    ls = []
    sql1 = f'select Class_ from wh3001'
    cursor.execute(sql1)
    results = cursor.fetchall()
    for result in results:
        ls.append(result[0])
    ls = list(set(ls))
    return ls

@app.route('/', methods=["GET", "POST"])
def h_first():
    """
    0-文学篇
    1-文学篇 - 欧阳修
    2-详细的
    """
    fg = request.args.get('fg')
    if fg == None:
        fg = 0
    fg = int(fg)
    return render_template('h_0.html', data=search_all((fg)))

@app.route('/sc', methods=["GET", "POST"])
def sc():
    word = request.args.get('word')
    res = search_data(word)
    print(res)
    return render_template('h_search.html', data=res)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6004, debug=True)


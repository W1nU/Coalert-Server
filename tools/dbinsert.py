import pymysql
import openpyxl
from getpass import getpass

user = input('Insert username : ')
password = getpass('Insert password : ')

connect = pymysql.connect(host = 'localhost',
                          port = 3306,
                          user = user,
                          password = password,
                          db = 'coalert',
                          charset = 'utf8',
                          unix_socket = '/Applications/mampstack-7.0.30-0/mysql/tmp/mysql.sock')
cursor = connect.cursor()

wb = openpyxl.load_workbook('lip.xlsx')
ws = wb.active
temp = []

def company(ws):
    temp = []
    for i in ws.rows:
        if i[1].value == '제품명' or None:
            continue
        temp.append(i[2].value)

    company = list(set(temp))

    for i in company:
        if i == None:
            continue
        try:
            sql = f"""INSERT INTO company (bname) VALUE ('{i}')"""
            cursor.execute(sql)
            connect.commit()
        except Exception as e:
            print(e)
            continue

def cinfo(ws):
    temp = []
    for i in ws.rows:
        if i[1].value == '제품명' or None:
            continue
        try:
            cname_t = i[1].value + ' - ' + i[2].value
            print(cname_t)
            sql = f"""INSERT INTO cinfo (rank, cname, category, bname) VALUES ('{i[0].value}','{cname_t}', 4, '{i[2].value}')"""
            cursor.execute(sql)
            connect.commit()

        except Exception as e:
            print(e)
            continue

def cingr(ws):
    for i in ws.rows:
        if i[1].value == '제품명' or None:
            continue
        try:
            temp = str(i[3].value).split(',')
            for j in temp:
                cname_t = i[1].value + ' - ' + i[2].value
                sql = f"""INSERT INTO cingr (cname, ingr) VALUES ('{cname_t}','{j}')"""
                cursor.execute(sql)
                connect.commit()

        except Exception as e:
            print(e)
            continue

company(ws)
cinfo(ws)
cingr(ws)

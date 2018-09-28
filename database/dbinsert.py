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
        if i[1].value == '제품명':
            continue
        temp.append(i[2].value)

    company = list(set(temp))

    for i in company:
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
        if i[1].value == '제품명':
            continue
        try:
            sql = f"""INSERT INTO cinfo (cname, category, company) VALUES ('{i[1].value}', 4, '{i[2].value}')"""
            cursor.execute(sql)
            connect.commit()

        except Exception as e:
            print(e)
            continue

def cingr(ws):
    for i in ws.rows:
        if i[1].value == '제품명':
            continue
        try:
            temp = str(i[3].value).split(',')
            for j in temp:
                sql = f"""INSERT INTO cingr (cname , ingr) VALUES ('{i[1].value}','{j}')"""
                cursor.execute(sql)
                connect.commit()

        except Exception as e:
            print(e)
            continue

company(ws)
cinfo(ws)
cingr(ws)

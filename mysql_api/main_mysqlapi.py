from mysql.connector import MySQLConnection, Error
import requests
import numpy as np
import pandas as pd
from json.decoder import JSONDecodeError
from fastapi import FastAPI
import datetime
import pytz

product_id_file = "./product_id_file.txt"

time = pytz.timezone('Asia/Ho_Chi_Minh')

app = FastAPI()

product_url = 'https://tiki.vn/api/v2/products/{}'

def check_info_id(input):
    conn = connect()
    cursor_check = conn.cursor()
    cursor_check.execute("SELECT * FROM product_info WHERE id_product LIKE %s", (f"%{input}%",))
    info_id_sql = cursor_check.fetchall()
    cursor_check.close()
    return info_id_sql

def connect():
    """ Kết nối MySQL bằng module MySQLConnection """
    db_config = {
        'host': '192.168.80.1',
        'database': 'crawl_tiki_panther',
        'user': 'root',
        'port': '6603',
        'password': '123456'

    }
    # Biến lưu trữ kết nối
    conn = None
    try:
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            return conn
    except Error as error:
        print(error)
    return conn

def crawl_product(product_list):
    list_id_crawl = []
    for x in product_list:
        list_id_crawl.append(x)
    result = []
    headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            'referer': 'https://tiki.vn/sua-tam-duong-the-dove-pampering-care-phuc-hoi-do-am-da-kho-voi-bo-hat-mo-va-huong-hoa-vanilla-500g-p193583718.html?itm_campaign=tiki-reco_UNK_DT_UNK_UNK_tiki-listing_UNK_p-category-mpid-listing-v1_202304150600_MD_batched_PID.193583719&itm_medium=CPC&itm_source=tiki-reco&spid=193583719' 
        }
    params = {
            'platform': 'web',
            'spid': '193583719',
        }
    soluongxoa = 0
    soluongthem = 0
    soluongcu = 0
    soluongupdate =0
    soluongcu = 0

    conn = connect()
    cursor_check = conn.cursor()
    cursor_check.execute("SELECT ID_product FROM product_info ")
    list_id_sql = cursor_check.fetchall()
    cursor_check.close()
    new__list_id_sql = []
    for tup in list_id_sql:
        new__list_id_sql.append(int(tup[0]))
    for id_sql in new__list_id_sql:
        if (id_sql not in product_list):
            cursor_xoa = conn.cursor()
            cursor_xoa.execute("DELETE FROM product_info WHERE ID_product LIKE %s", (f"%{id_sql}%",))
            soluongxoa +=1
            conn.commit()
            cursor_xoa.close()
    for check in list_id_crawl:
        conn = connect()
        row = check_info_id(check)
        response = requests.get('https://tiki.vn/api/v2/products/{}'.format(check),
                                headers=headers, params=params)
        y = response.json()
        if( row == []):
            soluongthem += 1
            cursor_add = conn.cursor()
            add_news = ("INSERT  INTO `product_info`"
                    "(ID_product, Product_name, Price, Classification, Link, Brand) "
                    "VALUES (%s, %s, %s, %s, %s , %s)")
            data_news = ( y.get('id') , y.get('name'), y.get('price'),y.get('productset_group_name'),y.get('short_url'),y.get('brand').get('name'))
            #insertion
            cursor_add.execute(add_news,data_news)
            conn.commit()
            cursor_add.close()
        else:
            id_product, product_name, price, classification, link, brand = row[0][0], row[0][1], row[0][2], row[0][3], row[0][4], row[0][5]
            if (id_product ,product_name, price, classification, link, brand) != (y.get('id'),y.get('name'), y.get('price'), y.get('productset_group_name'), y.get('short_url'), y.get('brand').get('name')):
                soluongcu +=1
            else:
                soluongupdate += 1
                cursor_update = conn.cursor()
                cursor_update.execute("UPDATE `product_info` SET  Product_name = %s , Price = %s, Classification = %s, Link = %s, Brand = %s  WHERE ID_product LIKE %s",
                    ( y.get('name'), y.get('price'), y.get('productset_group_name'), y.get('short_url'), y.get('brand').get('name'), id_product)) #
                conn.commit()
                cursor_update.close()
    crawl_history = datetime.datetime.now(time)
    curor = conn.cursor()
    add_news = ("INSERT INTO `history_crawl_data` "
            "(`Date_crawl`, `Add_crawl`, `Delete_crawl`, `Update_crawl`) "
            "VALUES (%s, %s, %s, %s)")
    data_news = ( str(crawl_history) , str(soluongthem), str(soluongxoa), str(soluongupdate))
    curor.execute(add_news, data_news)
    conn.commit()

    cursor_data_crawl = conn.cursor()
    cursor_data_crawl.execute("SELECT * FROM product_info ")
    data_crawl = cursor_data_crawl.fetchall()
    cursor_data_crawl.close()

    curor.close()
    conn.close()
    return ("Add : %d , Delete : %d, Update : %d , Const : %d"  %(soluongthem,soluongxoa,soluongupdate, soluongcu)),data_crawl

@app.get("/search_db/")
def search_db(input):
    conn = connect()
    cursor_check = conn.cursor()
    cursor_check.execute("SELECT * FROM product_info WHERE Product_name LIKE %s", ('%' + str(input) + '%',))
    info_id_sql = cursor_check.fetchall()
    cursor_check.close()
    return info_id_sql

@app.get("/insert_db/")
def insert_db():
    url = 'http://api_data_crawl:8000/crawl_product_id/'
    product_list_id = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        for product in response.json():
            if product.get('id') not in product_list_id:
                product_list_id.append({'id': product.get('id')})
        write_csv_file(product_list_id, product_id_file, mode='w')
        df = read_matrix_file(product_id_file).flatten()
        result = crawl_product(df)
        return result
    except JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def write_csv_file(data_matrix, file_path, mode = 'a'):
    df = pd.DataFrame(data_matrix)
    df.to_csv(file_path, sep=',', header=None, index=None, mode=mode)

def read_matrix_file(file_path):
    f = pd.read_csv(
        file_path, sep= ',', encoding='utf-8', header=None)
    f = f.to_numpy()
    return f

@app.get("/insert_row_data/")
def crawl_product_row(id_product, product_name, price, classification, brand, link):
    try:
        conn = connect()
        cursor = conn.cursor()
        # Check if the product already exists in the table
        cursor.execute("SELECT * FROM product_info WHERE ID_product = %s", (id_product,))
        row = cursor.fetchone()
        if row is None:
            # If the product does not exist, insert a new row into the table
            cursor.execute(
                "INSERT INTO product_info (ID_product, Product_name, Price, Classification, Brand, Link) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (id_product, product_name, price, classification, brand, link)
            )
            conn.commit()
            return "Thành công thêm vào"
        else:
            # Đã tồn tại
            if (row[1], row[2], row[3], row[4], row[5]) == (product_name, price, classification, brand, link):
                return "Đã tồn tại!"
            else:
                #Thay thế giá trị cũ
                cursor.execute(
                    "UPDATE product_info "
                    "SET Product_name = %s, Price = %s, Classification = %s, Brand = %s, Link = %s "
                    "WHERE ID_product = %s",
                    (product_name, price, classification, brand, link, id_product)
                )
                conn.commit()
                return "Đã update"
    except Exception as e:
        return f"Lỗi: {str(e)}"
    finally:
        cursor.close()
        conn.close()
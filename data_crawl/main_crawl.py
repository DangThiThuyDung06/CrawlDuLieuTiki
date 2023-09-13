import requests
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

lamdepsuckhoe_page_url = "https://tiki.vn/api/personalish/v1/blocks/listings"

@app.get("/crawl_product_id/")
def crawl_product_id():
    headers = {
       'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'Accept': 'application/json, text/plain, /',
        'sec-ch-ua-mobile': '?0',
        'authorization': 'Apikey 567e8e97e3739a83267ff1c221a88f9f0460f0b76cc6ef7dc5929565d26f8f4c',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36" ,
        'sec-ch-ua-platform': '"Windows"'
    }
    params = {
        'limit': '40',
        'include': 'advertisement',
        'aggregations': '2',
        'trackity_id': 'e1157d02-7eb2-6041-d7ec-7b1cdb1c54a6',
        'category': '1520',
        'page': '1',
        'src': 'c1883',
        'urlKey':  'lam-dep-suc-khoe',
        'sort': 'newest'
    }
    product_list_id = []
    i = 1
    while(i<5):
        params['page']=i
        response = requests.get(lamdepsuckhoe_page_url, headers=headers, params=params
        )
        for response in response.json().get('data'):
            if {'id': response.get('id')} not in product_list_id:
                product_list_id.append({'id': response.get('id')})
        i += 1
    return product_list_id

@app.get("/craw_product_list/")
def crawl_product_list():
    params={
        'limit': '40',
        'include': 'advertisement',
        'aggregations': '2',
        'trackity_id': 'e1157d02-7eb2-6041-d7ec-7b1cdb1c54a6',
        'category': '1520',
        'page': '1',
        'src': 'c1883',
        'urlKey':  'lam-dep-suc-khoe',
        'sort': 'newest'
    }
    files={}
    headers = {
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'Accept': 'application/json, text/plain, /',
    'sec-ch-ua-mobile': '?0',
    'authorization': 'Apikey 567e8e97e3739a83267ff1c221a88f9f0460f0b76cc6ef7dc5929565d26f8f4c',
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36" ,
    'sec-ch-ua-platform': '"Windows"'
    }
    i = 1
    product_list = []
    while(i<3):
        params['page']=i
        response = requests.request("GET", lamdepsuckhoe_page_url, headers=headers, params=params, files=files)
        product_list.extend(response.json()['data'])
        i+=1
    return(product_list)

def write_csv_file(data_matrix, file_path, mode = 'a'):
    df = pd.DataFrame(data_matrix)
    df.to_csv(file_path, sep=',', header=None, index=None, mode=mode)


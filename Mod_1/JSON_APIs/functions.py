import numpy as np
import pandas as pd

import requests
import json
import os.path

from  keys  import  client_id, api_key


# Load csv, add new data, rewrite to csv
def data_save(parsed_results, columns, filename):
    df = pd.read_csv(filename)
    new_df = pd.DataFrame(parsed_results, columns=columns)
    combined_df = pd.concat([df, new_df], join='outer')
    combined_df.to_csv(filename, index=False)
    return None


# Yelp API call 'Business Search'
def biz_call(term, location, url_params):
    url =  'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers, params=url_params)
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print('Status Code: ' + str(response.status_code))
        return None

    
# Parse results of 'Business Search' call
def biz_parse(results):
    parsed_data = []
    for result in results['businesses']:
        data = {
            'Business Name': result['name'],
            'Business ID': result['id'],
            'Review Count': result['review_count'],
            'Business Rating': result['rating'],
        }
        if 'price' in list(result.keys()):
            data['Price Range'] = result['price']
        else:
            data['Price Range'] = np.nan
        parsed_data.append(data)
    return parsed_data


# Primary function for Yelp 'Business Search'
def yelp_biz_search(term, location, biz_file):
    filename = biz_file
    columns = ['Business Name', 'Business ID', 'Review Count',
               'Business Rating', 'Price Range']
    df = pd.DataFrame(columns=columns)
    df.to_csv(filename, index=False)
    total_results = 1
    offset = 0
    while offset < total_results and offset < 1000:
        url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': 50,
        'offset': offset
        }
        results = biz_call(term, location, url_params)
        parsed_results = biz_parse(results)
        data_save(parsed_results, columns, filename)
        total_results = results['total']
        offset += 50
    total_saved = len(pd.read_csv(filename))
    print(f'Total Results: {total_results}\nTotal Saved: {total_saved}')
    return None


# Yelp API call 'Reviews'
def reviews_call(biz_id):
    url = f'https://api.yelp.com/v3/businesses/{biz_id}/reviews'
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        return response
    else:
        print('Status Code: ' + str(response.status_code))
        return None
    
    
# Parse results of 'Reviews' call
def reviews_parse(results, biz_name, biz_id):
    parsed_data = []
    if 'reviews' in list(results.keys()):
        for result in results['reviews']:
            data = {
                'Business Name': biz_name,
                'Business ID': biz_id,
                'Review ID': result['id'],
                'Review Text': result['text'],
                'Review Rating': result['rating'],
                'Review Time': result['time_created']
            }
            parsed_data.append(data)
        return parsed_data
    else:
        return None
    
    
# Primary function for Yelp 'Reviews'
def yelp_reviews_search(biz_file, reviews_file):
    filename = reviews_file
    columns = ['Business Name', 'Business ID', 'Review ID',
               'Review Text', 'Review Rating', 'Review Time']
    df = pd.DataFrame(columns=columns)
    df.to_csv(filename, index=False)
    biz_df = pd.read_csv(biz_file)
    for biz_name, biz_id in zip(biz_df['Business Name'], biz_df['Business ID']):
        results = reviews_call(biz_id)
        if results is not None:
            parsed_results = reviews_parse(results, biz_name, biz_id)
            data_save(parsed_results, columns, filename)
        else:
            pass
    total_saved = len(pd.read_csv(filename))
    print(f'Total Saved: {total_saved}')
    return None
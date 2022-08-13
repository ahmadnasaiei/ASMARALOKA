from multiprocessing.sharedctypes import Value
# from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import re
from pprint import pprint
from csv import writer
import sqlalchemy

# GETTING TOTAL PAGINATION
url = 'https://www.edgeprop.my/jwdsonic/api/v1/property/search?=&listing_type=sale&state=Kelantan&property_type=rl&start=0&size=20'
data = requests.get(url).json()

total_pages = int(data["found"]/20)
print(total_pages)

# DATA VARIABLES
property_Title = []
property_District = []
property_State = []
property_Price = []
property_Sqft = []
property_Bedroom = []
property_Bathroom = []
property_Image = []
property_Origin_URL = []


# -------------- EDGEPROP ------------- #

# SELANGOR
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Selangor&property_type=rl&start=" + \
        str(i) + "&size=20"

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'incap_ses_1139_2031621': 'yDGNJJzY2Wn4C+x8DovOD8RrhmIAAAAA/DZCQNhXukOsUXs5uez1kg==',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1135_2031621': 'gvp+K5ND5io7w1Q6FlXAD8VrhmIAAAAA/mpF+XhKlik1qLveNsmkSw==',
        'incap_ses_1138_2031621': 'w3A/dD1YCkSI1yWEjf3KD8VrhmIAAAAAY0+/XO5EMVIBS6zHcKPYJQ==',
        'incap_ses_1128_2031621': 'ujxAai4TJ1aRNqYCvnanD8VrhmIAAAAAHAJS3R5Y/r8Z31KOYtmMZQ==',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1130_2031621': 'ilGxFaB71z0/Dzymr5GuD8ZrhmIAAAAAOacNIx7nl30Uo6rnpo5ljQ==',
        'incap_ses_1132_2031621': 'O+TOaOu+mljJWnWinKy1Dy1yhmIAAAAAufGbVCyweuuXqbMtEYle8w==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/selangor/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# JOHOR
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Johor&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'incap_ses_1139_2031621': 'yDGNJJzY2Wn4C+x8DovOD8RrhmIAAAAA/DZCQNhXukOsUXs5uez1kg==',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'incap_ses_1135_2031621': 'y0TtBv7TRxt9GVs6FlXAD3J3hmIAAAAACIOcjVtiAIqvOC+fJxPeYQ==',
        'incap_ses_1138_2031621': 'lQMdYNpwxDtFaS2Ejf3KD3J3hmIAAAAAahP5ePCQPBu5lN7rgEgFnw==',
        'incap_ses_1128_2031621': 'lFosZY1HrVtzPawCvnanD3J3hmIAAAAA+zJIGHOTfn7eOR5oyN2X7Q==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/johor/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# PENANG
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Penang&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'incap_ses_1139_2031621': 'yDGNJJzY2Wn4C+x8DovOD8RrhmIAAAAA/DZCQNhXukOsUXs5uez1kg==',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1135_2031621': 'FjFQIix/JGjk2F06FlXADw99hmIAAAAAWvAlVkx/eU1DxpT5QE908g==',
        'incap_ses_1138_2031621': '7ZacfOJ7aDt/XTCEjf3KDw99hmIAAAAAGLpyy7RYxYABl4pRh8A1PQ==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/penang/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# PERAK
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Perak&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'incap_ses_1139_2031621': 'yDGNJJzY2Wn4C+x8DovOD8RrhmIAAAAA/DZCQNhXukOsUXs5uez1kg==',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1135_2031621': 'FjFQIix/JGjk2F06FlXADw99hmIAAAAAWvAlVkx/eU1DxpT5QE908g==',
        'incap_ses_1138_2031621': '7ZacfOJ7aDt/XTCEjf3KDw99hmIAAAAAGLpyy7RYxYABl4pRh8A1PQ==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/perak/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# NEGERI SEMBILAN
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Negeri^%^20Sembilan&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'incap_ses_1139_2031621': 'yDGNJJzY2Wn4C+x8DovOD8RrhmIAAAAA/DZCQNhXukOsUXs5uez1kg==',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1135_2031621': 'FjFQIix/JGjk2F06FlXADw99hmIAAAAAWvAlVkx/eU1DxpT5QE908g==',
        'incap_ses_1138_2031621': '7ZacfOJ7aDt/XTCEjf3KDw99hmIAAAAAGLpyy7RYxYABl4pRh8A1PQ==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/negeri-sembilan/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# SABAH
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Sabah&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/sabah/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# SARAWAK
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Sarawak&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/sarawak/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# KEDAH
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Kedah&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/kedah/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# KELANTAN
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Kelantan&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'visid_incap_2031621': '7+g4gMIsTyixCmx9sZLYTJlz4WEAAAAAQUIPAAAAAAAs1Wqe++yhxnjlxOiOQS6J',
        'nlbi_2031621': 'Yr8KF4E6r3JY1TES7CcVqwAAAADOf/RXrJdbyr9HYyjVYdq6',
        'show_map_v3': 'false',
        'userFingerprint': 'KEZZfclxgGapRJFpyqkoi',
        'incap_ses_1130_2031621': 'aK+WSazrMC558mwBpJGuD5o0VGIAAAAAvj2G7qjQ3o7Ra0XJOnsQlA==',
        'incap_ses_1133_2031621': 'TDhXLy9iNlXdF0mlDzq5D2ddVGIAAAAAR6Bqf5zFUM3aGKu1pZzdJw==',
        'G_ENABLED_IDPS': 'google',
        'incap_ses_1134_2031621': 'XSMbFk1Ho2ozchhJjse8D46VVWIAAAAACji1Vn8pfOiszC2Pqxd0oQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1596584^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Tumpat^%^22^%^2C^%^22state^%^22:^%^22Kelantan^%^22^}^%^2C^{^%^22PropertyID^%^22:1550545^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Wakaf^%^20Baru^%^22^%^2C^%^22state^%^22:^%^22Kelantan^%^22^}^%^2C^{^%^22PropertyID^%^22:1533626^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Kota^%^20Bharu^%^22^%^2C^%^22state^%^22:^%^22Kelantan^%^22^}^%^2C^{^%^22PropertyID^%^22:1245916^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Kota^%^20Bharu^%^22^%^2C^%^22state^%^22:^%^22Kelantan^%^22^}^%^2C^{^%^22PropertyID^%^22:1245916^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Kota^%^20Bharu^%^22^%^2C^%^22state^%^22:^%^22Kelantan^%^22^}^]',
        'incap_ses_1139_2031621': 'jw/JMfOEYHVorP0z/orODxCiVWIAAAAANGmRC2UpGPmbJlEkl2KPkg==',
        'incap_ses_1131_2031621': '2IhLaZAxgVT7LGhXGR+yD52pVWIAAAAAyn3t6Qak2eybJWtx6v7FdA==',
        'incap_ses_1136_2031621': '/enAO/JS4lAW3A4+ieLDD56pVWIAAAAAXEynbLhWX8d3pEHRej0xsw==',
        'incap_ses_1135_2031621': 'fJidS9Jx5Bj1Tj6aClXAD+OpVWIAAAAAu4IN3IJ5LmrlrGeuDpCKrQ==',
        'incap_ses_1138_2031621': 'FISuUUzx6m7ycpM5ff3KDx2vVWIAAAAAtM2q4FhAO1hrdiXGCeFqXw==',
        'incap_ses_1128_2031621': '9dOMK2S7bSm7JYK2rXanD1azVWIAAAAAtSHauEhdDrZpPhVV/y+qRQ==',
        'incap_ses_1137_2031621': 'IwpaI4DDXB2wKfrmB3DHD+q8VWIAAAAAVi5WH/Hxezld13qZDNKBNw==',
        'incap_ses_1132_2031621': 'krf6NDK5qWZbNTUAkay1D1q/VWIAAAAA2KvFSfBfAxFQ8R+H3ylUxw==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/kelantan/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
    }

    response = requests.get(
        current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# PAHANG
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Pahang&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'incap_ses_1132_2031621': 'FrNgGhq6NRtiS3iinKy1D3J3hmIAAAAAp2oSSHhK77J8Yp9mAuDZYQ==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/pahang/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# MELAKA
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Melaka&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
        'incap_ses_1132_2031621': 'pjl8QslGlmqLHIGinKy1D62NhmIAAAAAFffRQhVAGezHZ3r8ZhhRVA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/melaka/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# TERENGGANU
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Terengganu&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
        'incap_ses_1132_2031621': 'pjl8QslGlmqLHIGinKy1D62NhmIAAAAAFffRQhVAGezHZ3r8ZhhRVA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/terengganu/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# PUTRAJAYA
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Putrajaya&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
        'incap_ses_1132_2031621': 'pjl8QslGlmqLHIGinKy1D62NhmIAAAAAFffRQhVAGezHZ3r8ZhhRVA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/putrajaya/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# PERLIS
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Perlis&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
        'incap_ses_1132_2031621': 'pjl8QslGlmqLHIGinKy1D62NhmIAAAAAFffRQhVAGezHZ3r8ZhhRVA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/perlis/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")

# LABUAN
for i in range(0, 1):

    current_pages = "https://www.edgeprop.my/jwdsonic/api/v1/property/search?&listing_type=sale&state=Labuan&property_type=rl&start=" + \
        str(i) + "&size=20"
    print(current_pages)

    cookies = {
        'nlbi_2031621': 'BUh4dt2qqlrLfz+97CcVqwAAAACI3pDnu8ohq42PO/s+Frq2',
        'visid_incap_2031621': 'd7eEj+8mRIWeCCf0VHjJhMRrhmIAAAAAQUIPAAAAAACNqf2cwlSHBzfBFQemhSMH',
        'show_map_v3': 'false',
        'userFingerprint': 'HGr2knq9B4mME8DPy09Q_',
        'incap_ses_1129_2031621': 'MmhTa1cXWQ4FIVupNQSrD8VrhmIAAAAA71agK2pVXGYc97rStYXqkA==',
        'viewed_properties': '^[^{^%^22PropertyID^%^22:1664784^%^2C^%^22PropertyIDType^%^22:^%^22m^%^22^%^2C^%^22PropertyListingType^%^22:^%^22sale^%^22^%^2C^%^22district^%^22:^%^22Shah^%^20Alam^%^22^%^2C^%^22state^%^22:^%^22Selangor^%^22^}^]',
        'incap_ses_1130_2031621': 'PXdiBPfeUH9aaUOmr5GuD995hmIAAAAA8wfvxfGlD4bcVr164UtuiQ==',
        'incap_ses_1128_2031621': 'tVvAdPQg9w0JuK4CvnanD+p8hmIAAAAAsTwm0kdj+vuZ1MZOXwg23Q==',
        'incap_ses_1139_2031621': 'okI0bUObwhJkYvx8DovODyeLhmIAAAAAvkzLMtz7VhH2vbWx5tKlKA==',
        'incap_ses_1135_2031621': 'XaNxMKqdESSya2M6FlXADyiLhmIAAAAAKYmRz7suAI80XA9OE7y1bQ==',
        'incap_ses_1138_2031621': '+pB5TljU1B8I+zWEjf3KDyeLhmIAAAAAAVs6Mesd+eO3CLhUb5pkPA==',
        'incap_ses_1132_2031621': 'pjl8QslGlmqLHIGinKy1D62NhmIAAAAAFffRQhVAGezHZ3r8ZhhRVA==',
    }

    headers = {
        'authority': 'www.edgeprop.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.edgeprop.my/buy/labuan/all-residential?page=1',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['property']

    for result in result_items:
        property_Title.append(result['title_t'])
        property_State.append(result['state_s_lower'])
        try:
            property_District.append(result['district_s_lower'])
        except:
            property_District.append('N/A')
        property_Price.append("{:,}".format(
            result['field_prop_asking_price_d']))
        try:
            property_Sqft.append(f"{result['field_prop_built_up_d']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['field_prop_bedrooms_i'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['field_prop_bathrooms_i'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(result['field_prop_images_txt'][0])
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.edgeprop.my/listing/{result['url_s']}")


# -------------- MUDAH ------------- #
next_page = 0
# SELANGOR
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=8&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# JOHOR
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=12&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# PENANG
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=3&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# PERAK
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=6&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# NEGERI SEMBILAN
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=10&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# SABAH
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=14&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# SARAWAK
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=13&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# KELANTAN
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=4&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# KEDAH
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=2&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# PAHANG
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=7&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# MELAKA
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=11&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# TERENGGANU
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=5&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# PUTRAJAYA
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=16&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# PERLIS
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=1&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")

next_page = 0
# LABUAN
for i in range(0, 1):

    current_pages = "https://search.mudah.my/v1/search?category=2040&from=" + \
        str(next_page) + "&include=extra_images^%^2Cbody&limit=40&region=17&type=sell"
    next_page = next_page + 40
    print(current_pages)

    headers = {
        'authority': 'search.mudah.my',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.mudah.my',
        'referer': 'https://www.mudah.my/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    }

    response = requests.get(current_pages, headers=headers, cookies=cookies)

    result_json = response.json()
    result_items = result_json['data']

    for result in result_items:
        property_Title.append(result['attributes']['subject'])
        property_District.append(result['attributes']['subarea_name'])
        property_State.append(result['attributes']['region_name'])
        property_Price.append("{:,}".format(result['attributes']['price']))
        try:
            property_Sqft.append(f"{result['attributes']['size']} sqft")
        except:
            property_Sqft.append('N/A')
        try:
            property_Bedroom.append(result['attributes']['rooms_id'])
        except:
            property_Bedroom.append('N/A')
        try:
            property_Bathroom.append(result['attributes']['bathroom_id'])
        except:
            property_Bathroom.append('N/A')
        try:
            property_Image.append(
                f"https://img.rnudah.com/grids{result['attributes']['image']}")
        except:
            property_Image.append(
                'https://www.dia.org/sites/default/files/No_Img_Avail.jpg')

        property_Origin_URL.append(
            f"https://www.mudah.my/{result['attributes']['subject']}.htm")


df_edge = pd.DataFrame({'property_Title': property_Title, 'property_District': property_District,
                        'property_State': property_State, 'property_Price': property_Price, 'property_Sqft': property_Sqft,
                        'property_Bedroom': property_Bedroom, 'property_Bathroom': property_Bathroom,
                        'property_Image': property_Image, 'property_Origin_URL': property_Origin_URL})

# df_edge.to_excel('edgeprop_property_listing.xlsx', index=False)

# MYSQL
engine = sqlalchemy.create_engine(
    'mysql://root:''@localhost:3307/asmaraloka')
df_edge.to_sql('scrape_property', engine, if_exists='replace')

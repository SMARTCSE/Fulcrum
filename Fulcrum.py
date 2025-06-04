import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
import pandas as pd

def abstract_cleaner(abstract):
    """Converts all the sup and sub script when passing the abstract block as html"""
    conversion_tags_sub = BeautifulSoup(str(abstract), 'html.parser').find_all('sub')
    conversion_tags_sup = BeautifulSoup(str(abstract), 'html.parser').find_all('sup')
    abstract_text = str(abstract).replace('<.', '< @@dot@@')
    for tag in conversion_tags_sub:
        original_tag = str(tag)
        key_list = [key for key in tag.attrs.keys()]
        for key in key_list:
            del tag[key]
        abstract_text = abstract_text.replace(original_tag, str(tag))
    for tag in conversion_tags_sup:
        original_tag = str(tag)
        key_list = [key for key in tag.attrs.keys()]
        for key in key_list:
            del tag[key]
        abstract_text = abstract_text.replace(original_tag, str(tag))
    abstract_text = sup_sub_encode(abstract_text)
    abstract_text = BeautifulSoup(abstract_text, 'html.parser').text
    abstract_text = sup_sub_decode(abstract_text)
    abstract_text = re.sub('\\s+', ' ', abstract_text)
    text = re.sub('([A-Za-z])(\\s+)?(:|\\,|\\.)', r'\1\3', abstract_text)
    text = re.sub('(:|\\,|\\.)([A-Za-z])', r'\1 \2', text)
    text = re.sub('(<su(p|b)>)(\\s+)(\\w+)(</su(p|b)>)', r'\3\1\4\5', text)
    text = re.sub('(<su(p|b)>)(\\w+)(\\s+)(</su(p|b)>)', r'\1\3\5\4', text)
    text = re.sub('(<su(p|b)>)(\\s+)(\\w+)(\\s+)(</su(p|b)>)', r'\3\1\4\6\5', text)
    abstract_text = re.sub('\\s+', ' ', text)
    abstract_text = abstract_text.replace('< @@dot@@', '<.')
    return abstract_text.strip()

def sup_sub_encode(html):
    """Encodes superscript and subscript tags"""
    encoded_html = html.replace('<sup>', 's#p').replace('</sup>', 'p#s').replace('<sub>', 's#b').replace('</sub>',
                                                                                                         'b#s') \
        .replace('<Sup>', 's#p').replace('</Sup>', 'p#s').replace('<Sub>', 's#b').replace('</Sub>', 'b#s')
    return encoded_html


def sup_sub_decode(html):
    """Decodes superscript and subscript tags"""
    decoded_html = html.replace('s#p', '<sup>').replace('p#s', '</sup>').replace('s#b', '<sub>').replace('b#s',
                                                                                                         '</sub>')
    return decoded_html

if __name__ == '__main__':
    all_data = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Cookie': '_gcl_au=1.1.1332669900.1719927550; _gd_visitor=b0b480ef-8981-4cbb-8ee1-b518c75b4b35; _gd_svisitor=a5c333b86c2201001a308c65ba0200002b4b1701; _mkto_trk=id:882-FQK-573&token:_mch-fulcrumapp.com-1719927555117-14560; _fbp=fb.1.1719927555851.881990897736645616; _biz_uid=3ce5aedd7d7c4ab6a04d93e10de1eaa8; _biz_flagsA=%7B%22Version%22%3A1%2C%22ViewThrough%22%3A%221%22%2C%22Mkto%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; _zitok=c4117216941bb1fef5601719980523; machete_accepted_cookies=yes; _hjSessionUser_4934015=eyJpZCI6IjZjNWJjZGI0LTBmYTEtNTFhMi04NGRiLWNkMjhiN2IyNjk4YyIsImNyZWF0ZWQiOjE3MTk5Mjc1NTYyOTMsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.465856874.1720081865; _hjSession_4934015=eyJpZCI6ImVhOThlMTc5LWNkMzUtNGNiZi04NTI5LWI0N2U4YjM4ODUzMSIsImMiOjE3MjAxNTI1ODYyNjEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; ckAttEngine={"utm_data":{"utm_campaign_org":"","utm_content_org":"","utm_term_org":"","utm_medium_org":"organic","utm_source_org":"www.google.com","timestamp_org":"7/2/2024 19:9:10","landingpage_org":"https://www.fulcrumapp.com/","referrer_org":"https://www.google.com/","utm_campaign_conv":"","utm_content_conv":"","utm_term_conv":"","utm_medium_conv":"organic","utm_source_conv":"www.google.com","timestamp_conv":"7/5/2024 9:41:50","landingpage_conv":"https://www.fulcrumapp.com/","referrer_conv":"https://www.google.com/"}}; blog_list=[{"id_post":"7629","category":null,"res_st":null,"cat_name":"","res_industry":null,"res_industry_name":"","current_page":"1"}]; data_gallery=[{"id_post":"7629","use_case":null,"res_industry":null,"res_st":null,"use_case_name":"All Categories","res_industry_name":"","current_page":"1"}]; resource_list=[{"id_post":"6244","res_type":"","res_role":"","res_industry":"","res_st":"","cat_name":"All Categories","res_industry_name":"","current_page":"1"},{"id_post":"6337","res_type":"","res_role":"","res_industry":"","res_st":"","cat_name":"All Categories","res_industry_name":"","current_page":"5"},{"id_post":"7629","res_type":"","res_role":"","res_industry":"","res_st":"","cat_name":"All Categories","res_industry_name":"","current_page":"1"}]; stories_list=[{"id_post":"7629","category":null,"current_page":"1"}]; _ga_LWQS1PT1LH=GS1.1.1720152581.6.1.1720153377.30.0.0; _ga=GA1.1.1707775085.1719927553; _biz_nA=29; _uetsid=a96f7ec039df11ef95f3839866032103; _uetvid=78f7c0f0387811ef97dc1339a813e5c5; _biz_pendingA=%5B%5D; _fulcrum_session=aHpUcG10V1ZudXFtZHNFSDUrZFlkbklxbkZocitIZHdkZHFUeVhaTjdNZlAyakxiZ0VoMHpLRnNDWTdpdGpxSWR3L3VyUUFwTDIyeUJRMGF5MWJLM3l0ckVpdGtnVzJoaGRwSThBRUVpejdhYjRCaFJSTmhsZEpnczN6NW1XYWFmZjJlTjBqcGdzTCt0MU9NK0tsa3JYbVVCalIxLzNac0tVanIzUzNOOHZBMTVRUWJydW1yQ2tQem9TNVBnQ2g4NHhWZ1lycjNvR0crWnVzUlZ5cnFQZz09LS15eUp5blZhS2FKWlcyRGlRd1hxRUNRPT0%3D--196f1d58623ee7f0635ce7999c05ed81e3fb221a',
        'Priority': 'u=0, i',
        'Referer': 'https://www.fulcrumapp.com/customer-stories/',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': 'Windows',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    urls = ['https://www.fulcrumapp.com/customer-stories/',
            'https://www.fulcrumapp.com/customer-stories/page/2/',
            'https://www.fulcrumapp.com/customer-stories/page/3/',
            'https://www.fulcrumapp.com/customer-stories/page/4/',
            'https://www.fulcrumapp.com/customer-stories/page/5/'
    ]
    for url in urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"Response from {url}:")
            #print(response.text)  # or whatever processing you need
        else:
            print(f"Failed to retrieve {url}")

        soup = BeautifulSoup(response.text, 'html.parser')
        Data = soup.find_all('div', class_='post-grid-item resource-grid-item')
        for content in Data:
            link = content.find('a').get('href')
            link_response = requests.get(link, headers=headers)
            link_content = BeautifulSoup(link_response.text, 'html.parser')
            Title = link_content.find('h1')
            Title = abstract_cleaner(Title)
            abstract1 = link_content.find('div', class_='about-customer-block-left')
            abstract2 = link_content.find('div', class_='single-resource-content')
            abstracts1 = abstract_cleaner(abstract1)
            abstracts2 = abstract_cleaner(abstract2)
            Abstracts = abstracts1 + abstracts2
            all_dict = {'TITLE': Title, 'URL': link, 'Success_Abstract': Abstracts}
            all_data.append(all_dict)
            df = pd.DataFrame(all_data)
            df.to_csv('Fulcrum_output.csv', index=False)
            print(Abstracts)



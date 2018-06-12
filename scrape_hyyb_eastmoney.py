# -*- coding: utf-8 -*-
import os,sys
import re
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
# import pandas as pd

import logging
from datetime import datetime
from utils import datetime2date


LOG_FILE = './hyyb_log.log'
HYYB_DIR = './hyyb'
HYYB_PDF_DIR = './hyyb_pdf'
EXTRACTED_HYYB_IDS_FILE = './extracted_hyyb_ids.txt'

logging.basicConfig(filename = LOG_FILE, level = logging.INFO)

# use id to identify the hyyb, return a set
def _get_extracted_hyyb_ids():
    res = set()
    if os.path.exists(EXTRACTED_HYYB_IDS_FILE):
        with open(EXTRACTED_HYYB_IDS_FILE) as f:
            for line in f:
                if line[-1]=='\n':
                    line = line[:-1]
                res.add(line) 
        return res
    else:
        print (EXTRACTED_HYYB_IDS_FILE + " does not exist!")
        return res

# EXTRACTED_HYYB_IDS is used for store all the ids, avoid duplicated extraction
EXTRACTED_HYYB_IDS = _get_extracted_hyyb_ids()



def extract_hyyb_metainfo_from_eastmoney(max_page, save2file = 'hyyb/hyyb_meta.txt'):
    with open(save2file, 'w') as fopen:
        for p in range(1,max_page+1):
            try:

                text = None
                url = 'http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&code=&sc=&ps=50&p='+str(p)+'&js=var%20vLstrieD={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&rt=50845181'
                try:
                    f_url = urlopen(url)
                except ValueError as e:
                    logging.error ("can not open url: {}".format(url))
                    continue

                fp = f_url.read()

                try: 
                    text = fp.decode('utf-8')
                except UnicodeDecodeError as e:
                    text = fp.decode('gb2312')
                    logging.info("Decode by GB2312: extract_hyyb_metainfo_from_eastmoney({})".format(url))
                except UnicodeDecodeError as e:
                    text = fp.decode('gbk')
                    logging.info("Decode by GBK: extract_hyyb_metainfo_from_eastmoney({})".format(url))
                except:
                    logging.error("unknown Error: extract_hyyb_metainfo_from_eastmoney({})".format(url))
                    continue

                if text is None:
                    continue

                idx = text.find(r'{"data"')
                hyyb_meta_infos = json.loads(text[idx:])['data']

                #TODO: use sql later

                for meta in hyyb_meta_infos:
                    x = meta + '\n'
                    fopen.write(x)
                
                logging.info("Successfully write hyyb_info on page {} into disk".format(p))
            except:
                logging.error("Fail to write hyyb_info on page {} into disk".format(p))

            if p%10==0:
                print (p, '/', max_page)

# read hyyb_meta_info from the hyyb_meta.txt file, and yield one at a time
def get_hyyb_meta_generator(filepath = 'hyyb/hyyb_meta.txt'):
    """
        input: a string 
        output: a generator yielding hyyb_meta_info every time (dict)
    """
    column_names = ['rate_change','date','id','unk1','jg','unk2','unk3','rate','unk4','title','industry','per_change', 'hyyb_url']
    with open(filepath, 'r') as f:
        for item in f:
            if item[-1] == '\n':
                item = item[:-1]

            splited_item = item.split(',')
            # splited_item[1] is date, splited_item[2] is id
            splited_item[1] = datetime2date(splited_item[1])
            hyyb_url = 'http://data.eastmoney.com/report/' + splited_item[1] + '/hy,' + splited_item[2] + '.html'
            splited_item.append(hyyb_url)
            yield dict(zip(column_names, splited_item))


# hyyb_meta_info -> save to json external file, save the pdf
def extract_hyyb(hyyb_meta_info, hyyb_dir, decode = 'GB2312'):
    """
        extract one hyyb given hyyb_meta_info
    """
    hyyb_url = hyyb_meta_info['hyyb_url']
    hyyb_id = hyyb_meta_info['id']
    industry = hyyb_meta_info['industry']
    date = hyyb_meta_info['date']
    title = hyyb_meta_info['title']

    if hyyb_id in EXTRACTED_HYYB_IDS:
        logging.info (hyyb_id + " has already been extracted")
        return

    # get the html text and parse it by bs4
    html = get_html_text(url=hyyb_url, decode=decode)
    soup = BeautifulSoup(html, 'html.parser')

    # extract keywords and newsContent
    keywords = soup.head.find('meta',{'name':'keywords'})['content']
    hyyb_content = soup.find('div', {"class":"report-content"})
    newsContent = hyyb_content.find('div', {"class":"newsContent"})
    newsContent_text = '\n'.join([s.string for s in newsContent('p') if s.string])
    d = {'keywords':keywords, 'newsContent_text':newsContent_text}

    # update hyyb_info
    hyyb_meta_info.update(d)


    # Save to json file. Add the id to EXTRACTED_HYYB_IDS
    target_dir = os.path.join(hyyb_dir, industry)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    json_filename = os.path.join(target_dir, hyyb_id + '.json')    
    

    with open(json_filename, 'w') as outfile:
        json.dump(hyyb_meta_info, outfile)
        logging.info("Successfully write to file {}".format(json_filename) )

    ## add the id to EXTRACTED_HYYB_IDS
    _add_extracted_hyyb(hyyb_id)


def _add_extracted_hyyb(hyyb_id):
    if hyyb_id in EXTRACTED_HYYB_IDS:
        print (hyyb_id + " has already been extracted.")
        return
    try:
        with open(EXTRACTED_HYYB_IDS_FILE, 'a') as f:
            f.write(hyyb_id + '\n')
            logging.info("Successfully write {} into {}".format(hyyb_id, EXTRACTED_HYYB_IDS_FILE))

        EXTRACTED_HYYB_IDS.add(hyyb_id)
    except:
        logging.error("Errors when Writing {} into {}".format(hyyb_id, EXTRACTED_HYYB_IDS_FILE))


def extract_hyybs(filepath = 'hyyb/hyyb_meta.txt', decode='GB2312'):
    hyyb_meta_info_gen = get_hyyb_meta_generator(filepath)
    count = 0
    for hyyb_meta_info in hyyb_meta_info_gen:
        try:
            logging.info("processing hyyb id: {}, title: {}".format(hyyb_meta_info['id'], hyyb_meta_info['title']))
            extract_hyyb(hyyb_meta_info, HYYB_DIR, decode=decode)
            count += 1
        except:
            logging.error("Fail to extract hyyb id: {}, title: {}".format(hyyb_meta_info['id'], hyyb_meta_info['title']))

    logging.info("Successfully extract {} hyybs".format(count))


# url -> html
def get_html_text(url, decode="GB2312"):
    """
    return a string: html text
    """
    html = None
    try: 
        with urlopen(url) as f:
            fp = f.read() # avoid http.client.IncompleteRead, 
            # https://docs.python.org/3/library/http.client.html#http.client.HTTPException
            try:
                html = fp.decode(decode)  # f.read()
            except UnicodeDecodeError as e:
                html = fp.decode('gbk')   # f.read(), the second time will read 0 bytes
                logging.info("Decode by GBK: get_html_text({})".format(url))
            except UnicodeDecodeError as e:
                html = fp.decode('utf-8')
                logging.info("Decode by UTF-8: get_html_text({})".format(url))
            except UnicodeDecodeError as e:
                logging.error('UnicodeDecodeError: ' + str(e))
            except:
                logging.error("unknown Error: get_html_text({})".format(url))
    except ValueError as e:
        logging.error ("can not open url: {}".format(url))
    return html



def check_the_id(file='hyyb/hyyb_meta.txt'):
    maps = {}
    with open(file,'r') as f:
        for line in f:
            tokens = line.split(',')
            _id = tokens[2]
            if _id not in maps:
                maps[_id] = line
            else:
                print (maps[_id])
                print (line)






# 维持,2018/5/3 0:00:18,APPIQ7SmA1hsIndustry,80000124,天风证券,3,545,增持,强于大市,机械设备行业研究周报：政策的微调降低对投资品龙头估值的抑制,机械行业,1.20
# # html -> extracted data (str)
# def extract_data_from_html(html, parser = 'html.parser', tags = None, attrs = None):
#     """
#         input: html, string
#                parser, string, can be html.parser, lxml etc.
#         output: data, string
#     """
#     soup = BeautifulSoup(html, parser)
#     data = None

#     contents = soup.findAll("script", {"type":"text/javascript", "src": None})
#     if contents is None:
#         return None

#     pattern = re.compile(r"rr\.firstInit\(({.*?})\)") # minimal match using .*?
    
#     for content in contents:
#         s = content.string
#         match = pattern.search(s)
#         if match:
#             data = match.group(1)
#             break
#     return data








# def to_df_table(data):
#     """
#         input is a json string
#         output is a df
#     """
#     d = json.loads(data)
#     if 'data' in d:
#         items = d['data']
#         items_new = [ i.split(',')for i in items]

#         column_names = ['rate_change','date','id','unk1','jg','unk2','unk3','rate','unk4','title','industry','per_change']
#         df = pd.DataFrame(items_new, columns= column_names)
#         datetime_format = '%Y/%m/%d %H:%M:%S'
#         df['date'] = df['date'].apply(lambda x: datetime.strptime(x,datetime_format).date()) 
#         df['date'] = df['date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))

#         report_url = 'http://data.eastmoney.com/report/' + df['date'] + '/hy,' + df['id'] + '.html'
#         df['report_url'] = report_url
#         return df
#     else:
#         return None




# # data -> reports
# def extract_reports(data, report_json_dir, report_pdf_dir, decode='GB2312'):
#     report_info_gen = get_report_info_generator(data)
#     count = 0
#     for hyyb_meta_info in report_info_gen:
#         logging.info("processing report id: {}, title: {}".format(hyyb_meta_info['id'], hyyb_meta_info['title']))
#         extract_report(hyyb_meta_info, report_json_dir, report_pdf_dir, decode=decode)
#         count += 1

#     logging.info("Successfully extract {} reports".format(count))


# extract the pdf_url from report_url
def get_pdf_url(hyyb_url):
    html = get_html_text(hyyb_url)
    soup = BeautifulSoup(html, 'html.parser')
    nag_text = soup(text='查看PDF原文')[0]
    pdf_url = nag_text.parent.attrs['href']
    return pdf_url

    # try to download the pdf
def extract_hyyb_pdf(pdf_url, hyyb_id, hyyb_pdf_dir):
    maybe_download_pdf(pdf_url, hyyb_id, hyyb_pdf_dir)


# get everything by using this function
# def extract_reports_from_start_page(start_url, decode="GB2312", parser = 'html.parser'):
#     logging.info("Start extracting reports from {}".format(start_url))
#     html = get_html_text(start_url, decode=decode)
#     data = extract_data_from_html(html, parser)
#     extract_reports(data, REPORT_JSON_DIR,REPORT_PDF_DIR, decode=decode)
#     logging.info("Complete extracting reports from {}".format(start_url))



if __name__ == '__main__':
    # extract_hyyb_metainfo_from_eastmoney(max_page=1352)
    logging.info("START AT TIME {}".format(datetime.now()))
    extract_hyybs()


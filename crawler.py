from flask import Flask, render_template, jsonify, request
# from flask_apscheduler import APScheduler
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

# class Config(object):
#
#     SCHEDULER_API_ENABLED = True
#
#
#
# app = Flask(__name__)
#
# app.config.from_object(Config())


#
# scheduler = APScheduler()
#
# scheduler.init_app(app)
#




# cron examples

# @scheduler.task('cron', id='job_1', second='*') # 매초 마다

# @scheduler.task('cron', id='job_1', minute='5') # 매시 5분 마다

# @scheduler.task('cron', id='job_1', hour='8') # 매일 8시

def find_keyword():
    result = list(db.programlist.find({}, {'_id' : 0}))

    for programs in result:
        program = programs['programs']
        keywords = programs['keywords'].split(',')

        for keyword in keywords:
              dcinside(program, keyword)
              fmkorea(program, keyword)
              fomos(program, keyword)
              pgr(program, keyword)
              ruliweb(program, keyword)
              dogdrip(program, keyword)



def dcinside(program, keyword):
    url = "https://search.dcinside.com/combine/q/" + keyword
    data = getData(url)
    select_list = data.select('ul.sch_result_list > li > a')

    for selected in select_list:
        soup = getData(selected['href'])

        if soup.select_one('title_subject') is not None:
            dc_post_name = soup.select_one('.title_subject').text
            dc_post_date = soup.select_one('.gall_date').text
            dc_post_reach = soup.select_one('.gall_count').text
            dc_post_url = selected['href']
        # print(dc_post_name, dc_post_date, dc_post_reach, dc_post_url)

            community_data = {
            'site': "디씨인사이드",
            'program' : program,
            'title': dc_post_name,
            'date': dc_post_date,
            'reach': dc_post_reach,
            'url': dc_post_url,
            'keyword' : keyword,
            'property': True
        }

            db.community_data.insert_one(community_data)

def fmkorea(program, keyword):
    url = "https://www.fmkorea.com/?act=IS&is_keyword=" + keyword
    data = getData(url)
    select_list = data.select('ul.searchResult > li > dl > dt > a')

    for selected in select_list:
        soup = getData("https://www.fmkorea.com/"+selected['href'])
        if soup.select_one('.np_18px_span') is not None:
            fmkorea_post_name = soup.select_one('.np_18px_span').text
            fmkorea_post_date = soup.select_one('.date.m_no').text
            fmkorea_post_reach = soup.select_one('.side.fr > span:nth-child(1) > b').text
            fmkorea_post_url = "https://www.fmkorea.com/"+selected['href']
            # print(fmkorea_post_name, fmkorea_post_date, fmkorea_post_reach, fmkorea_post_url)

            community_data = {
            'site': "에펨코리아",
            'program': program,
            'title': fmkorea_post_name,
            'date': fmkorea_post_date,
            'reach': fmkorea_post_reach,
            'url': fmkorea_post_url,
            'keyword': keyword,
            'property': True
        }
            db.community_data.insert_one(community_data)

def fomos(program, keyword):
    url = "http://www.fomos.kr/search/list?menu=talk&fword=" + keyword
    data = getData(url)
    select_list = data.select('div.result_area > div > ul > li > div.info > p.tit > a')

    for selected in select_list:
        soup = getData("http://www.fomos.kr/"+selected['href'])

        if soup.select_one('div.board_area.common_view > p.sub_tit > span:nth-child(3)') is not None:
            fomos_post_name = soup.select_one('meta[property="og:title"]')['content']
            fomos_post_date = soup.select_one('meta[property="article:published_time"]')['content']
            fomos_post_reach = soup.select_one('div.board_area.common_view > p.sub_tit > span:nth-child(3)').text
            fomos_post_url = "http://www.fomos.kr/"+selected['href']

            community_data = {
            'site': "FOMOS",
            'program': program,
            'title': fomos_post_name,
            'date': fomos_post_date,
            'reach': fomos_post_reach,
            'url': fomos_post_url,
            'keyword': keyword,
            'property': True
        }
            db.community_data.insert_one(community_data)


def pgr(program, keyword):

    url = "https://pgr21.com/pb/pb.php?id=humor&ss=on&sc=on&keyword=" + keyword
    data = getData(url)
    select_list = data.select('td.tdsub.old > a')

    idx = 0
    for selected in select_list:
        soup = getData("https://pgr21.com/" + selected['href'])

        if soup.select_one('meta[property="og:title"]')['content'] is not None:
            pgr_post_name = soup.select_one('meta[property="og:title"]')['content']
            pgr_post_date = data.select('td.tddate > span')[idx + 3].text
            pgr_post_reach = data.select('td.tdhit')[idx +3].text
            pgr_post_url = soup.select_one('meta[property="og:url"]')['content']

            community_data = {
            'site': "pgr21",
            'program': program,
            'title': pgr_post_name,
            'date': pgr_post_date,
            'reach': pgr_post_reach,
            'url': pgr_post_url,
            'keyword': keyword,
            'property': True
        }

            db.community_data.insert_one(community_data)
        idx += 1

def ruliweb(program, keyword):
    url = "https://bbs.ruliweb.com/community/board/300143?search_type=subject_content&search_key=" + keyword
    data = getData(url)
    select_list = data.select('.board_list_table > tbody > tr')

    idx = 0
    for selected in select_list:
        if idx > 2:
            link = selected.select_one('.subject a')['href']
            soup = getData(link)
            if soup.select_one('div.user_view > div:nth-child(1) > h4 > span') is not None:
                ruliweb_post_name = soup.select_one('div.user_view > div:nth-child(1) > h4 > span').text
                ruliweb_post_date = soup.select_one('meta[property="og:updated_time"]')['content']
                ruliweb_post_reach = data.select('td.hit > span')[idx-3].text
                ruliweb_post_url = link
            # print(ruliweb_post_name, ruliweb_post_date, ruliweb_post_reach, ruliweb_post_url)

                community_data = {
                'site': "루리웹",
                'program': program,
                'title': ruliweb_post_name,
                'date': ruliweb_post_date,
                'reach': ruliweb_post_reach,
                'url': ruliweb_post_url,
                'keyword': keyword,
                'property': True
            }

                db.community_data.insert_one(community_data)

        idx += 1

def dogdrip(program, keyword):
    url = "https://www.dogdrip.net/?_filter=search&act=&vid=&mid=dogdrip&category=&search_target=title_content&search_keyword=" + keyword
    data = getData(url)
    select_list = data.select('td.title > a')

    idx = 0
    for selected in select_list:
        soup = getData("https://www.dogdrip.net" + selected['href'])
        if soup.select_one('div.ed.article-head.margin-bottom-large > h4 > a') is not None:
            dogdrip_post_name = soup.select_one('div.ed.article-head.margin-bottom-large > h4 > a').text
            dogdrip_post_date = soup.select_one('div.ed.flex.flex-wrap > span:nth-child(2) > span:nth-child(2)').text
            dogdrip_post_reach = data.select('td.ed.voteNum.text-primary')[idx].text
            dogdrip_post_url = "https://www.dogdrip.net" + selected['href']
        # print(dogdrip_post_name, dogdrip_post_date, dogdrip_post_reach, dogdrip_post_url)

            community_data = {
            'site' : "DogDrip",
            'program': program,
            'title': dogdrip_post_name,
            'date': dogdrip_post_date,
            'reach': dogdrip_post_reach,
            'url': dogdrip_post_url,
            'keyword': keyword,
            'property': True
        }
            db.community_data.insert_one(community_data)

        idx += 1


def getData(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    return BeautifulSoup(data.text, 'html.parser')


find_keyword()

#
#
# if __name__ == '__main__':
#
#     scheduler.start()
#
#     app.run('0.0.0.0', port=5001, debug=True)
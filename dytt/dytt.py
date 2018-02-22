import re
import requests
from utils.TimeHelper import TimeHelper
import pymysql
import random


class MovieSky(object):
    # 静态变量
    UrlHead = 'http://www.ygdy8.net'
    PathHead = "http://www.ygdy8.net/html/gndy/oumei/list_7_182.html"

    index = 0

    # 构造函数
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3322.4 Safari/537.36'}
        db = pymysql.connect("localhost", "root", "mojinyang", "mjy_test", charset='utf8')
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS DYTT")
        sql = """CREATE TABLE DYTT (
                 Chinese_Name  MEDIUMTEXT  NOT NULL,
                 Name  MEDIUMTEXT ,
                 YEAR MEDIUMTEXT ,
                 Production_Place MEDIUMTEXT ,
                 Type MEDIUMTEXT ,
                 Language MEDIUMTEXT ,
                 Subtitle MEDIUMTEXT ,
                 IMDb MEDIUMTEXT ,
                 Douban MEDIUMTEXT ,
                 Layout MEDIUMTEXT ,
                 Size MEDIUMTEXT ,
                 FileSize MEDIUMTEXT ,
                 Time MEDIUMTEXT ,
                 Director MEDIUMTEXT ,
                 Acter MEDIUMTEXT ,
                 Link MEDIUMTEXT )"""
        cursor.execute(sql)

        self.cursor = cursor
        self.db = db

    # Start方法
    def startWork(self):
        print("工作开始..." + TimeHelper.formatTime1())
        url = MovieSky.UrlHead + '/html/gndy/oumei/list_7_1.html'
        response = requests.get(url, headers=self.headers)
        print("解析首页完成...")
        response.encoding = 'gb2312'
        html = response.text
        print("转码完成...")
        maxIndex = self.getLastPageIndex(html)
        print("总共的页数是:" + str(maxIndex))
        for index in range(1, int(maxIndex)):
            url = MovieSky.UrlHead + '/html/gndy/oumei/list_7_' + str(index) + '.html'
            print(url)
            html = self.getHtmlContent(url)
            self.getUrlMovie(html)

    def getLastPageIndex(self, html):
        pattern = re.compile("共(\d+)页")
        item = re.search(pattern, html)
        return int(item[1])

    def getUrlMovie(self, html):
        pattern = re.compile(
            "<b>[\s\S]*?<a class=ulink href=\'.*?\'[\s\S]*?<a href=\"(.*?)\".*?>(.*?)</a>[\s\S]*?</b>", re.S)
        items = re.findall(pattern, html)
        for item in items:
            url = MovieSky.UrlHead + '/' + item[0]
            html = self.getHtmlContent(url)
            if html is None:
                continue
            patternChinese_Name = re.compile(r"◎译　　名\u3000(.*?) <br />", re.S)
            patternName = re.compile(r"◎片　　名\u3000(.*?) <br />", re.S)
            patternYEAR = re.compile(r"◎年　　代\u3000(.*?) <br />", re.S)
            patternProduction_Place = re.compile(r"◎产　　地\u3000(.*?) <br />", re.S)
            patternType = re.compile(r"◎类　　别\u3000(.*?) <br />", re.S)
            patternLanguage = re.compile(r"◎语　　言\u3000(.*?) <br />", re.S)
            patternSubtitle = re.compile(r"◎字　　幕\u3000(.*?) <br />", re.S)
            patternIMDb = re.compile(r"◎IMDb评分 \u3000(.*?) <br />", re.S)
            patternDouban = re.compile(r"◎豆瓣评分\u3000(.*?) <br />", re.S)
            patternLayout = re.compile(r"◎文件格式\u3000(.*?) <br />", re.S)
            patternSize = re.compile(r"◎视频尺寸\u3000(.*?) <br />", re.S)
            patternFileSize = re.compile(r"◎文件大小\u3000(.*?) <br />", re.S)
            patternTime = re.compile(r"◎片　　长\u3000(.*?) <br />", re.S)
            patternDirector = re.compile(r"◎导　　演\u3000(.*?) <br />", re.S)
            patternActer = re.compile(r"◎主　　演\u3000(.*?)◎", re.S)
            patternLink = re.compile(r"\"(ftp:.*?)\"", re.S)

            listTmp = []
            subItemChinese_Name = re.findall(patternChinese_Name, html)
            if (len(subItemChinese_Name) > 0):
                listTmp.append(subItemChinese_Name[0])
            else:
                listTmp.append("")
            subItemName = re.findall(patternName, html)
            if (len(subItemName) > 0):
                listTmp.append(subItemName[0])
            else:
                listTmp.append("")
            subItemYEAR = re.findall(patternYEAR, html)
            if (len(subItemYEAR) > 0):
                listTmp.append(subItemYEAR[0])
            else:
                listTmp.append("")
            subItemProduction_Place = re.findall(patternProduction_Place, html)
            if (len(subItemProduction_Place) > 0):
                listTmp.append(subItemProduction_Place[0])
            else:
                listTmp.append("")
            subItemType = re.findall(patternType, html)
            if (len(subItemType) > 0):
                listTmp.append(subItemType[0])
            else:
                listTmp.append("")
            subItemLanguage = re.findall(patternLanguage, html)
            if (len(subItemLanguage) > 0):
                listTmp.append(subItemLanguage[0])
            else:
                listTmp.append("")
            subItemSubtitle = re.findall(patternSubtitle, html)
            if (len(subItemSubtitle) > 0):
                listTmp.append(subItemSubtitle[0])
            else:
                listTmp.append("")
            subItemIMDb = re.findall(patternIMDb, html)
            if (len(subItemIMDb) > 0):
                listTmp.append(subItemIMDb[0])
            else:
                listTmp.append("")
            subItemDouban = re.findall(patternDouban, html)
            if (len(subItemDouban) > 0):
                listTmp.append(subItemDouban[0])
            else:
                listTmp.append("")
            subItemLayout = re.findall(patternLayout, html)
            if (len(subItemLayout) > 0):
                listTmp.append(subItemLayout[0])
            else:
                listTmp.append("")
            subItemSize = re.findall(patternSize, html)
            if (len(subItemSize) > 0):
                listTmp.append(subItemSize[0])
            else:
                listTmp.append("")
            subItemFileSize = re.findall(patternFileSize, html)
            if (len(subItemFileSize) > 0):
                listTmp.append(subItemFileSize[0])
            else:
                listTmp.append("")
            subItemTime = re.findall(patternTime, html)
            if (len(subItemTime) > 0):
                listTmp.append(subItemTime[0])
            else:
                listTmp.append("")
            subItemDirector = re.findall(patternDirector, html)
            if (len(subItemDirector) > 0):
                listTmp.append(subItemDirector[0])
            else:
                listTmp.append("")
            subItemActer = re.findall(patternActer, html)
            if (len(subItemActer) > 0):
                listTmp.append(subItemActer[0])
            else:
                listTmp.append("")
            subItemLink = re.findall(patternLink, html)
            if (len(subItemLink) > 0):
                listTmp.append(subItemLink[0])
            else:
                listTmp.append("")
            sql = """INSERT INTO DYTT(Chinese_Name,
                     Name,YEAR ,Production_Place, Type, Language,Subtitle
                     ,IMDb,Douban,Layout,
                     Size,FileSize,Time,Director,Acter,Link)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            try:
                # 执行sql语句
                self.cursor.execute(sql, listTmp)
                # 提交到数据库执行
                self.db.commit()
            except:
                # 如果发生错误则回滚
                self.db.rollback()

    def getHtmlContent(self, url):
        headers = {
            "User-Agent": "User-Agent:Mozilla/5.0",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host': 'www.dytt8.net',
            "Connection": "keep-alive",
        }

        MovieSky.index += 1
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'gb2312'
            html = response.text
        except:
            html = None
            print(MovieSky.index, "导入失败", url)

        return html


if __name__ == "__main__":
    movie = MovieSky()
    movie.startWork()

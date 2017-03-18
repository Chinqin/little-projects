import requests
import time
import re
from lxml import etree

# loading settings
from settings import cookies

class SinaSpider:

    cookies = cookies # varibles share for all instant

    def __init__(self, target_url, sleep=False):
        # varibles unique for 
        self.target_url = target_url
        self.uid = target_url.split('/')[-1]
        self.url_add = target_url + '?page={}'
        self.max_page = self._parseFirstPage()
        self.items = []
        self.sleep = sleep # for control sleep time

    def _parseFirstPage(self):
        res = requests.get(self.target_url, cookies=cookies)
        assert res.status_code == 200, "Error: Request failed"
        selector = etree.HTML(res.content)
        # get page
        try:
            max_page = selector.xpath('//div[@id="pagelist"]/form/div/input/@value')[0]
        except IndexError:
            max_page = 1  # user has only one page           
        return max_page

    def _parsePage(self, page):
        res = requests.get(self.url_add.format(page), cookies=cookies)
        assert res.status_code == 200, "Error: Request failed"
        selector = etree.HTML(res.content)
        # get tweet
        try:
            tweets = selector.xpath('//span[@class="ctt"]')
            if page == 1:
                tweets = tweets[2:]
            tweetStampes = selector.xpath('//span[@class="ct"]')
        except etree.XPathEvalError:
            raise
        except Exception:
            raise
        items = list() 
        for tweet, tweetStamp in zip(tweets, tweetStampes):
            item = dict()
            item['tweet'] = tweet.text
            item['tweetStamp'] = tweetStamp.text
            items.append(item)
        return items

    def parsePages(self):
        for page in range(1, int(self.max_page) + 1):
            print('Parsing Page %s' % page)
            try:
                if self.sleep:
                    time.sleep(0.5) # sleep half a second after parse one page
                items = self._parsePage(page)
            except Exception as ex:
                print('Error %s: Page %s' % (ex, page))
                items = None
            if items:
                self.items.extend(items)

    def write2txt(self):
        with open('sina_{}.txt'.format(self.uid), 'a', encoding='utf-8') as file:
            for item in self.items:
                try:
                    file.write('|'.join([item['tweet'], item['tweetStamp']]) + '\n')
                except Exception as ex:
                    print("Error write item: {}".format(ex))
        print("Write file Done.")

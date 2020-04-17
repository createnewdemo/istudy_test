# -*- coding: gbk -*-
from selenium import webdriver
import time
import json
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class spider_land(object):
    def crawl_xdaili(self):
        """
        ��ȡѶ����
        :return: ����
        """
        url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=62258522ca084c20abccfb1028f6ad7e&orderno=YZ2018626596Oclk48&returnType=2&count=1'
        r = requests.get(url)
        if r:
            result = json.loads(r.text)
            proxies = result.get('RESULT')
            for proxy in proxies:
                self.proxies = {
                    'http':'http://' + proxy.get('ip') + ":"+ proxy.get('port')
                }
                print(proxies)
                #return proxies
    def get_some_infos(self):
        ip = self.proxies
        ip = ip["http"]
        print(ip)
        driver_path = r'E:\pycharm\chromediver\chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--proxy-server=%s"%ip)#����IP����
        self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)#�����ű�
        url = 'https://www.landchina.com/default.aspx?tabid=261&ComName=default'
        self.driver.get(url)#����Ҫ��ȡ��ҳ��
        #�ȶ�λ���鿴�Ƿ����Ԫ��
        WebDriverWait(self.driver, 1000).until(
            EC.presence_of_element_located(
                (By.XPATH, "//tr[@onmouseout='this.className=rowClass']")))
        infos = self.driver.find_elements_by_xpath("//tr[@onmouseout='this.className=rowClass']")#��ȡ����
        some_info=[]
        self.urls = []
        self.titles = []
        for info in infos:
            title = info.find_element_by_xpath('.//a/span').get_attribute('title') #����
            url = info.find_element_by_xpath('.//a').get_attribute('href')#����
            address = info.find_element_by_xpath('./td[2]').text
            ways = info.find_element_by_xpath('./td[4]').text#��ʽ
            time1 = info.find_element_by_xpath('./td[5]').text#����
            time2 = info.find_element_by_xpath('./td[6]').text
            self.urls.append(url)
            self.titles.append(title)
        print("��ȡһҳ��url��title�ɹ�")
        #     data = {
        #         'title': title,
        #         'url': url,
        #         'address':address,
        #         'ways': ways,
        #         'time1': time1,
        #         'time2': time2
        #     }
        #     some_info.append(data)
        # print(some_info)
    def parser_Onepage(self):
        t = 0
        try:
            for url in self.urls:
                time.sleep(2)
                self.driver.get(url)
                window_height = self.driver.get_window_size()['height']
                page_width = self.driver.execute_script('return document.documentElement.scrollWidth')  # ҳ����
                page_height = self.driver.execute_script('return document.documentElement.scrollHeight')  # ҳ��߶�
                print(page_width)
                print(page_height)
                self.driver.set_window_size(page_width, page_height)  # ���ڴ�С����
                self.driver.save_screenshot('%s.png'%self.titles[t])  # ����
                print('�ѽ�ͼ......��%d��'%t)
                t += 1
                time.sleep(2)
        except Exception as e:
            print("ʧ��ԭ��%s"%e)
    def next_page(self):
        #���Ե��  ����
        aElements = self.driver.find_elements_by_tag_name("a")
        time.sleep(2)
        names = []
        for name in aElements:
            if (name.get_attribute("href") is not None and "javascript:void" in name.get_attribute("href")):
                names.append(name)
        #print(names)
        time.sleep(2)
        self.driver.execute_script('arguments[0].click();', names[-2])
    def send_keys(self):
        time.sleep(1)
        self.driver.find_element_by_id("TAB_queryDateItem_268_1").send_keys(self.start_time)
        time.sleep(1)
        self.driver.find_element_by_id("TAB_queryDateItem_268_2").send_keys(self.over_time)
        time.sleep(1)
        check = self.driver.find_element_by_id("TAB_QueryButtonControl").click()
    def send_keys_time(self):
        self.start_time = input("�����뿪ʼʱ��:(��ʽ:2020-1-01)")
        self.over_time = input("���������ʱ��:(��ʽ:2020-1-01)")
    def run(self):
        self.send_keys_time()
        self.send_keys()
        self.crawl_xdaili()
        self.get_some_infos()
        self.next_page()
        self.parser_Onepage()

if __name__ == '__main__':
    spider = spider_land()
    spider.run()
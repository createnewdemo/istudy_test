# -*- coding: gbk -*-
from selenium import webdriver
import time
import json
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

"""
���̣�
��ҳ��-������ʱ��-����ȡһ������ҳ��ҳ����url-��������ҳ��ҳ��-����ҳ
                         *            ѭ��               *
                         *            ѭ��               *
                         ********************************
"""


class spider_land(object):
    def crawl_xdaili(self):  # ����  �ɲ���  ��Ҫʱ ���ע��
        """
        ��ȡѶ����
        :return: ����
        """
        url = 'Ѱ�����api�ӿ� �Լ�ȥѶ�������'
        r = requests.get(url)
        if r:
            result = json.loads(r.text)
            proxies = result.get('RESULT')
            for proxy in proxies:
                self.proxies = {
                    'http': 'http://' + proxy.get('ip') + ":" + proxy.get('port')
                }
                print(proxies)
                # return proxies

    def get_some_infos(self):  # ���� ��ѯʱ�� ����ҳ��
        try:
            # ip = self.proxies
            # ip = ip["http"]
            # print(ip)
            driver_path = r'E:\pycharm\chromediver\chromedriver.exe'  # ������������chromedriver.exe��Ŀ¼
            options = webdriver.ChromeOptions()
            # options.add_argument("--proxy-server=%s"%ip)#����IP����
            self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)  # �����ű�
            url = 'https://www.landchina.com/default.aspx?tabid=226'
            self.driver.get(url)  # ����Ҫ��ȡ��ҳ��
            self.send_keys_time()
            time.sleep(1)
            self.send_keys()
            time.sleep(1)
            self.driver.current_window_handle
            # print("������")
            try:
                numbers = self.driver.find_element_by_xpath("//tr/td[@class='pager']")
                number = numbers.text
                num = re.findall(r'��(\d+)ҳ', number)[0]
                # print("������2")
                return num
            except:
                print("ֻ��һҳ")
                num = 1
                return num

        except Exception as e:
            print(e)

    def info_url(self):  # ��ȡҳ���е�url����Ϣ
        try:
            self.driver.current_window_handle
            # �ȶ�λ���鿴�Ƿ����Ԫ��
            WebDriverWait(self.driver, 1000).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//tr[@onmouseout='this.className=rowClass']")))
            infos = self.driver.find_elements_by_xpath("//tr[@onmouseout='this.className=rowClass']")  # ��ȡ����
            print('��λ�ɹ�')
            some_info = []
            self.urls = []
            self.titles = []
            for info in infos:  # ѡ���Ի�ȡ����Ҫ����Ϣ
                # print('��ʼ����')
                ways = info.find_element_by_xpath('./td[4]').text  # ��ʽ
                # print(ways)
                if "��������" in ways:
                    title = info.find_element_by_xpath('.//a').text  # ����
                    # print(title)
                elif info.find_element_by_xpath('.//a').text:
                    title = info.find_element_by_xpath('.//a').text
                else:
                    title = info.find_element_by_xpath('.//a/span').get_attribute('title')  # ����
                    # print(title)
                url = info.find_element_by_xpath('.//a').get_attribute('href')  # ����
                address = info.find_element_by_xpath('./td[2]').text
                time1 = info.find_element_by_xpath('./td[5]').text  # ����
                time2 = info.find_element_by_xpath('./td[6]').text
                self.urls.append(url)
                self.titles.append(title)

            # print(len(self.urls))
            print("��ȡһҳ��url��title�ɹ�")
        except Exception as e:
            print(e)
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

    def parser_Onepage(self):  # ����һҳ
        t = 0
        try:
            self.first_window_handle = self.driver.current_window_handle
            for url in self.urls:
                self.driver.switch_to.window(self.first_window_handle)
                js = 'window.open("{}");'.format(url)
                self.driver.execute_script(js)
                handles = self.driver.window_handles
                for handle in handles:
                    if handle != self.driver.current_window_handle:
                        self.driver.switch_to.window(handle)
                        WebDriverWait(self.driver, 1000).until(
                            EC.presence_of_element_located(
                                (By.ID, "lblCreateDate")))
                        window_height = self.driver.get_window_size()['height']
                        page_width = self.driver.execute_script('return document.documentElement.scrollWidth')  # ҳ����
                        page_height = self.driver.execute_script('return document.documentElement.scrollHeight')  # ҳ��߶�
                        self.driver.set_window_size(page_width, page_height)  # ���ڴ�С����
                        u = 'F:\\pycharm_pracise\\land\\Picture\\%s.png' % self.titles[t]  # �ĵ����Լ��������ļ���
                        self.driver.get_screenshot_as_file(u)
                        # self.driver.save_screenshot('%s.png'%self.titles[t])  # ����
                        print('�ѽ�ͼ......��%d��' % t)
                        t += 1
                        # self.driver.close()
                        time.sleep(2)
                self.driver.close()
                # break   #���Է�ҳ
        except Exception as e:
            print("ʧ��ԭ��%s" % e)

    def next_page(self):  # ��ҳ
        # ���Ե��  ����
        try:
            self.driver.switch_to.window(self.first_window_handle)
            aElements = self.driver.find_elements_by_tag_name("a")
            time.sleep(2)
            names = []
            for name in aElements:
                if (name.get_attribute("href") is not None and "javascript:void" in name.get_attribute("href")):
                    names.append(name)
            # print(names)
            time.sleep(2)
            self.driver.execute_script('arguments[0].click();', names[-2])
        except Exception as e:
            print(e)

    def send_keys(self):  # ������
        self.driver.find_element_by_id("TAB_QueryConditionItem76").click()
        time.sleep(1)
        self.driver.find_element_by_id("TAB_queryDateItem_76_1").send_keys(self.start_time)
        time.sleep(1)
        self.driver.find_element_by_id("TAB_queryDateItem_76_2").send_keys(self.over_time)
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.ID, "TAB_QueryButtonControl"))
                                               )
        check = self.driver.find_element_by_id("TAB_QueryButtonControl")
        self.driver.execute_script('arguments[0].click();', check)

    def send_keys_time(self):  # ������
        self.start_time = input("�����뿪ʼʱ��(��ʽ:2020-1-1)��")
        self.over_time = input("���������ʱ��(��ʽ:2020-1-1)��")

    def run(self):  # ������
        # self.crawl_xdaili()
        num = self.get_some_infos()
        print("һ��%dҳ" % int(num))
        for i in range(int(num)):
            print("��%dҳ��ʼ����" % i)
            self.info_url()
            self.parser_Onepage()
            print("��%dҳ��������" % i)
            self.next_page()
        print("�������")


if __name__ == '__main__':
    spider = spider_land()
    spider.run()

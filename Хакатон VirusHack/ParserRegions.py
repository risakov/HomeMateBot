# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
import json

link = 'https://datalens.yandex/7o7is1q6ikh23?tab=X1&state=4073f6e411618'


class ParserRegions:
    generated_html = None
    # Получение html кода страницы

    def get_html(self, url):
        while True:
            browser = webdriver.Chrome('./chromedriver')
            browser.get(url)
            self.generated_html = browser.page_source
            browser.quit()
            if self.generated_html.find('Москва') != -1:
                break

    # Парсинг данных в словарь
    @staticmethod
    def get_data(html):
        soup = BeautifulSoup(html, 'lxml')
        names_of_regions = soup.find_all('div', class_='chartkit-table__content chartkit-table__content_undefined')
        numbers_of_regions = soup.find_all('div', class_='chartkit-table__content chartkit-table__content_number')
        data = {}
        data_top = {}
        j = 3
        for i in names_of_regions:
            data[i.text] = {}
            data[i.text]['Заражений'] = numbers_of_regions[j].text.replace(u'\xa0', '')
            data_top[i.text] = numbers_of_regions[j].text.replace(u'\xa0', '')
            data[i.text]['Выздоровлений'] = numbers_of_regions[j+1].text.replace(u'\xa0', '')
            data[i.text]['Смертей'] = numbers_of_regions[j + 2].text.replace(u'\xa0', '')
            data[i.text]['Летальность, %'] = numbers_of_regions[j + 3].text.replace(u'\xa0', '')
            j += 4

        return data, data_top

    # Метод получения данных
    def parser_region(self):
        self.get_html(link)
        data, top = self.get_data(self.generated_html)

        with open('./data/regions_data.json', 'w') as f:
            f.write(json.dumps(data))

    def parser_region_top(self):
        top, data_top = self.get_data(self.generated_html)

        l_dt = list(data_top.items())

        data_top = {}
        for i in range(10):
            data_top[l_dt[i][0]] = l_dt[i][1]

        with open('./data/regions_data_top.json', 'w') as f:
            f.write(json.dumps(data_top))




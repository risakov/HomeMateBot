import requests
from bs4 import BeautifulSoup
import datetime
import json
from googletrans import Translator

now_1 = datetime.datetime.now()
array = []
url = 'https://www.worldometers.info/coronavirus/'
trans = Translator()


class ParserCountries:
    text_of_html = None

    def get_html(self, link):
        self.text_of_html = requests.get(link).text

    @staticmethod
    def get_data(html):
        soup = BeautifulSoup(html, 'lxml')
        row_len = len(soup.find('div', class_='main_table_countries_div').find_all('tr')[2].text.split('\n')) - 2
        data = soup.find('tbody')
        data_list = data.text.split('\n')

        while data_list[1] != 'World':
            del data_list[0]

        return data_list, row_len

    @staticmethod
    def dict_of_data(data, row_len):
        n = int(len(data))
        f = ''
        i = 0
        info = {}
        info_top = {}
        while i < n-1:
            # _____СТРАНА______
            country = data[i + 1]

            info[country] = {}
            array.append(info[country])
            # _____ВСЕГО_ЗАБОЛЕВАНИЙ_____
            f = data[i + 2]
            info[country]['total_cases'] = f
            info_top[country] = int(f.replace(',', '').replace(' ', ''))

            # _____СЕГОДНЯ_ЗАРАЗИЛИСЬ_____
            f = data[i + 3]
            if f != '':
                info[country]['today_infected'] = f
            else:
                info[country]['today_infected'] = '0'

            # _____ВСЕГО_СМЕРТЕЙ_____
            f = data[i + 4]
            if f != '':
                info[country]['total_deaths'] = f
            else:
                info[country]['total_deaths'] = '0'

            # _____CЕГОДНЯ_СМЕТРЕЙ_____
            f = data[i + 5]
            if f != '':
                info[country]['today_deaths'] = f
            else:
                info[country]['today_deaths'] = '0'

            # _____ВСЕГО_ВЫЗДОРОВЕЛИ_____
            f = data[i + 6]
            if f != '':
                info[country]['total_recovered'] = f
            else:
                info[country]['total_recovered'] = '0'

            # _____ЕЩЕ_БОЛЬНЫ_____
            f = data[i + 7]
            if f != '':
                info[country]['active_cases'] = f
            else:
                info[country]['active_cases'] = '0'

            # _____СЕРЬЕЗНО_БОЛЬНЫ_____
            f = data[i + 8]
            if f != '':
                info[country]['serious_cases'] = f
            else:
                info[country]['serious_cases'] = '0'

            # _____ПРОВЕДЕННЫЕ_ТЕСТЫ_____
            f = data[i + 11]
            if f != '':
                info[country]['total_tests'] = f
            else:
                info[country]['total_tests'] = '0'

            # _____КОНТИНЕНТЫ_____
            f = data[i + 13]
            info[country]['continent'] = f

            i += row_len
        return info, info_top

    def parser(self):
        self.get_html(url)
        table, row_len = self.get_data(self.text_of_html)
        data, top_inf = self.dict_of_data(table, row_len)
        with open('./data/countries_data.json', 'w') as f:
            f.write(json.dumps(data))

    def parser_top(self):
        table, row_len = self.get_data(self.text_of_html)
        data, top_inf = self.dict_of_data(table, row_len)

        l_dt = list(top_inf.items())
        l_dt.sort(key=lambda i: i[1], reverse=True)

        data_top_eng = {}
        for i in range(10):
            data_top_eng[l_dt[i + 1][0]] = l_dt[i + 1][1]

        data_top_rus = {}
        for key, value in list(data_top_eng.items()):
            if key == "Turkey":
                data_top_rus["Турция"] = value
            else:
                key = trans.translate(key, dest="ru").text
                data_top_rus[key] = value
        with open('./data/countries_data_top.json', 'w') as f:
            f.write(json.dumps(data_top_rus))


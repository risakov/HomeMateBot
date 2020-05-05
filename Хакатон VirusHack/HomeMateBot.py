# -*- coding: utf8 -*-
# import requests
# import json
# import datetime

import io
import locale

from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
import logging.config
from ParserRegions import *
from constants import *
from parser import *

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
init_bot = Bot(token=token, timeout_s=60)

parser_regions = ParserRegions()
parser_countries = ParserCountries()


# logging.basicConfig(level=logging.DEBUG)
# logging.config.fileConfig("./logging.ini", disable_existing_loggers=False)
# log = logging.getLogger(__name__)


class HomeMateBot:
    fileId = "4g8jm000WXvWCj3Pr1bma15eb0fb381af"
    reg = None
    translated_countries = None
    countries_data = None
    regions_data = None
    countries_data_top = None
    regions_data_top = None
    time_before = datetime.datetime.now()

    def __init__(self, bot):
        with open('./data/in_regs.json') as f:
            self.reg = json.load(f)
        with open('./data/translated_countries.json') as f:
            self.translated_countries = json.load(f)
        with open('./data/countries_data.json') as f:
            self.countries_data = json.load(f)
        with open('./data/regions_data.json') as f:
            self.regions_data = json.load(f)
        with open('./data/countries_data_top.json') as f:
            self.countries_data_top = json.load(f)
        with open('./data/regions_data_top.json') as f:
            self.regions_data_top = json.load(f)

    def update(self):
        parser_countries.parser()
        parser_regions.parser_region()
        parser_countries.parser_top()
        parser_regions.parser_region_top()

        with open('./data/in_regs.json') as f:
            self.reg = json.load(f)
        with open('./data/translated_countries.json') as f:
            self.translated_countries = json.load(f)
        with open('./data/countries_data.json') as f:
            self.countries_data = json.load(f)
        with open('./data/regions_data.json') as f:
            self.regions_data = json.load(f)
        with open('./data/countries_data_top.json') as f:
            self.countries_data_top = json.load(f)
        with open('./data/regions_data_top.json') as f:
            self.regions_data_top = json.load(f)

        print("updated " + str(datetime.datetime.now()))

    @staticmethod
    def send_help(bot, from_chat, all_countries, all_regions, message_id):
        region = "Ростовская обл."
        msg = help_bot + ':\n\n' + emo_title % (all_countries["Russia"]["total_cases"],
                                                all_countries["Russia"]["total_deaths"],
                                                all_countries["Russia"]["total_recovered"],
                                                all_countries["Russia"]["today_infected"],
                                                all_countries["Russia"]["today_deaths"],
                                                all_countries["Russia"]["active_cases"],
                                                all_countries["Russia"]["serious_cases"],
                                                all_countries["Russia"]["total_tests"]) + "\n" \
                                                                                          "➡ ВВОДИМ: Ростовская область\n" \
                                                                                          "⬅ ПОЛУЧАЕМ:\n\n" + \
              region + ':\n\n' + regions % (all_regions[region]["Заражений"],
                                            all_regions[region]["Смертей"],
                                            all_regions[region]["Выздоровлений"]
                                            ) + "\n" + "Так же Вы можете получить помощь по команде /help"
        bot.edit_text(chat_id=from_chat, text=msg, inline_keyboard_markup="{}".format(json.dumps([[
            {"text": "Вернуться в начало",
             "callbackData": "toBegin"}
        ]
        ])), msg_id=message_id)

    @staticmethod
    def send_top_countries(bot, from_chat, top_countries):
        msg = 'Количество зараженных людей в странах по убыванию: \n\n'
        count = 1
        for key, value in top_countries.items():
            # Форматирование int значения с помощью locale.format_string() для добавления запятых в число по тысячам
            count_of_cases = str(locale.format_string("%d", value, grouping=True))
            msg += str(count) + ". " + key + " — " + count_of_cases + " человек\n"
            count += 1

        bot.send_text(chat_id=from_chat,
                      text=msg, inline_keyboard_markup="{}".format(json.dumps([
                [
                    {"text": "Источник",
                     "url": "https://datalens.yandex/7o7is1q6ikh23?tab=X1&state=4073f6e411618"}
                ],
                [
                    {"text": "GIF-график истории заражения",
                     "callbackData": "gifGeneralCasesId", "style": "primary"}
                ],
                [
                    {"text": "Вернуться в начало",
                     "callbackData": "toBegin"}
                ]
            ])))

    @staticmethod
    def send_russian_detail_message(bot, from_chat, region, statistics):
        all_cases = int(statistics[region]["Заражений"])
        death_cases = int(statistics[region]["Смертей"])
        recovered_cases = int(statistics[region]["Выздоровлений"])
        # Форматирование int значения с помощью locale.format_string() для добавления запятых в число по тысячам
        msg = region + ':\n\n' + regions % (locale.format_string("%d", all_cases, grouping=True),
                                            locale.format_string("%d", death_cases, grouping=True),
                                            locale.format_string("%d", recovered_cases, grouping=True))
        bot.send_text(chat_id=from_chat,
                      text=msg, inline_keyboard_markup="{}".format(json.dumps([
                [
                    {"text": "Источник",
                     "url": "https://datalens.yandex/7o7is1q6ikh23?tab=X1&state=4073f6e411618"}
                ],
                [
                    {"text": "Вернуться в начало",
                     "callbackData": "toBegin"}
                ]
            ])))

    @staticmethod
    def send_top_regions(bot, from_chat, regions_top):
        msg = 'Количество зараженных людей в регионах России по убыванию: \n\n'
        count = 1
        for key, value in regions_top.items():
            # Форматирование int значения с помощью locale.format_string() для добавления запятых в число по тысячам
            count_of_cases = str(locale.format_string("%d", int(value), grouping=True))
            msg += str(count) + ". " + key + " — " + count_of_cases + " человек\n"
            count += 1

        bot.send_text(chat_id=from_chat,
                      text=msg, inline_keyboard_markup="{}".format(json.dumps([
                [
                    {"text": "Источник",
                     "url": "https://datalens.yandex/7o7is1q6ikh23?tab=X1&state=4073f6e411618"}
                ],
                [
                    {"text": "Вернуться в начало",
                     "callbackData": "toBegin"}
                ]
            ])))

    # Метод для отправки информации по стране
    @staticmethod
    def send_country_message(bot, from_chat, country, statistics, translated):
        if country != "World" and country != "Total:":
            msg = translated[country] + ':\n\n' + emo_title % (statistics[country]["total_cases"],
                                                               statistics[country]["total_deaths"],
                                                               statistics[country]["total_recovered"],
                                                               statistics[country]["today_infected"],
                                                               statistics[country]["today_deaths"],
                                                               statistics[country]["active_cases"],
                                                               statistics[country]["serious_cases"],
                                                               statistics[country]["total_tests"]
                                                               )
            bot.send_text(chat_id=from_chat,
                          text=msg, inline_keyboard_markup="{}".format(json.dumps([
                    [
                        {"text": "Источник", "url": "http://www.worldometers.info/coronavirus/"}
                    ],
                    [
                        {"text": "Вернуться в начало",
                         "callbackData": "toBegin"}
                    ]
                ])))
        else:
            msg = translated[country] + ':\n\n' + emo_title_world % (statistics[country]["total_cases"],
                                                                     statistics[country]["total_deaths"],
                                                                     statistics[country]["total_recovered"],
                                                                     statistics[country]["today_infected"],
                                                                     statistics[country]["today_deaths"],
                                                                     statistics[country]["active_cases"],
                                                                     statistics[country]["serious_cases"]
                                                                     )
            bot.send_text(chat_id=from_chat, text=msg, inline_keyboard_markup="{}".format(json.dumps([
                [
                    {"text": "Источник", "url": "http://www.worldometers.info/coronavirus/"}
                ],
                [
                    {"text": "Вернуться в начало",
                     "callbackData": "toBegin"}
                ]
            ])))

    @staticmethod
    def to_begin(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=to_begin, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Акутальная информация", "callbackData": "actualInfoId", "style": "primary"}
            ],
            [
                {"text": "Что мне делать?", "callbackData": "whatToDoId", "style": "primary"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def start(bot, from_chat):
        bot.send_text(chat_id=from_chat, text=start, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Акутальная информация", "callbackData": "actualInfoId", "style": "primary"}
            ],
            [
                {"text": "Что мне делать?", "callbackData": "whatToDoId", "style": "primary"}
            ]
        ])))

    @staticmethod
    def send_start(bot, from_chat):
        bot.send_text(chat_id=from_chat, text=to_begin, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Акутальная информация", "callbackData": "actualInfoId", "style": "primary"}
            ],
            [
                {"text": "Что мне делать?", "callbackData": "whatToDoId", "style": "primary"}
            ]
        ])))

    @staticmethod
    def edit_what_to_do(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=what_to_do, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Беспокоит немного...", "callbackData": "worriedId", "style": "attention"}
            ],
            [
                {"text": "А чем заняться?", "callbackData": "thingsToDo", "style": "primary"}
            ],
            [
                {"text": "Назад", "callbackData": "backId1"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_worried(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=problems, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Психологического характера", "callbackData": "psychologicalId", "style": "attention"}
            ],
            [
                {"text": "Физического характера", "callbackData": "physicalId", "style": "attention"}
            ],
            [
                {"text": "Источник", "url": "https://www.minobrnauki.gov.ru/ru/press-center/card/?id_4=2504"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ],
            [
                {"text": "Назад", "callbackData": "backId2"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_psychological(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=choice, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Тревога, страх, паника", "callbackData": "fearId", "style": "attention"}
            ],
            [
                {"text": "Социальная изоляция", "callbackData": "isolationId", "style": "attention"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ],
            [
                {"text": "Назад", "callbackData": "backId3"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_fear(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=fear, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Источник",
                 "url": "https://www.minobrnauki.gov.ru/ru/press-center/card/?id_4=2504"}
            ],
            [
                {"text": "Назад", "callbackData": "backId4"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_isolation(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=isolation, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Источник",
                 "url": "https://www.minobrnauki.gov.ru/ru/press-center/card/?id_4=2504"}
            ],
            [
                {"text": "Назад", "callbackData": "backId4"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_physical(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=choice, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Сидячий образ жизни", "callbackData": "sedentaryLifeId", "style": "attention"}
            ],
            [
                {"text": "Неправильное питание", "callbackData": "wrongFoodId", "style": "attention"}
            ],
            [
                {"text": "Назад", "callbackData": "backId3"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_sedentary_life(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=sedentary_life, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Источник",
                 "url": "https://www.belnovosti.by/krasota-i-zdorove/kak-pobedit-sidyachiy-obraz-zhizni-"
                        "vo-vremya-pandemii-covid-19-v-voz-perechislili"}
            ],
            [
                {"text": "Назад", "callbackData": "backId5"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_wrong_food(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=wrong_food, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Источник",
                 "url": "https://www.oblgazeta.ru/society/107637/"}
            ],
            [
                {"text": "Назад", "callbackData": "backId5"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_things_to_do(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=things_to_do, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Фильмы", "callbackData": "filmsId", "style": "primary"},
                {"text": "Стримы", "callbackData": "streamsId", "style": "primary"},
                {"text": "Музыка", "callbackData": "musicId", "style": "primary"}
            ],
            [
                {"text": "Халява", "callbackData": "filmsId", "style": "primary"},
                {"text": "Курсы", "callbackData": "streamsId", "style": "primary"},
                {"text": "Работа", "callbackData": "jobId", "style": "primary"}
            ],
            [
                {"text": "Сериалы", "callbackData": "seriesId", "style": "primary"},
                {"text": "Лайфхаки", "callbackData": "lifehacksId", "style": "primary"},
                {"text": "Советы", "callbackData": "advicesId", "style": "primary"}
            ],
            [
                {"text": "Групповой просмотр фильмов", "callbackData": "filmsId", "style": "primary"},
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ],
            [
                {"text": "Назад", "callbackData": "backId6"}
            ]

        ])), msg_id=message_id)

    @staticmethod
    def edit_films(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=films, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "250 фильмов(IMDB)",
                 "url":"https://www.imdb.com/chart/top/",
                 "style": "primary"}
            ],
            [
                {"text": "250 фильмов(Кинопоиск)",
                 "url": "https://www.kinopoisk.ru/lists/top250/?tab=all",
                 "style": "primary"}
            ],
            [
                 {"text": "BadComedian плейлист",
                  "url": "https://www.youtube.com/watch?v=YAdIiPaf3_0&list=PL471DC4C544B5A1B9",
                  "style": "primary"}
            ],
            [
                 {"text": "Антон Долин: что смотреть сейчас",
                  "url": "https://www.youtube.com/watch?v=YAdIiPaf3_0&list=PL471DC4C544B5A1B9",
                  "style": "primary"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ],
            [
                {"text": "Назад", "callbackData": "backId7"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_advices(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=advices, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ],
            [
                {"text": "Назад", "callbackData": "backId7"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_streams(bot, from_chat, message_id):
        bot.edit_text(chat_id=from_chat, text=streams, inline_keyboard_markup="{}".format(json.dumps([
            [
                {"text": "Twitch",
                 "url": "https://www.twitch.tv/",
                 "style": "primary"}
            ],
            [
                {"text": "Youtube Live Now",
                 "url": "https://www.youtube.com/watch?v=FgWhpLxpiSg&list=PLU12uITxBEPFb0yuTkLH2tu8j5SVx1YaA",
                 "style": "primary"}
            ],
            [
                 {"text": "GoodGame",
                  "url": "https://goodgame.ru/streams/",
                  "style": "primary"}
            ],
            [
                {"text": "Вернуться в начало",
                 "callbackData": "toBegin"}
            ],
            [
                {"text": "Назад", "callbackData": "backId7"}
            ]
        ])), msg_id=message_id)

    @staticmethod
    def edit_before(bot, from_chat, button_id, message_id):
        if button_id == "backId1":
            home_mate_bot.to_begin(bot=bot, from_chat=from_chat, message_id=message_id)
        if button_id == "backId2":
            home_mate_bot.edit_what_to_do(bot=bot, from_chat=from_chat, message_id=message_id)
        if button_id == "backId3":
            home_mate_bot.edit_worried(bot=bot, from_chat=from_chat, message_id=message_id)
        if button_id == "backId4":
            home_mate_bot.edit_psychological(bot=bot, from_chat=from_chat, message_id=message_id)
        if button_id == "backId5":
            home_mate_bot.edit_physical(bot=bot, from_chat=from_chat, message_id=message_id)
        if button_id == "backId6":
            home_mate_bot.edit_what_to_do(bot=bot, from_chat=from_chat, message_id=message_id)
        if button_id == "backId7":
            home_mate_bot.edit_things_to_do(bot=bot, from_chat=from_chat, message_id=message_id)

    @staticmethod
    def send_photo_net(bot, from_chat, url_p):
        rem_img = requests.get(url_p)
        photo = io.BytesIO(rem_img.content)
        bot.send_file(chat_id=from_chat, file=photo)

    def message_cb(self, bot, event):
        time_now = datetime.datetime.now()
        from_chat = event.from_chat

        if self.time_before.hour < time_now.hour or self.time_before.day < time_now.day or \
                self.time_before.month < time_now.month or self.time_before.year < time_now.year:
            self.time_before = time_now
            self.update()
        # Переменная индекса для запоминания позиции строки в массиве сокращений регионов
        index = -1
        # Флаг, содержащий информацию о том, что сообщение уже отправлено

        message = event.text.lower().replace(" ", "")

        if message == "/start":
            self.start(bot=bot, from_chat=from_chat)
            return

        # Прогон по словарю переведенных стран
        for key, value in self.translated_countries.items():
            # Проверка сообщения от пользователя на соответствие зн2ачению из словаря переведенных стран
            if message == value.lower().replace(" ", ""):
                self.send_country_message(bot=bot, from_chat=from_chat, country=key,
                                          statistics=self.countries_data,
                                          translated=self.translated_countries)
                return

        # Проверка вхождения подстроки(сокращения региона) в сообщение от пользователя
        for i in range(len(self.reg)):
            if self.reg[i] in message:
                index = i
                break

        for key in self.regions_data:
            # Если индекс изменился
            if index != -1:
                # Проверка на вхождения подстроки(сокращения региона)
                # в ключе словаря спарсенных данных по России
                if self.reg[index] in key.lower().replace(" ", ""):
                    if message == "омская" or message == "омск":
                        self.send_russian_detail_message(bot=bot, from_chat=from_chat, region="Омская обл.",
                                                         statistics=self.regions_data)
                    elif message == "томская" or message == "томск":
                        self.send_russian_detail_message(bot=bot, from_chat=from_chat, region="Томская обл.",
                                                         statistics=self.regions_data)
                    else:
                        self.send_russian_detail_message(bot=bot, from_chat=from_chat, region=key,
                                                         statistics=self.regions_data)
                    return

        if message == "топмир" or message == "топмира":
            self.send_top_countries(bot=bot, from_chat=from_chat, top_countries=self.countries_data_top)
            return

        if message == "топроссия" or message == "топроссии":
            self.send_top_regions(bot=bot, from_chat=from_chat, regions_top=self.regions_data_top)
            return

        if message == "/help":
            self.send_help(bot=bot, from_chat=from_chat, all_countries=self.countries_data,
                           all_regions=self.regions_data)
            return

        bot.send_text(chat_id=from_chat, text="Неверный формат ввода.\nВведите '/help' ,"
                                              " если у Вас возникли трудности.")


def buttons_answer_cb(bot, event):
    from_chat = event.data['message']['chat']['chatId']
    button_id = event.data['callbackData']
    message_id = event.data['message']['msgId']

    bot.answer_callback_query(
        query_id=event.data["queryId"],
        text=""
    )

    if button_id == "toBegin":
        home_mate_bot.to_begin(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "russianButtonId":
        home_mate_bot.start(bot=bot, from_chat=from_chat)

    if button_id == "actualInfoId":
        home_mate_bot.send_help(bot=bot, from_chat=from_chat,
                                all_countries=home_mate_bot.countries_data,
                                all_regions=home_mate_bot.regions_data, message_id=message_id)

    if button_id == "whatToDoId":
        home_mate_bot.edit_what_to_do(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "worriedId":
        home_mate_bot.edit_worried(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "psychologicalId":
        home_mate_bot.edit_psychological(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "fearId":
        home_mate_bot.edit_fear(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "isolationId":
        home_mate_bot.edit_isolation(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "physicalId":
        home_mate_bot.edit_physical(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "sedentaryLifeId":
        home_mate_bot.edit_sedentary_life(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "wrongFoodId":
        home_mate_bot.edit_wrong_food(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "thingsToDo":
        home_mate_bot.edit_things_to_do(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "filmsId":
        home_mate_bot.edit_films(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "streamsId":
        home_mate_bot.edit_streams(bot=bot, from_chat=from_chat, message_id=message_id)

    if button_id == "advicesId":
        home_mate_bot.edit_advices(bot=bot, from_chat=from_chat, message_id=message_id)

    if "back" in button_id:
        home_mate_bot.edit_before(bot=bot, from_chat=from_chat, button_id=button_id, message_id=message_id)
    if button_id == "gifGeneralCasesId":

        bot.send_file(chat_id=from_chat, file_id=home_mate_bot.fileId)
        home_mate_bot.send_start(bot=bot, from_chat=from_chat)


home_mate_bot = HomeMateBot(init_bot)
init_bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))
init_bot.dispatcher.add_handler(MessageHandler(callback=home_mate_bot.message_cb))
init_bot.start_polling()
init_bot.idle()


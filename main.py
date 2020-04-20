from selenium import webdriver
import datetime, time

from sorting import Sort
from my_logging import Log


class Parse:
    def __init__(self):
        # Иницилизация переменных
        firefox_driver = 'drivers'
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        self.dr = webdriver.Firefox(firefox_driver, options=options, service_log_path='log\\log_web_drivers.log')
        self.mass = []

    def start(self):
        print('-=Start parse=- {}'.format(self.date_time()))
        url = 'https://edadeal.ru/sankt-peterburg/retailers/5ka'
        Log().write_log(['info', 'Start Parse'] )
        Log().write_log(['info', 'Url Parse:'.format(url)])
        self.dr.get(url)
        self.dr.implicitly_wait(1)
        self.next_page_parse()
        print('End parse {}'.format(self.date_time()))
        Log().write_log(['info', 'End Parse'])
        self.dr.close()

    def parse(self, elements):
        i = 0
        for el in elements:
            i += 1
            # print(el)
            date = el.find_element_by_class_name('b-offer__dates').text
            name = el.find_element_by_class_name('b-offer__description').text
            new_price = el.find_element_by_class_name('b-offer__price-new').text
            try:
                shop = el.find_element_by_class_name('b-offer__retailer-icon').get_attribute('title')
            except Exception as e:
                shop = 'Нет магазина'
            try:
                old_price = el.find_element_by_class_name('b-offer__price-old').text
            except Exception as e:
                # Вывод ошибки
                # print(e)
                old_price = 'Нет старой цены'

            item = {'date': date, 'name': name, 'new_price': new_price, 'old_price': old_price, 'shop': shop}
            #print(item)
            self.mass.append(item)

    def next_page_parse(self):
        i = 1
        while True:
            print('Page {}'.format(i))
            Log().write_log(['info', 'Page {}'.format(i)])
            # Проверка на наличие элемента. Если p-offers__offers, значит все скидки, иначе(p-retailer__offer) магазин.
            try:
                Log().write_log(['info', 'Parse all catalog'])
                self.dr.find_element_by_class_name('p-offers__offers')
                body_elem = self.dr.find_elements_by_css_selector('a.p-offers__offer')
            except Exception as e:
                Log().write_log(['info', 'Parse only catalog'])
                body_elem = self.dr.find_elements_by_css_selector('a.p-retailer__offer')
            # Отправляем все элементы в функцию для парса
            self.parse(body_elem)
            el = self.dr.find_elements_by_css_selector('div.b-pagination__root')
            try:
                for ii in el:
                    ii.find_element_by_class_name('b-pagination__next').click()
                time.sleep(0.7)
                # self.dr.implicitly_wait(5)
                i += 1
                print(len(self.mass))
                if len(self.mass) >= 30:
                    # print(self.mass)
                    # записываем и обнуляем значения
                    print('Записываю и обнуляю массив')
                    Sort().sort(self.mass)
                    Log().write_log(['info', 'Send data to sort and NULL massive'])
                    self.mass = []

            except Exception as e:
                #   Вывод ошибки
                print(e)
                Log().write_log(['info', e])
                break

    @staticmethod
    def date_time():
        date_time = datetime.datetime.now().strftime('%d_%m_%Y %H_%M_%S_[%f]')
        return date_time


if __name__ == '__main__':
    Parse().start()

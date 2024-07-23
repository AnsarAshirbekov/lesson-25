# а) Получить погоду в Астане с статического сайта погоды, используя
# string.split()
# б) Получить погоду в Астане с статического сайта погоды, используя bs4

# Мне не удалось найти статический сайт с погодой, где бы был нормальный HTML-код, я нашел сайт https://wttr.in/
# но там HTML-код какой-то странный, там много одинаковых классов с разным содержанием, и при выводе полностью 
# этого кода в консоль выводится не просто HTML-код, а полностью страница как в браузере.
# Кароче, я еще там немного покапался и нашел такую страницу с одним единственным тэгом со значением температуры в Астане,
# это явно не подходит для парсинга, но что поделать, нормальных статистических сайтов с погодой нет :(

# import requests

# url = "https://wttr.in/Astana?format=3"

# response = requests.get(url)

# weather = response.text
# print(f"Погода: {weather}")

# # используем string.split() как требовалось в условии задачи
# parts = weather.split()    
# location = parts[0]
# temperature = parts[2] # 1-й элемент там какое-то облачко) 
    
# print(f"Локация: {location}")
# print(f"Температура: {temperature}")


# Далее сказано что нужно опять использовать статический сайт с погодой, но таких сайтов практически нет, так что будем
# использовать динамические, как например всем известный gismeteo, и еще библиотеку selenium для парсинга динамических
# сайтов
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Создаем объект вебдрайвера браузера Chrome
chrome = webdriver.Chrome()
# Передадим url со страницей погоды
url = "https://www.gismeteo.kz/weather-astana-5164/10-days/"
# Делаем запрос со страницы
chrome.get(url)
# Дадим какое-то время для открытия страницы и считывания HTML-кода с нее 
time.sleep(5)
# Считываем HTML-код 
html = chrome.page_source
# Создаем объект для парсинга HTML-кода
soup = BeautifulSoup(html, 'html.parser')
# Вытаскиваем все элементы класса 'maxt', который содержит значение максимальной температуры за какой-то определенный день
weather_elements = soup.find_all(class_ = 'maxt')
# Теперь нужно вывести все значения температур в консоль
for w in weather_elements:
    # но в том сайте в HTML-коде в классах 'maxt' содержатся не только значения температур, там еще есть какие-то непонятные
    # числа, которые нам не нужны. Нам нужно вывести только те, которые содержат перед собой + или -, что будет будет явно
    # указывать на то, что это температура  
    if '+' in w.text or '-' in w.text:
        print(w.text)
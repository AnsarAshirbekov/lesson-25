# а) Загрузите циклом 10 рандомных картинок с сайта используя библиотеку
# requests, затем aiohttp.
# б) Сохраните их в разные папки циклом.

from bs4 import BeautifulSoup

# import requests

import os

# Выясняем директорию текущей папки
current_dir = os.getcwd()
# Делаем запрос с сайта
# response = requests.get("https://books.toscrape.com/")
# Из полученного запроса составляем html код в виде текста  
# html = response.text
# Создаем объект класса BeautifulSoup, которому передаем наш html-код и применяем к нему встроенный парсер html.parser
# bs4 = BeautifulSoup(html, 'html.parser')
# К этому объекту применяем метод .find_all(), находим все тэги класса 'thumbnail' и записываем их в переменную picture_tags
# picture_tags = bs4.find_all(class_='thumbnail')
# Запускаем цикл из 10-ти итераций
# for i in range(10):
      # Задаем имя для новой папки
#     folder_name = f'Picture{i} folder'
      # Обращаемся к элементу переменной picture_tags по i и получаем значение атрибута src из каждого элемента (тэга)
#     picture_tag = picture_tags[i].get('src')
      # Задаем путь для новой папки
#     path = os.path.join(current_dir, folder_name)
      # Создаем новую папку, передав ей ее путь
#     os.makedirs(path, exist_ok=True)
      # Задаем имя для файла (картинки)
#     file_name = f'picture{i}.png'
      # Создаем путь для файла, что бы он находился в новой папки
#     file_path = os.path.join(path, file_name)
      # Делаем запрос к сайту, передав ему тэги картинок из атрибутов src
#     picture_response = requests.get(f"https://books.toscrape.com/{picture_tag}")
      # Создаем файл по уже заданному пути
#     with open(file_path, 'wb') as file:
          # Скачиваем картинку из запроса с помощью 'wb' и атрибута .content
#         file.write(picture_response.content)


# Теперь необходимо проделать все это с помощью aiohttp
import aiohttp
import asyncio
import aiofiles

# Создаем асинхронную функцию для получение тэгов картинок с сайта по некоторому url
async def fetch_data(url):
    # Так как мы будем делать несколько запросов к сайту, лучше создать сессию запросов, вместо одного единственного запроса
    # "async with aiohttp.request('GET', url) as response" как здесь из задачи предыдущей домашки. 
    async with aiohttp.ClientSession() as session:
        # а уже в сессии запросов мы будем делать один запрос
        async with session.get(url) as response:
            # Для получения html-кода в виде текста уже используем метод .text() а не атрибут .text , потому что нам здесь
            # нужно поставить await, чтобы удовлетворить требованиям асинхронности, а он не ставится перед атрибутами 
            html = await response.text()
            bs4 = BeautifulSoup(html, 'html.parser')
            # Возвращаем все тэги картинок
            return bs4.find_all(class_='thumbnail')  # Этот вызов может быть выполнен синхронно, так как это не IO операция

# Создаем асинхронную функцию для создания папок, создания задач по скачиванию картинок и запуску этих задач    
async def save_files(data):
    # Открываем асинхронную сессию для запросов
    async with aiohttp.ClientSession() as session:
        # Далее чтобы все работало асинхронно, быстро и красиво, нужно создать список задач. Задачи часто используются 
        # в асинхронном программировании. Задача - это обертка вокруг корутины, управляемая asyncio. Она позволяет 
        # асинхронно выполнять корутину и предоставляет средства для управления её выполнением. Корутина - это 
        # асинхронная функция, которую можно поставить на паузу await и продолжить позже. 
        # Здесь нам нужно создать такую задачу, которая будет скачивать картинки по запросу из сессии по заданному url 
        # и сохранять ее в своей папке.
        tasks = []
        # Далее проделываем почти тоже самое, что и было с requests
        for i in range(10):
            folder_name = f'Picture{i} folder'
            # Вместо picture_tags здесь data из функции fetch_data
            picture_tag = data[i].get('src')
            path = os.path.join(current_dir, folder_name)
            os.makedirs(path, exist_ok=True)
            file_name = f'picture{i}.png'
            file_path = os.path.join(path, file_name)
            # Создаем url для картинки
            picture_url = f"https://books.toscrape.com/{picture_tag}"
            # В список задач добавляем корутины (асинхронные функции), которые будут написаны чуть ниже
            tasks.append(save_file(session, picture_url, file_path))
        # Далее вызываем функцию gather из asyncio, которая асинхронно запускает выполнение задач (распакованных *)
        await asyncio.gather(*tasks)

# Создаем корутину для скачивания картинок и добавления их в папки, передав ей аргументы, полученные из функции выше
async def save_file(session, picture_url, file_path):
    # Здесь стоит заметить, что запрос из сессии происходит только здесь, а не в той функции, где она была открыта. 
    # Это позволяет организовать код так, что все HTTP-запросы и операции ввода-вывода выполняются параллельно и 
    # эффективно.
    async with session.get(picture_url) as response:
        content = await response.read()  # Асинхронное чтение контента
        async with aiofiles.open(file_path, 'wb') as file:
            await file.write(content)  # Асинхронная запись файла

async def main():
    url = "https://books.toscrape.com/"
    data = await fetch_data(url)
    await save_files(data)

if __name__ == "__main__":
    asyncio.run(main())
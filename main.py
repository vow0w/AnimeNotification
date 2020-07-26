import time
import requests
import vk_api
from bs4 import BeautifulSoup
from vk_api.utils import get_random_id
import os


def parse():
    request = requests.get("https://animevost.am/")
    soup = BeautifulSoup(request.content, 'html.parser')
    name = soup.select('#dle-content > div:nth-child(1) > div.shortstoryHead > h2 > a')
    name = str(name[0].text)
    image = soup.find_all('img', attrs={"class": "imgRadius"})
    image = "https://animevost.am" + image[0]['src']
    return name + "\n" + image


def start():
    token = os.environ['VK_TOKEN']
    vk = vk_api.VkApi(token=token)
    api = vk.get_api()

    print("Бот запущен")
    api.messages.send(user_id=186003041, message="ABot включён!", random_id=get_random_id())
    while True:
        read = open('notification', 'r')
        message = read.read()
        read.close()
        pars = parse()
        if pars != message:
            write = open('notification', 'w')
            write.write(pars)
            write.close()
            api.messages.send(user_id=186003041, message=pars, random_id=get_random_id())
            print("Сообщение отправлено: \n" + pars + "\n_________________________________________________________")

        time.sleep(120)


if __name__ == "__main__":
    start()

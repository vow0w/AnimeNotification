import time
import requests
import vk_api
from bs4 import BeautifulSoup
from vk_api.utils import get_random_id
import os


def parse():
    request = requests.get("https://www19.gogoanime.io/")
    soup = BeautifulSoup(request.content, 'html.parser')
    name = soup.select('#load_recent_release > div.last_episodes.loaddub > ul > li:nth-child(1) > p.name > a')
    name = str(name[0].text)
    episode = soup.select('#load_recent_release > div.last_episodes.loaddub > ul > li:nth-child(1) > p.episode')
    episode = str(episode[0].text)
    image = soup.select('#load_recent_release > div.last_episodes.loaddub > ul > li:nth-child(1) > div > a > img')
    image = str(image[0]['src'])

    return name + "\n" + episode + "\n" + image


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

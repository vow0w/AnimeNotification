import time
import requests
import vk_api
from bs4 import BeautifulSoup
from vk_api.utils import get_random_id
import os

token = os.environ['VK_TOKEN']
vk = vk_api.VkApi(token=token)
api = vk.get_api()

user = [186003041, 187419279, 288925718]


def parse():
    request = requests.get("https://animevost.am/")
    soup = BeautifulSoup(request.content, 'html.parser')
    name = soup.select('#dle-content > div:nth-child(1) > div.shortstoryHead > h2 > a')
    name = str(name[0].text)
    image = soup.find_all('img', attrs={"class": "imgRadius"})
    image = "https://animevost.am" + str(image[0]['src'])
    return [name, image]


def photos():
    upload = vk_api.VkUpload(vk)
    photo = upload.photo_messages('image.jpg')
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    return attachment


def start():
    print("Бот запущен")
    api.messages.send(user_id=186003041, message="ABot включён!", random_id=get_random_id())

    while True:
        read = open('notification', 'r')
        message = read.read()
        read.close()
        pars = parse()
        name = pars[0]
        url = pars[1]
        pars = name + '\n' + url
        if pars != message:
            write = open('notification', 'w')
            write.write(pars)
            write.close()
            response = requests.get(url)
            with open('image.jpg', 'wb') as img:
                img.write(response.content)
                img.close()
            for i in range(len(user)):
                api.messages.send(user_id=user[i], message=name, random_id=get_random_id(), attachment=photos())
                print(f"Сообщение отправлено:\nНазвание: {name}\nПользователю: {user[i]}\n----------------------------")

        time.sleep(120)


if __name__ == "__main__":
    start()

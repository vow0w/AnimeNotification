from threading import Timer
from vk_api.longpoll import VkLongPoll, VkEventType
from config import token
import requests
import vk_api
from bs4 import BeautifulSoup
from vk_api.utils import get_random_id

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
api = vk.get_api()

# Debug mode
DEBUG = False

# Time for timers
TIME_CHECK_SITE_VALUE = 120.0
TIME_CHECK_MESSAGES_VALUE = 1

# Bot chat id for debugging
botChatID = 186003041

# Users id for notifications
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


def parseSite():
    if DEBUG:
        print("Parsing site for new data")

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
        for i in user:
            api.messages.send(user_id=i, message=name, random_id=get_random_id(), attachment=photos())
            print(f"Сообщение отправлено:\nНазвание: {name}\nПользователю: {i}\n----------------------------")

    if DEBUG:
        print("Starting new Timer")

    # run self after TIME_CHECK_VALUE seconds
    Timer(TIME_CHECK_SITE_VALUE, parseSite).start()


def sendMessage(user_id, text):
    api.messages.send(user_id=user_id, message=text, random_id=get_random_id())


def animeList(user_id, text):
    alist = open(f'{user_id}', 'a')
    alist.write(text + '\n')
    alist.close()


def checkMessages():
    if DEBUG:
        print("Check for new message")

    for event in longpoll.listen():

        if event.attachments.items():
            continue

        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                print(f'Новое сообщение от: {event.user_id}\nТекст: {event.text}\n-------------------')
                try:
                    text = event.text.lower().split(' ')
                    if text[0] == "!add":
                        if text[1] != "":
                            animeList(event.user_id, text[1])
                        else:
                            sendMessage({event.user_id}, "Не правильный формат ссылки!\nПравильный формат: "
                                                         "https://animevost.am/tip/**/*************.html")
                except:
                    continue

    if DEBUG:
        print("Start new timer for messages")
    # run self after TIME_CHECK_MESSAGES_VALUE seconds
    Timer(TIME_CHECK_MESSAGES_VALUE, checkMessages)


def start():
    print("Бот запущен")
    api.messages.send(user_id=botChatID, message="ABot включён!", random_id=get_random_id())

    # Start parse site every 120 seconds
    parseSite()

    # Start parse site every 120 seconds
    checkMessages()


if __name__ == "__main__":
    start()

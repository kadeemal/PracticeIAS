import configparser
import telethon.sync
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetChatsRequest
from telethon.tl.types import PeerChannel, PeerChat
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon import functions, types
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep
import glob, os, os.path
import tkinter as tk
from PIL import Image, ImageTk

api_id = 111111                                                    #вставьте собственное api_id, взятое с сайта телеграмм
api_hash = 'dassaddsa'                                             #api_hash то же самое
phone = '0000'                                                     #номер телефона, к которому привязан акк телеграмм
username = 'iasprac'                                               #название программы
client = TelegramClient(username, api_id, api_hash)

about = []                                                          #список для информации о группах
photos = []                                                         #список для фото групп
j = -1                                                              #переменная для итерации

def lookfor():                                                      #функция для запуска telethon
    global about, j, photos
    about = []
    photos = []
    j = -1
    filelist = glob.glob(os.path.join("*.jpg"))                     #удаление всех файлов jpg в каталоге с проектом
    for f in filelist:
        os.remove(f)
    async def main():
        search = ent_find.get()                                     #поиск групп
        result = await client(functions.contacts.SearchRequest(
        q=search,
        limit=100
        ))
        groups = []
        for i in result.chats:
            groups.append(i.title)
        mes = ''
        for i in groups:                                            #взятие всей необходимой инфы
            now = await client.get_entity(i)
            channel_full_info = await client(GetFullChannelRequest(channel=now))
            message = await client.get_messages(now, ids=types.InputMessagePinned())
            if (message): mes = str(message.message)
            #print(channel_full_info.full_chat.participants_count, ' ', message)        #закреп
            textabout = ('Название: ' + str(now.title) + '\n' +
                         'Username: @' + str(now.username) + '\n'
                         'Количество участников: ' + str(channel_full_info.full_chat.participants_count) + '\n'
                         'Описание: ' + str(channel_full_info.full_chat.about) + '\n'
                         'Закрепленное сообщение: ' + str(mes) + '\n' +
                         'Фото ----> \n')
            about.append(textabout)
            #direct = await client.download_profile_photo(now.title)    #метод для скачивания фото групп
            #photos.append(direct)                                      #метод для добавления названий фото групп в список фото групп
        next_i()

    with client:
        client.loop.run_until_complete(main())


def next_i():                                                       #функция для перелистывания найденной инфы вперед
    global j, photos
    j = j + 1
    if (j == len(about)): j = 0
    txt_about.delete("1.0", tk.END)
    if (len(about) != 0): txt_about.insert("1.0", about[j])
    else: txt_about.insert("1.0", "No information")


def previous_i():                                                   #функция для перелистывания найденной инфы назад
    global j
    j = j - 1
    if (j == -1): j = len(about) - 1
    txt_about.delete("1.0", tk.END)
    if (len(about) != 0): txt_about.insert("1.0", about[j])
    else: txt_about.insert("1.0", "No information")


window = tk.Tk()                                            #создание оконного приложения
window.title("Telegram Practice")

ent_find = tk.Entry(width=100)
ent_find.grid(row=0, column=0, padx=10, pady=10)
but_find = tk.Button(width=20, text="Найти", command=lookfor)
but_find.grid(row=0, column=1, padx=10, pady=10)
txt_about = tk.Text(width=60, heigh=30)
txt_about.grid(row=1, column=0, padx=10, pady=10)
but_previous = tk.Button(width=5, heigh=1, text="<", command=previous_i)
but_previous.grid(row=2, column=0, padx=10, pady=10)
but_next = tk.Button(width=5, heigh=1, text=">", command=next_i)
but_next.grid(row=2, column=1, padx=10, pady=10)
canvas = tk.Canvas(window, height=640, width=640)
image = Image.open("icon/hello.jpg")
photo = ImageTk.PhotoImage(image)
image = canvas.create_image(1, 1, anchor='nw', image=photo)
canvas.grid(row=1, column=1)

window.mainloop()
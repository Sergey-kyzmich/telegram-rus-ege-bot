import json
import random
import time
import datetime

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import requests
token=''
bot=telebot.TeleBot(token)

def check_time():

    now = datetime.datetime.now()
    dt = datetime.datetime.now() - datetime.datetime(year=now.year, month=now.month, day=now.day, hour=0, minute=0, second=0)
    return (dt - datetime.timedelta(hours=8, minutes=10)).total_seconds()

class call(object):
    def __init__(self, message, data):
        self.message = message
        self.data = data


def replace(s):
    s = s.replace("</span>", "")
    while "span" in s:
        s = s[:s.index("<span")] + s[s.index("span") + s[s.index("span"):].index(">") + 1:]
    while "<p" in s:
        s = s[:s.index("<p")] + s[s.index("<p") + 1 + s[s.index("<p"):].index(">") :]

    return (s.replace("&mdash;", "-").replace("<p>", "\n").replace("</p>", "").replace("&nbsp;<strong>", "<em> ")
            .replace("</strong>&nbsp;", "</em> ").replace("br", "\n").replace("strong", "em").replace("/strong", "/em")
            .replace("<...>", "...").replace("&shy;", "").replace("&ldquo;", "").replace("\r", "")
            .replace("< ", "").replace(" >", "").replace("<>", "").replace('<"">', "").replace("<\n>", "\n")
            .replace("&lt;", "").replace("&gt;", "").replace("<!-- [if !supportLists]-->", "")
            .replace("<!--[endif]-->", "").replace("&nbsp;", ".").replace("\r", "").replace("<&hellip;", "")
            .replace("&hellip;", "'...'").replace("&laquo;", "").replace("&raquo;", "").replace("&ndash;", "-"))



@bot.message_handler(commands=['start'])
def start_message(message):
    main_kb = ReplyKeyboardMarkup()
    mb_1 = KeyboardButton(text="/create_task")
    main_kb.add(mb_1)
    if random.randint(1, 10) == 1:
        for i in range(100):
            bot.send_video(message.chat.id, 'https://steamuserimages-a.akamaihd.net/ugc/829076779830279442/D9861E4A35F464C8EE9E5B3B58BA2E02B352B743/?imw=512&amp;imh=346&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true', None, 'Text')
    else:
        bot.send_message(message.chat.id, "Привет ✌️ ", reply_markup=main_kb)
@bot.message_handler(commands=['create_task'])
def create_task(message):
    kb = InlineKeyboardMarkup()
    for i in range(1, 28, 3):
        # print(i)
        b1 = InlineKeyboardButton(text=str(i), callback_data=f"task{i}")
        b2 = InlineKeyboardButton(text=str(i+1), callback_data=f"task{i+1}")
        b3 = InlineKeyboardButton(text=str(i+2), callback_data=f"task{i+2}")
        kb.add(b1,b2,b3)
    rand_button = InlineKeyboardButton(text="Рандомное задание", callback_data="task_random")
    kb.add(rand_button)

    bot.send_message(message.chat.id, "Выберите номер задания:", reply_markup=kb)


def def_eror(eror, e, k, rand, msg, callback):
    if eror.count("Неудачные посылки:") <= 15:
        print(e)
        eror += f"""
Неудачные посылки:
--------------------
Текст ошибки: {e}
Тип задания: {k}
Номер задания: {rand}
        """
        send(msg, callback, eror)
def send(msg, callback, eror):
    if callback.data != "task_random":
        k = callback.data
        k = int(k[4:])
    else:
        k = random.randint(1, 27)
    lines = 264 + k
    count = 200
    rand = random.randint(0, 200)
    if k == 27:
        response = requests.get(
            f"https://backend.neofamily.ru/api/task?sort[id]=asc&only=question,additional_info,subject_id,is_hidden,is_informal,free_answer,is_related,id,task_answer_size,status,is_favorite,is_briefcase&subject=russkiy-yazyk&parts[]=%D0%A7%D0%B0%D1%81%D1%82%D1%8C+2&lines[]={lines}&perPage={count}&except_solved=0&is_informal=0&is_hidden=0")
    else:
        response = requests.get(
        f"https://backend.neofamily.ru/api/task?sort[id]=asc&only=question,additional_info,subject_id,is_hidden,is_informal,free_answer,is_related,id,task_answer_size,status,is_favorite,is_briefcase&subject=russkiy-yazyk&parts[]=%D0%A7%D0%B0%D1%81%D1%82%D1%8C+1&lines[]={lines}&perPage={count}&except_solved=0&is_informal=0&is_hidden=0")
    result = response.json()['data']
    # try:
    name_task = f"""
Тип задания: {k}
Номер задания: {result[rand]["id"]}

"""

    kb_answer = InlineKeyboardMarkup()
    button_answer = InlineKeyboardButton(text=f'Получить ответ на задание ', callback_data=result[rand]["id"])
    kb_answer.add(button_answer)
    try:
        question = replace(result[rand]["question"])
        # print(f"{result[rand]}")
        if result[rand]["additional_info"]!=None:
            additional_info = replace(result[rand]["additional_info"])
        else:
            additional_info = ""
        if 21<k<27:
            if len(question) > 4096 or len(additional_info) > 4096:
                def_eror(eror, f"the message is very long. len first message: {len(additional_info)} len second message: {len(question)}", k, rand, msg, callback)
            else:
                bot.edit_message_text(chat_id=callback.message.chat.id, message_id=msg.message_id, text=name_task + "\nТекст для задания:\n"+ additional_info, parse_mode="HTML")
                bot.send_message(chat_id=callback.message.chat.id, text="Задание:\n"+question+"\n\n"+eror, reply_markup=kb_answer, parse_mode="HTML")
        elif additional_info == "":
            if k==27:
                if len(question[question.index("почерком.") + 10:])>4096 or len(question[:question.index("почерком.") + 10])>4096:
                    def_eror(eror, f"the message is very long. len first message: {len(question[question.index('почерком.') + 10:])} len second message: {len(question[:question.index('почерком.') + 10])}", k, rand, msg, callback)
                else:
                    bot.edit_message_text(chat_id=callback.message.chat.id, message_id=msg.message_id, text=name_task + "\nТекст для задания:\n" + question[question.index("почерком.") + 10:], parse_mode="HTML")
                    bot.send_message(chat_id=callback.message.chat.id, text = "Задание:\n"+question[:question.index("почерком.") + 10]+"\n\n"+eror, parse_mode="HTML")
            else:# print(result[rand]["question"])
                if len(question)+len(additional_info)>4096:
                    def_eror(eror, f"the message is very long. len first message: {len(question)} len second message: {len(additional_info)}", k, rand, msg, callback)
                else:
                    bot.edit_message_text(chat_id=callback.message.chat.id,message_id=msg.message_id, text=name_task+replace(result[rand]["question"])+"\n\n"+eror, reply_markup=kb_answer, parse_mode="HTML")

        else:
            # print(replace(result[rand]["question"] + "\n" + result[rand]["additional_info"]))
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=msg.message_id, text=name_task+question + "\n \n" + additional_info+"\n\n"+eror, reply_markup=kb_answer, parse_mode="HTML")
    except Exception as e:
        def_eror(eror, e, k, rand, msg, callback)
@bot.callback_query_handler(func=lambda  callback: callback.data)
def check_callback_data(callback):
    if "task" not in callback.data:
        answer = requests.get(f"https://backend.neofamily.ru/api/task/{callback.data}/solution")
        ans = answer.json()
        ans = ans["data"]["solution"]
        try:
            bot.send_message(callback.message.chat.id, replace(ans[:ans.index("<p><strong>Источник")]), parse_mode="HTML")

        except:
            pizdec = ans[ans.index("Ответ:") + ans[ans.index("Ответ"):].index("/span") - 10:ans.index("Ответ:") + ans[ans.index("Ответ"):].index("/span")]
            pizdec = (ans[ans.index("Ответ:") + ans[ans.index("Ответ"):].index("/span") - 10 + pizdec.index(">") + 1:ans.index("Ответ:") + ans[ans.index("Ответ"):].index("/span") - 10 + pizdec.index("<")])
            bot.send_message(callback.message.chat.id, replace(ans[:ans.index("Ответ")]) + "Ответ: " + pizdec + "</em>",
                             parse_mode="HTML")
    else:
        msg = bot.send_message(callback.message.chat.id, "Загрузка...")
        send(msg, callback, "")
    # except:
    #     bot.send_message(callback.message.chat.id, replace(result[rand]["question"]), parse_mode="HTML")

@bot.message_handler(commands=['on_timer'])
def on_timer(message):
    with open("id_list.json", "r") as f:
        load = json.load(f)
    load[str(message.chat.id)] = True
    with open("id_list.json", "w") as f:
        json.dump(load, f)
    bot.send_message(message.chat.id, text= "Отлично, утром ожидайте задание!")

@bot.message_handler(commands=["off_timer"])
def off_timer(message):
    with open("id_list.json", "r") as f:
        load = json.load(f)
    load[str(message.chat.id)] = False
    with open("id_list.json", "w") as f:
        json.dump(load, f)
    bot.send_message(message.chat.id, text="Задания больше не будут приходить!")

@bot.message_handler(commands="off_all_timer")
def off_all_timer(message):
    if message.chat.id == 5173778472:
            with open("id_list.json", "r") as f:
                load = json.load(f)
            load["all"] = False
            with open("id_list.json", "w") as f:
                json.dump(load, f)
            bot.send_message(message.chat.id, text="Рассылка заданий отключена!")
    else:
        bot.send_message(message.chat.id, text = "Ты не я!")

@bot.message_handler(commands="on_all_timer")
def on_all_timer(message):
    bot.send_message(message.chat.id, text="Рассылка активированна!")
    print("Рассылка активированна!")
    total = check_time()
    if total<0:
        print(f"{total=}")
        time.sleep(abs(int(total)))
    # print(message.chat.id)
    while True:
        with open("id_list.json", "r") as f:
            d = json.load(f)
        user_list = d
        print("Активные каналы:", d)
        for id in user_list:
            if id != "all":
                if user_list[id]==True:
                    message.chat.id = int(id)
                    msg = bot.send_message(message.chat.id, "Загрузка...")
                    send(msg, call(message, "task_random"), "")
        total = check_time()
        # print(total)
        print("wait", 24*3600-int(total))
        time.sleep(24*3600-int(total))
        if datetime.datetime.now().weekday() in [5,6]:
            time.sleep(3*3600)

@bot.message_handler(commands="help")
def help(message):
    text_2 = """
/help - Список команд
/start - старт бота(+показать кнопку с командой /create_task)
/create_task - создать задание
/on_timer - Активировать рассылку одного рандомного задания в 8:10 по МСК
/off_timer - Отключить рассылку
/on_all_timer - Активировать рассылку
/off_all_timer - Отключить рассылку"""
    bot.send_message(message.chat.id, text=text_2)
bot.infinity_polling()

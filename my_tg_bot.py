import telebot
from random import *
import json
import requests
import g4f
from g4f.client import Client

films=[]
API_TOKEN='7665859013:AAETJ_yvV77R7PNNJkqZEqui_60Zu0AVifg'
API_URL='https://7012.deeppavlov.ai/model' # From DeepPavlov 1.0 API
bot=telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        load()
        bot.send_message(message.chat.id,"Фильмотека была успешно загружена!")

    except:
        films.append("Матрица")
        films.append("Солярис")
        films.append("Властелин колец")
        films.append("Техасская резня бензопилой")
        films.append("Санта Барбара") 
        bot.send_message(message.chat.id,"Фильмотека была загружена по умолчанию!")

@bot.message_handler(commands=['save'])
def save_all(message):
    with open("films.json","w",encoding="utf-8") as fh:
        fh.write(json.dumps(films,ensure_ascii=False))
    bot.send_message(message.chat.id,"Наша фильмотека была успешно сохранена в файле films.json")

@bot.message_handler(commands=['load'])    
def load_all(message):
    global films
    with open("films.json","r",encoding="utf-8") as fh:
        films=json.load(fh)
    bot.send_message(message.chat.id,"Наша фильмотека была успешно загруженна")
        

@bot.message_handler(commands=['all'])
def show_all(message):
    try:
        bot.send_message(message.chat.id,"Вот список фильмов")
        bot.send_message(message.chat.id, ", ".join(films))
    except:
        bot.send_message(message.chat.id,"Фильмотека пустая")
        
## Работа Telegramm с ChatGPT        
        
@bot.message_handler(content_types=['text'])
def gpt_response(message): 
    bot.send_message(message.chat.id, "хмммм.... сейчас отвечу, буквально минутку.")
    user_text = message.text

    try:
        
        client = Client()
        resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}], temperature =0.5)
        rep=resp.choices[0].message.content
        bot.send_message(message.chat.id, rep, parse_mode='Markdown') 
                     
    except:
        bot.send_message(message.chat.id, "Нету связи с ChatGPT. Введите запрос ещё раз ")
        
        
## Работа Telegramm с ChatGPT  с тремя вариантами ответа        
        
# import openai

# openai.api_key = 'your_openai_api_key'


# @bot.message_handler(content_types=['text'])
# def gpt_response(message): 
#     bot.send_message(message.chat.id, "хмммм.... сейчас отвечу, буквально минутку.")
#     user_text = message.text

#     try:
        
#         client = Client()
#         resp = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": user_text}], temperature =0.5, 
#         n=3   # Запрашиваем три варианта
#         )
        
#         # Выводим все три варианта ответа
#         for i, choice in enumerate(resp.choices):
#             rep = choice.message.content
#             bot.send_message(message.chat.id, f"Вариант {i+1}:\n{rep}", parse_mode='Markdown')
            
#     except:
#         bot.send_message(message.chat.id, "Нету связи с ChatGPT. Введите запрос ещё раз ")

    
@bot.message_handler(commands=['wiki'])
def wiki(message):
    quest = message.text.split()[1:]
    qq=" ".join(quest)
    data = { 'question_raw': [qq]}
    try:
        res = requests.post(API_URL,json=data,verify=False).json()
        bot.send_message(message.chat.id, res)
    except:
        bot.send_message(message.chat.id, "Что-то я ничего не нашел :-(")
        
        
# @bot.message_handler(content_types=['text'])
# def get_text_message(message):
#     if "дела" in message.text.lower():
#         bot.send_message(message.chat.id, "Дела у меня хорошо, сам как?")

bot.polling()


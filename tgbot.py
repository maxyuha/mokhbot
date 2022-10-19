from datetime import datetime
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint as rd
from scripts21 import check 
from random import choice as ch
import wikipedia


wikipedia.set_lang('ru')

bot = Bot(token='5657140697:AAH8Hk-YnFRbz0kEJR2N_zKSonT3stWVGvc')
updater = Updater(token='5657140697:AAH8Hk-YnFRbz0kEJR2N_zKSonT3stWVGvc')
dispatcher = updater.dispatcher


def start(update, context):
  context.bot.send_message(update.effective_chat.id, '''Привет,я бот, и мне не нравится слова ,содержащие "абв",когда ты их пишешь.
  Доступные комманды:
  /news - случайная  новость
  /random - число от 1 до 1000
  /commands - список комманд
  /game - игра в 21(я считаю сколько каждый из нас выирал)
  /restart - перезапуск бота''')


def wiki(update, context):
  now = datetime.now()
  text = now.date()
  result = wikipedia.summary(text)
  context.bot.send_message(update.effective_chat.id, result)

def rand(update, context):
  context.bot.send_message(update.effective_chat.id, f'{rd(1,1000)}')


def commands(update,context):
    context.bot.send_message(update.effective_chat.id, '''
  Доступные комманды:
  /news - случайная свежая новость
  /random - число от 1 до 1000
  /commands - список комманд
  /game - игра в 21(я считаю сколько каждый из нас выирал)(напиши стоп)
  /restart - перезапуск бота''')




data = {"Валет" : 2,"Дама" : 3, "Король" : 4, 6 : 6, 7 : 7, 8 : 8, 9 : 9, 10 : 10, "Туз" : 11}
count_player_points = []
count_bot_points = 0
BOT = 1
USER = 2
WINNER = None # 0 - ничья, 1 - выиграл пользователь, -1 - выиграл бот

BOT = 1
USER = 2
def winner_check(user, bots):
    global WINNER
    if sum(user) > 21 and bots < 22 or sum(user) < bots and sum(user) <= 21 and bots <= 21:
        WINNER = -1
    elif bots > 21 and sum(user) < 22 or sum(user) > bots and sum(user) <= 21 and bots <= 21:
        WINNER = 1
    elif sum(user) > 21 and bots > 21:
        WINNER = 0


def game(update, context):
    global count_points_user, count_points_bot, WINNER

    count_points_user.clear()
    count_points_bot = 0
    WINNER = None

    for i in range(2):
        data_object = ch(list(data.keys()))
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_user.append(points)

    for i in range(2):
        data_object = ch(list(data.keys()))
        print(data_object)
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_bot += points

    if sum(count_points_user) > 21 and count_points_bot < 22:
        context.bot.send_message(update.effective_chat.id, "Перебор выиграл бот")
    elif count_points_bot > 21 and sum(count_points_user) < 22:
        context.bot.send_message(update.effective_chat.id, "Перебор выиграл ты")
    elif sum(count_points_user) > 21 and count_points_bot > 21:
        context.bot.send_message(update.effective_chat.id, "Перебор вы оба проиграли")
    else:
        a = '\n'.join([str(i) for i in count_points_user])
        context.bot.send_message(update.effective_chat.id, f"{a}\nСумма: {sum(count_points_user)}")


def yet(update, context):
    global count_points_user
    if sum(count_points_user) < 21:
        data_object = ch(list(data.keys()))
        while data[data_object] == 0:
            data_object = ch(list(data.keys()))
        data[data_object] -= 1
        points = check(data_object)
        count_points_user.append(points)

        a = '\n'.join([str(i) for i in count_points_user])
        winner_check(count_points_user, count_points_bot)
        if sum(count_points_user) > 21:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, ты проиграл")
        context.bot.send_message(update.effective_chat.id, f"{a}\nСумма: {sum(count_points_user)}")
    else:
        context.bot.send_message(update.effective_chat.id, "Ты не можешь взять больше!")


def gamestop(update, context):
    if WINNER == None:
        global count_points_bot
        context.bot.send_message(update.effective_chat.id, 'Вы закончили набор, теперь набирает бот')
        if count_points_bot > 15 and ch([True, False]) or count_points_bot <= 12:
            data_object = ch(list(data.keys()))
            while data[data_object] == 0:
                data_object = ch(list(data.keys()))
            data[data_object] -= 1
            points = check(data_object)
            count_points_bot += points

        winner_check(count_points_user, count_points_bot)
        context.bot.send_message(update.effective_chat.id, f'Кол-во очков у бота: {count_points_bot}\n'
                                                           f'Кол-во очков у {update.effective_user.first_name}: {sum(count_points_user)}')
        if WINNER == -1:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, "
                                                               f"у тебя перебор выиграл бот")
        elif WINNER == 1:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name}, ты выиграл")
        elif WINNER == 0:
            context.bot.send_message(update.effective_chat.id, f"{update.effective_user.first_name} вы с ботом лузеры")
    else:
        context.bot.send_message(update.effective_chat.id, f"Игра окончена, чтобы начать заново напишите /start")






def message(update, context):
    my_text = update.message.text
    def del_some_words(my_text):
      my_text = list(filter(lambda x: 'абв' not in x, my_text.split()))
      return " ".join(my_text)

    my_text = del_some_words(my_text)
    context.bot.send_message(update.effective_chat.id, f'{my_text}')


  


start_handler = CommandHandler('start', start)
random_handler = CommandHandler('random', rand)
wiki_handler = CommandHandler('news', wiki)
commands_handler = CommandHandler('commands', commands)
game_handler = CommandHandler('game', game)
still_handler = CommandHandler('yet', yet)
stop_handler = CommandHandler('stop', gamestop)
message_handler = MessageHandler(Filters.text, message)



dispatcher.add_handler(start_handler)
dispatcher.add_handler(wiki_handler)
dispatcher.add_handler(random_handler)
dispatcher.add_handler(commands_handler)
dispatcher.add_handler(game_handler)
dispatcher.add_handler(still_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(message_handler)




updater.start_polling()
updater.idle()
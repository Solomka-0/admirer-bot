import time

import telebot
from telebot import types

from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, declarative_base

# from models.user import User

# Инициализация моделей ORM
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    romantic_step = Column(Integer, nullable=True)

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()


def user(id):
    user_model = session.query(User).filter_by(id=id).first()
    if (user_model == None):
        user_model = User(id=id)
        session.add(user_model)
    session.commit()
    return user_model


BOT_TOKEN = "6466590892:AAFfVUByQ2VcTlY82qipJGzf1F_sU1Q5Ga8"
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)


def romantic_start(message):
    user_model = user(message.from_user.id)
    user_model.username = message.from_user.username
    session.commit()
    romantic_handler(message, chat_id=message.chat.id)

def romantic_handler(message, chat_id, step=0):
    markup = types.InlineKeyboardMarkup()

    user_model = user(message.from_user.id)
    user_model.romantic_step = step
    session.commit()

    if user_model.romantic_step == 0:
        markup.add(types.InlineKeyboardButton(text='Ναι.', callback_data=f"romantic_1_{chat_id}"))
        markup.add(types.InlineKeyboardButton(text='δεν.', callback_data=f"romantic_2_{chat_id}"))

        bot.send_message(chat_id, reply_markup=markup,
                         text="Ω, αγαπητό κορίτσι. Ελπίζω αυτό το γράμμα να φτάσει σε εσάς. Το πήρες; 📩"
                         )
    elif user_model.romantic_step == 1:
        markup.add(types.InlineKeyboardButton(text='Ναι.', callback_data=f"romantic_3_{chat_id}"))
        markup.add(types.InlineKeyboardButton(text='δεν.', callback_data=f"romantic_4_{chat_id}"))

        bot.send_message(chat_id, reply_markup=markup,
                         text="Μπες στο θέμα. Δεν ξέρω καθόλου Ελληνικά. Νομίζω ότι γράφω με λάθη. Μπορώ να μιλήσω ρωσική; 👅"
                         )
    elif user_model.romantic_step == 2:
        markup.add(types.InlineKeyboardButton(text='Εντάξει...', callback_data=f"romantic_1_{chat_id}"))

        bot.send_message(chat_id, reply_markup=markup,
                         text="Είναι λυπηρό να το συνειδητοποιείς αυτό. Έχω ετοιμάσει μια άλλη επιστολή. Ορίστε! 🧹️")
    elif user_model.romantic_step == 3:
        # Если согласна перейти на русский
        markup.add(types.InlineKeyboardButton(text='Какой?', callback_data=f"romantic_5_{chat_id}"))
        
        bot.send_message(chat_id, reply_markup=markup,
                         text="Солнце ☀️, у меня всего один вопрос...")
    elif user_model.romantic_step == 4:
        # Если не согласна перейти на русский
        bot.send_message(chat_id, reply_markup=markup,
                         text="Ηλιαχτίδα, έχω μόνο μια ερώτηση... ☀️")
        markup.add(types.InlineKeyboardButton(text="Ποιο απ ' όλα;", callback_data=f"romantic_6_{chat_id}"))
    elif user_model.romantic_step == 5:
        # Вопрос на русском
        markup.add(types.InlineKeyboardButton(text='Да!', callback_data=f"romantic_7_{chat_id}"))
        markup.add(types.InlineKeyboardButton(text='Нет', callback_data=f"romantic_8_{chat_id}"))

        bot.send_message(chat_id, reply_markup=markup,
                         text="Пойдешь со мной на свидание? ❤️‍")
    elif user_model.romantic_step == 6:
        # Вопрос на греческом
        markup.add(types.InlineKeyboardButton(text='Ναι!', callback_data=f"romantic_7_{chat_id}"))
        markup.add(types.InlineKeyboardButton(text='Δεν', callback_data=f"romantic_8_{chat_id}"))
        bot.send_message(chat_id, reply_markup=markup,
                         text="Θα βγεις ραντεβού μαζί μου; ❤️‍")
    elif user_model.romantic_step == 7:
        # Ответила да
        print('Это да!')
        markup.add(types.InlineKeyboardButton(text='💘', callback_data=f"romantic_10_{chat_id}"))
        bot.send_message(chat_id, reply_markup=markup,
                         text="!!!!!!!!!"
                              "\nСегодня буду счастливым! 💘"
                              "\nВозможно, не увижу ответа, бот еще совсем зеленый")
        bot.send_message(6616840677,
                         text="Это да!")
    elif user_model.romantic_step == 8:
        # Ответила нет
        markup.add(types.InlineKeyboardButton(text='...', callback_data=f"romantic_0_{chat_id}"))
        bot.send_message(chat_id, reply_markup=markup,
                         text="Ладно :[ 💔")
    elif user_model.romantic_step == 10:
        bot.send_message(6616840677,
                         text="Она ответила да!")
        print('Она ответила да!')


@bot.message_handler(commands=['help'])
def help(message):
    time.sleep(1)
    bot.send_message(message.chat.id,
                     "Что я умею?"
                     "\nНичего...😢 _* to be continued *_"
                     , parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if 'romantic' in call.data:
        romantic_handler(call, call.data.split('_')[2], call.data.split('_')[1])
    else:
        bot.send_message(call.chat.id,
                         text="Пустота... Осторожно, строительные работы. Попробуйте тыкнуть в другое место")

@bot.message_handler(commands=['start'])
def start(message):
    # Главное меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add("Новая книга", "Новый тэг", "🔎 Поиск")

    if message.from_user.username == 'NoaDjo':
        markup.add("Создать статью", types.KeyboardButton(text="💌"))
    else:
        markup.add("Создать статью")

    bot.send_message(message.chat.id, reply_markup=markup,
                     text="Приветствую! Я - помощник по управлению контентом."
                          "\n📕 Есть новая книга? - смело нажимай на кнопку меню, помогу"
                          "\n💼 Хочешь изменить стандарты, упростить поиск? - поможет ли тег?"
                          "\n📝 Пиши на интересную тему"
                          "\nБуду развиваться и дальше"
                     )
    help(message)

@bot.message_handler(content_types=['text'])
def text_handler(message):
    handler = {
        '💌': romantic_start,
    }

    try:
        handler[message.text](message)
    except:
        bot.send_message(message.chat.id,
                         text="Пустота... 🍃\nОсторожно, строительные работы.⚠️\nПопробуйте тыкнуть в другое место")


bot.polling(none_stop=True, interval=0)

import os
import toml
import hashlib
import jsonpickle
import mysql.connector
from telebot import types, TeleBot
from requests_doh import DNSOverHTTPSSession, add_dns_provider, remove_dns_provider

LAST_PART = ''
FLAG = 'CODEBY{うそだ}'
TOKEN = ""
bot = TeleBot(TOKEN)
states = {}


def connect_and_query(host, user, password, query):
    try:
        con = mysql.connector.connect(host=host, user=user, password=password, database='commands')
        cursor = con.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        return e


# name: Earth Is A Black Hole, key: ?????????
def get_obfuscate_bot_username_tg(name, key):
    return 'bot_' + hashlib.sha256((''.join([x for x in hashlib.md5(name.encode()).hexdigest() if x.isdigit()] + [x for x in hashlib.md5(key.encode()).hexdigest() if x.isdigit()])[:20]).encode()).hexdigest()[:20] + '_bot'


def db_query(message: types.Message):
    temp = message.text.split(sep='\n')
    if len(temp) == 4:
        bot.send_message(chat_id=message.chat.id, text=connect_and_query(temp[0], temp[1], temp[2], temp[3]))
    elif len(temp) == 5:
        try:
            add_dns_provider(str(message.chat.id), temp[4] + f'/{message.chat.id}')
            session = DNSOverHTTPSSession(str(message.chat.id))
            r = session.get(f'http://hlebniypunkeasy.codeby/?last_part={LAST_PART}')
            if r.status_code == 200:
                bot.send_message(chat_id=message.chat.id, text='✅ Last part was sent to <b>http://hlebniypunkeasy.codeby</b>', parse_mode='HTML')
            else:
                bot.send_message(chat_id=message.chat.id, text=f'❌ Error occured', parse_mode='HTML')
            remove_dns_provider(str(message.chat.id))
        except:
            bot.send_message(chat_id=message.chat.id, text=f'❌ Error occured', parse_mode='HTML')
    else:
        bot.send_message(chat_id=message.chat.id, text='❌ Incorrect count parameters', parse_mode='HTML')


def convert(message: types.Message):
    try:
        bot.send_message(chat_id=message.chat.id, text=toml.dumps(jsonpickle.decode(message.text)))
    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=f'❌ Incorrect input, {e}')


@bot.message_handler(commands=['????????????????????????????????'])
def secret_command(message: types.Message):
    if message.chat.id not in states or states[message.chat.id] != 'convert':
        states[message.chat.id] = 'convert'
    bot.send_message(chat_id=message.chat.id, text='❕ Send JSON string for convert to TOML\nEnter <b>/exit</b> to '
                                                   f'leave <i>{states[message.chat.id]}</i> mode', parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start_bot(message: types.Message):
    bot.send_photo(chat_id=message.chat.id, photo=open('images/mrfresh.jpg', 'rb'), caption='Hello! 😸\nIt is my helper bot for small ⚙️ '
                                                               'administrative works')


@bot.message_handler(commands=['db'])
def db_command(message: types.Message):
    if message.chat.id not in states or states[message.chat.id] != 'db':
        states[message.chat.id] = 'db'

    bot.send_message(chat_id=message.chat.id, text='❕ <b>Enter credentials and '
                                                   'query</b>\n\n<u>Example</u>:\nexample.com\nadmin\npassword'
                                                   f'\nSELECT vesrion()\n\nEnter <b>/exit</b> to leave <i>{states[message.chat.id]}</i> mode',
                     parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def handle_text(message: types.Message):
    if message.text == '/exit':
        try:
            states.pop(message.chat.id)
            bot.send_photo(chat_id=message.chat.id, photo=open('images/sadcat.jpg', 'rb'),
                           caption='💡 Successfully exited')
        except:
            bot.send_message(chat_id=message.chat.id, text='🔧 No selected mode')
            bot.send_sticker(chat_id=message.chat.id, sticker=open('images/sad_cat_sticker.webm', 'rb'))
    else:
        try:
            if states[message.chat.id] == 'db':
                db_query(message)
            if states[message.chat.id] == 'convert':
                convert(message)
        except:
            pass

bot.infinity_polling()

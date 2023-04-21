import telebot
import sqlite3

from telebot import types

bot = telebot.TeleBot("TOKEN_BOT")
name = None #By writing this command

@bot.message_handler(commands= ["start"])
def start(message):
    conn = sqlite3.connect("sql.sql")
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS user (id int auto_increment primary key, name varchar(50), pass varchar(50))")
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Hi, we'll register you now! Write your name user: ")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name #We can use the command global 
    name = message.text.strip()
    bot.send_message(message.chat.id, "Enter your password: ")
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    
    conn = sqlite3.connect("sql.sql") #you can rename the file 
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES('%s', '%s')"% (name, password))
    conn.commit()
    cur.close()
    conn.close()
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("List of users", callback_data= "users"))
    bot.send_message(message.chat.id, "User is registered", reply_markup=markup)
    
@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    conn = sqlite3.connect("sql.sql")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    info = ""
    for el in users:
        info += f"Name: {el[1]}, password: {el[2]}＼n" #it adds every time a new user registers 
                                                       #el{1} - taken from line 14, 0-id, 1-name, 2-pass
    cur.close()
    conn.close()
    
    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                           
#   ~ CyPay 1.0 beta ~                            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# CoDeD: bY TSENKEO
# DaTe: 02/11/2021
# Dev: Python
#
#~~~~~~~~~~~ INFO ~~~~~~~~~~~~
#
# Sending Bitcoin in Telegram bot
#
#*****************************



import my_constants, re, secrets, string, datetime, pytz, sqlite3
from telebot import *
from bit import *
from bit import PrivateKey as Key 
#from bit import PrivateKeyTestnet as Key
from bit.network import currency_to_satoshi
from bit.network import satoshi_to_currency 


def create_base(db):
    cursor = db.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS "USERS"(user_id INTEGER, 
            private_key TEXT, 
            registration_date TEXT, 
            user_address TEXT, 
            last_transaction TEXT, 
            now_balance TEXT, 
            btc_balance TEXT, 
            usd_balance TEXT, 
            rub_balance TEXT, 
            status_date TEXT);'''
                    )
    db.commit()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS "TRANSACTION"(sender_id INTEGER,
            summ_in_btc TEXT,  
            address_accept TEXT,
            commission_network TEXT, 
            commission_bot TEXT, 
            datetime_transaction TEXT,
            status TEXT,  
            order_transaction TEXT,
            FOREIGN KEY("sender_id") REFERENCES "USERS"("user_id"));'''
                       )
    db.commit()
    print('Create DataBase')


with sqlite3.connect('db.db', check_same_thread=False) as db:
    db = db

create_base(db)

def cur():
    cursor = db.cursor()
    return cursor

def generate_crypt(len:int):
    len_and_dig = string.ascii_letters + string.digits
    crypt_string = ''.join(secrets.choice(len_and_dig) for i in range(len))
    return crypt_string

class select_db:
    def check_id_in_db(id:int):
        cursor = cur()
        cursor.execute(f'SELECT user_id FROM USERS WHERE "user_id" = "{id}";')
        data = cursor.fetchone()
        if data is None:
            return False
        elif id == data[0]:
            return True
    def private_key(user_id:int):
        cursor = cur()
        cursor.execute(f'SELECT private_key FROM USERS WHERE "user_id" = "{int(user_id)}"')
        data = cursor.fetchone()
        return data[0]
    def registration_date(user_id:int):
        cursor = cur()
        cursor.execute(f'SELECT registration_date FROM USERS WHERE "user_id" = "{int(user_id)}"')
        data = cursor.fetchone()
        return data[0]
    def user_address(user_id:int):
        cursor = cur()
        cursor.execute(f'SELECT user_address FROM USERS WHERE "user_id" = "{int(user_id)}"')
        data = cursor.fetchone()
        return data[0]
    class fin:
        def last_transaction(user_id:int):
            cursor = cur()
            cursor.execute(f'SELECT last_transaction FROM USERS WHERE "user_id" = "{int(user_id)}"')
            data = cursor.fetchone()
            return data[0]
        def now_balance(user_id:int):
            cursor = cur()
            cursor.execute(f'SELECT now_balance FROM USERS WHERE "user_id" = "{int(user_id)}"')
            data = cursor.fetchone()
            return data[0]
        def btc_balance(user_id:int):
            cursor = cur()
            cursor.execute(f'SELECT btc_balance FROM USERS WHERE "user_id" = "{int(user_id)}"')
            data = cursor.fetchone()
            return data[0]
        def usd_balance(user_id:int):
            cursor = cur()
            cursor.execute(f'SELECT usd_balance FROM USERS WHERE "user_id" = "{int(user_id)}"')
            data = cursor.fetchone()
            return data[0]
        def rub_balance(user_id:int):
            cursor = cur()
            cursor.execute(f'SELECT rub_balance FROM USERS WHERE "user_id" = "{int(user_id)}"')
            data = cursor.fetchone()
            return data[0]
        def status_date(user_id:int):
            cursor = cur()
            cursor.execute(f'SELECT status_date FROM USERS WHERE "user_id" = "{int(user_id)}"')
            data = cursor.fetchone()
            return data[0]


class add_db:
    def add_new_user(user_id:int):
        cursor = cur()
        key = Key()
        private_key = key.to_wif()
        d = datetime.now(pytz.timezone('Europe/Moscow'))
        registration_date = d.strftime('%d.%m.%Y %H:%M')
        user_address = key.address
        last_transaction = 'not'
        now_balance = key.get_balance()
        btc_balance = key.get_balance('btc')
        usd_balance = key.get_balance('usd')
        rub_balance = key.get_balance('rub')
        status_date = d.strftime('%d.%m.%Y %H:%M')
        d = (user_id, private_key,  registration_date, user_address,
            last_transaction, now_balance, btc_balance,
            usd_balance, rub_balance, status_date)
        cursor.execute('INSERT INTO "USERS" VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', d)
        db.commit()
        return True


    def add_own_key(key:str, user_id:int):
        try:
            key = Key(key)
            key = key.to_wif()
            cursor = cur()
            user_address = Key(key).address
            registration_date = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%H:%M %d.%m.%Y')
            cursor.executescript(f'''UPDATE USERS set "private_key" = "{key}" WHERE "user_id" = "{user_id}";
                                    UPDATE USERS set "registration_date" = "{registration_date}" WHERE "user_id" = "{user_id}";
                                    UPDATE USERS set "user_address" = "{user_address}" WHERE "user_id" = "{user_id}";''')
            db.commit()
            an = '✅ *Ключ успешно добавлен!*'
        except ValueError and Exception as v:
            an = '❌ *Ключ не распознан!*\nПопробуйте снова.'
            print(v)
            if re.compile(r'^Decoded checksum ').findall(str(v)):
                print(an)
                an = '❌ *Ключ не распознан!*'
        return an
    def update_user_data(user_id:int):
        cursor = cur()
        key = Key(select_db.private_key(user_id=user_id))
        now_balance = key.get_balance()
        btc_balance = key.get_balance('btc')
        usd_balance = key.get_balance('usd')
        rub_balance = key.get_balance('rub')
        d = datetime.now(pytz.timezone('Europe/Moscow'))
        status_date = d.strftime('%H:%M %d.%m.%Y')
        cursor.executescript(f'''UPDATE USERS set "now_balance" = "{now_balance}" WHERE "user_id" = "{user_id}";
                                UPDATE USERS set "btc_balance" = "{btc_balance}" WHERE "user_id" = "{user_id}";
                                UPDATE USERS set "usd_balance" = "{usd_balance}" WHERE "user_id" = "{user_id}";
                                UPDATE USERS set "rub_balance" = "{rub_balance}" WHERE "user_id" = "{user_id}";
                                UPDATE USERS set "status_date" = "{status_date}" WHERE "user_id" = "{user_id}";''')
        db.commit()
        return True
    def transaction_address_and_id(sender_id:int, address_accept:str, order=str):
        cursor = cur()
        d = datetime.now(pytz.timezone('Europe/Moscow'))
        Date = str(d.strftime('%d.%m.%Y %H:%M:%S'))
        d = (sender_id, '-', address_accept, '-', '-', Date,  'create', order)
        cursor.execute('INSERT INTO "TRANSACTION" VALUES(?, ?, ?, ?, ?, ?, ?, ?);', d)
        db.commit()




bot = telebot.TeleBot(my_constants.token, parse_mode="Markdown")
while True:
    print('Connection with Telegram')


    class keyboards:
        def keyboard_start(address:str):
            keyboard_start = types.InlineKeyboardMarkup()
            callback_button_update = types.InlineKeyboardButton(text='Обновить курс и баланс', callback_data='start_update')
            callback_button_add_key = types.InlineKeyboardButton(text='Добавить адрес️', callback_data='add_key')
            callback_button_show_private_key = types.InlineKeyboardButton(text='Показать ключ 👁', callback_data='show_private_key')
            callback_button_trade = types.InlineKeyboardButton(text='Пополнить/вывести', callback_data='trade')
            callback_button_transaction = types.InlineKeyboardButton(text='Перевести 💳', callback_data='send')
            url_button_history = types.InlineKeyboardButton(text='История транзакций 🧾',
                                                            url=f'{my_constants.blockchain}{address}/')
            switch_button = types.InlineKeyboardButton(text='Быстрый перевод️', switch_inline_query='100 rub')
            keyboard_start.add(callback_button_update)
            keyboard_start.add(callback_button_show_private_key, callback_button_add_key)
            keyboard_start.add(callback_button_transaction, switch_button)
            keyboard_start.add(callback_button_trade)
            keyboard_start.add(url_button_history)
            return keyboard_start

  
        keyboard_send = types.InlineKeyboardMarkup()
        callback_button_yes = types.InlineKeyboardButton(text='✅ Подтвердить', callback_data='yes_send')
        callback_button_no = types.InlineKeyboardButton(text='✖Отмена', callback_data='no_send')
        keyboard_send.add(callback_button_yes)
        keyboard_send.add(callback_button_no)

        keyboard_sign = types.InlineKeyboardMarkup()
        callback_button_yes_terms = types.InlineKeyboardButton(text='✅ Принять', callback_data='yes_terms')
        keyboard_sign.add(callback_button_yes_terms)


    def mailing(text:str):
        cursor = cur()
        cursor.execute('SELECT user_id FROM USERS')
        data = cursor.fetchall()
        print('Столько у тебя пользователей: ', len(data))
        kol = 0
        block = ' '
        for i in range(0, len(data)):
            try:
                id = data[i][0]
                bot.send_message(chat_id=id, text=text)
                print('Отправлено ', id)
                kol = kol + 1
            except telebot.apihelper.ApiException:
                print('Заблокировал бот ', id)
                block += f'\n`{id}`'
        f = f'*Готово!*\n\n*Количество пользователей: {len(data)}*\n\n*Доставлено: {kol}*\n\n*Заблокировали бот (ID):*{block}'
        return f


    class transaction:
        def transaction(user_id:int, address:str, summ):
            balance = int(select_db.fin.now_balance(user_id))
            summ = int(summ)
            try:
                if balance < summ:
                    answer_None = f'*Указанная сумма:* ' \
                                  f'\n└*{float(float(summ)/100000000.0)} BTC*' \
                                  f'\n\n*Ваш баланс:* ' \
                                  f'\n└ *{float(float(balance)/100000000.0)} BTC*' \
                                  f'\n\n*Уменьшите сумму!*'
                    cursor = cur()
                    cursor.execute(f'UPDATE "TRANSACTION" set "status" = "False" WHERE "sender_id" = "{user_id}" and "summ_in_btc" = "{summ}" and "address_accept" = "{address}" and "status" = "create"')
                    db.commit()
                    return answer_None
                elif balance > summ:
                    summ = str(summ)
                    key = Key(select_db.private_key(user_id))
                    cursor = cur()
                    cursor.execute(f'SELECT * FROM "TRANSACTION" WHERE "sender_id" = "{user_id}" and "summ_in_btc" = "{summ}" and "address_accept" = "{address}" and "status" = "create"')
                    data = cursor.fetchone()
                    if data:
                        summ = int(summ)
                        address_to_send = data[2]
                        commisson_net = int(data[3])
                        commission_bot = int(data[4])
                        summ_without_comm = summ - commission_bot - commisson_net
                        transaction_id = key.send(
                            [(address_to_send, satoshi_to_currency(summ_without_comm, 'btc'), 'btc'),
                             (my_constants.btc_address_for_commission, satoshi_to_currency(commission_bot, 'btc'), 'btc')],
                            fee=commisson_net, absolute_fee=True)
                        if True:
                            answer_True = f'✅ *Успешно отправлено в сеть!*' \
                                          f'\n*ID транзакции:* ' \
                                          f'\n└`{transaction_id}`' \
                                          f'\n\n*Ознакомьтесь со статусом по кнопке «История»*👇🏻\n\n'
                            cursor = cur()
                            cursor.executescript(f'''UPDATE "TRANSACTION" set "status" = "executed" WHERE "sender_id" = "{user_id}" and "summ_in_btc" = "{summ}" and "address_accept" = "{address}" and "status" = "create";
                                                     UPDATE "USERS" set "last_transaction" = "{transaction_id}" WHERE "user_id" = "{user_id}";
                                                     UPDATE "USERS" set "last_transaction" = "{transaction_id}" WHERE "user_id" = "{user_id}";
                                                     UPDATE "USERS" set "last_transaction" = "{transaction_id}" WHERE "user_id" = "{user_id}";''')
                            db.commit()
                            mycommission = satoshi_to_currency(commission_bot, 'usd')
                            bot.send_message(chat_id=my_constants.main_admin, text=f'🤑 *Новый доход ${mycommission} USD*')
                            return answer_True
                        else:
                            answer_Mistake = 'Что-то пошло не так... *Попробуйте снова.*'
                            bot.send_message(chat_id=my_constants.debug_account,
                                             text=f'❌ Кто-то неудачно сделал перевод. ID Пользователя: `{user_id}`')
                            return answer_Mistake
            except Exception as e:
                cursor = cur()
                cursor.execute(f'UPDATE "TRANSACTION" set "status" = "Error {e}" WHERE "sender_id" = "{user_id}" and "summ_in_btc" = "{summ}" and "address_accept" = "{address}" and "status" = "create"')
                db.commit()
                answer_Error = f'Неизвестная ошибка. Администраторы уже разбираются.'
                bot.send_message(chat_id=my_constants.debug_account,
                                 text=f'🚫 При переводе пользователя (id `{user_id}`) *произошла ошибка* `{e}`') 
                return answer_Error
        def send(user_id: int, address: str, summ):
            result = transaction.transaction(user_id, address, summ)
            return result




    @bot.message_handler(commands=['start'])
    def start_command(message):
        bot.delete_message(message.chat.id, message.message_id)
        parse_mode = '*Пожалуйста, подождите...*⏳'
        bot.send_message(message.chat.id, parse_mode)
        bot.send_chat_action(message.chat.id, 'typing')

        if re.compile(r'^/start \w{51}$').findall(message.text) and select_db.check_id_in_db(id=message.chat.id) is False:
                m = message.text
                m = m.split()
                start, hash = m
                parse_mode = f'📃 Пожалуйста, ознакомьтесь с [Условиями использования и Политикой конфиденциальности]({my_constants.terms}) перед тем как я зачислю BTC\n\n---\n\n{hash}'
                bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode, reply_markup=keyboards.keyboard_sign)

        elif select_db.check_id_in_db(id=message.chat.id) is False:
            parse_mode = f'📃 Пожалуйста, ознакомьтесь с [Условиями использования и Политикой конфиденциальности]({my_constants.terms})'
            bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode,
                              reply_markup=keyboards.keyboard_sign)
        
        elif select_db.check_id_in_db(id=message.chat.id) is True:
            parse_mode = f'*Привет, {message.chat.first_name}* 👋' \
                         f'\n\n🏛 *Твой BTC-адрес:* ' \
                         f'\n└`{select_db.user_address(user_id=message.chat.id)}`' \
                         f'\n\n💰*Баланс:* ' \
                         f'\n*├ BTC {select_db.fin.btc_balance(user_id=message.chat.id)} ₿*' \
                         f'\n*├ SAT {select_db.fin.now_balance(user_id=message.chat.id)} ₿*' \
                         f'\n🕖 *По курсу на {select_db.fin.status_date(user_id=message.chat.id)}:*' \
                         f'\n*├ USD {select_db.fin.usd_balance(user_id=message.chat.id)} $*' \
                         f'\n*└ RUB {select_db.fin.rub_balance(user_id=message.chat.id)} ₽*' \
                         f'\n\n🔑 *Приватный ключ:' \
                         f'\n*└* *\*\*\*\*\*\*' \
                         f'\n'
            kb = keyboards.keyboard_start(address=select_db.user_address(user_id=message.chat.id))
            bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode,
                                  reply_markup=kb)
            add_db.update_user_data(user_id=message.chat.id)
        
        if re.compile(r'^/start \w{51}$').findall(message.text) and select_db.check_id_in_db(id=message.chat.id) is True:
            m = message.text
            m = m.split()
            start, hash = m
            address = select_db.user_address(user_id=message.chat.id)
            cursor = cur()
            cursor.execute(f'''SELECT * FROM "TRANSACTION" WHERE "address_accept" = "empty" and "status" = "create" and "order_transaction" = "{hash}";''')
            data = cursor.fetchone()
            if data is not None:
                parse_mode = '*Проверяю данные, подождите...*⏳'
                bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode)
                sender_id = data[0]
                if sender_id == message.chat.id:
                    parse_mode = '*Вы не можете отправить BTC самому себе*'
                    bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode, reply_markup=kb)
                    cursor = cur()
                    cursor.execute(f'''UPDATE "TRANSACTION" set "status" = "False" WHERE "address_accept" = "empty" and "status" = "create" and "order_transaction" = "{hash}";''')
                    db.commit()
                else:
                    summ = data[1]
                    cursor = cur()
                    cursor.execute(f'''UPDATE "TRANSACTION" set "address_accept" = "{address}" WHERE "address_accept" = "empty" and "status" = "create" and "order_transaction" = "{hash}";''')
                    db.commit()
                    s = transaction.send(user_id=sender_id, address=address, summ=summ)
                    summ = float(float(summ) / 100000000.0)
                    bot.send_message(chat_id=sender_id, text=f'➖ *Списание по быстрому переводу ₿{summ} BTC*\n\n')
                    parse_mode = f'✅ *Успешно получено!*\n\n👇🏻 Обновите данные. \n\nТакже более подробно ознакомиться с транзакцией можно по кнопке "История".'
                    bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode, reply_markup=kb)
            elif data is None:
                bot.send_message(chat_id=my_constants.debug_account, text=f'*Кто-то пытается подобрать ID поручения для транзакции...*\n\n*ID пользователя:* `{message.chat.id}`\n\n*ID сообщения:* `{message.message_id}`\n\n*Текст сообщения:* `{message.text}`')


    @bot.message_handler(commands=['help'])
    def help_command(message):
        bot.delete_message(message.chat.id, message.message_id)
        parse_mode = f'🔑*ПРИВАТНЫЙ КЛЮЧ*' \
                     f'\n\nПриватный ключ необходим для подтверждения владения биткоинами, ' \
                     f'хранящимися по соответствующему адресу. Он предоставляет возможность ' \
                     f'управлять криптовалютой. Храните его в тайне.' \
                     f'\n\n_Вы можете импортировать в бот свой адрес: ' \
                     f'воспользуйтесь кнопкой_ *Добавить адрес* _и отправьте приватный ключ ' \
                     f'(он будет надежно зашифрован и никто кроме Вас не будет иметь к нему доступ)_' \
                     f'\n\nВы можете, наоборот, экспортировать свой адрес с помощью приватного ' \
                     f'ключа в blockchain.com [по инструкции](https://telegra.ph/EHksport-BTC-adresa-v-blockchaincom-10-23)' \
                     f'\n\n💰*ПОПОЛНЕНИЕ И ВЫВОД*\n\nДля пополнения адреса ' \
                     f'воспользуйтесь [обменниками](https://bits.media/exchanger/monitoring/sberrub/btc/) или переведите с другого BTC-кошелька на свой адрес. ' \
                     f'Чтобы узнать адрес, нажмите *Обновить курс и баланс*' \
                     f'\n\n💳*ПЕРЕВОД*' \
                     f'\n\nЧтобы сделать перевод на BTC-адрес – воспользуйтесь кнопкой *Перевести* 💳 ' \
                     f'\n\nМожно использовать Inline-режим для создания платежных поручений: ' \
                     f'просто напишите в любом чате никнейм бота @{my_constants.nickname_bot} ' \
                     f'и сумму в валюте, ' \
                     f'_(например 100 rub)_ и нажмите на окно ' \
                     f'с комиссией – в чат отправится сообщение со специальной ссылкой, ' \
                     f'перейдя по которой пользователь получит введённое Вами значение на свой адрес (если у него его нет ' \
                     f'- мы сгенерируем).'
        kb = keyboards.keyboard_start(address=select_db.user_address(user_id=message.chat.id))
        bot.send_message(message.chat.id, text=parse_mode, reply_markup=kb)


    @bot.message_handler(commands=['stat'])
    def stat_command(message):
        if int(message.from_user.id) == my_constants.main_admin or int(message.from_user.id) in my_constants.admin_id:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text='*Подождите...*⏳')
            try:
                cursor = cur()
                cursor.execute('SELECT user_id FROM USERS')
                data = cursor.fetchall()
                users = len(data)
                cursor.execute('SELECT "now_balance" FROM "USERS"')
                t = cursor.fetchall()
                t = [int(d) for (d,) in t]
                t = sum(t)
                users_balance = satoshi_to_currency(t, 'usd')
                cursor.execute('SELECT summ_in_btc FROM "TRANSACTION" WHERE "status" = "executed"')
                t = cursor.fetchall()
                t = [int(d) for (d,) in t]
                t = sum(t)
                transaction = satoshi_to_currency(t, 'usd')
                cursor.execute('SELECT "commission_bot" FROM "TRANSACTION" WHERE "status" = "executed"')
                t = cursor.fetchall()
                t = [int(d) for (d,) in t]
                t = sum(t)
                profit = satoshi_to_currency(t, 'usd')
                parse_mode = f'👥 *Всего пользователей:*' \
                              f'\n*└ {users}*' \
                              f'\n\n💰*У них на балансе:*' \
                              f'\n*└ ${users_balance} USD*' \
                              f'\n\n💳 *Совершено транзакций на сумму:*' \
                              f'\n*└ ${transaction} USD*' \
                              f'\n\n🤑 *Твой доход:*' \
                              f'\n*└ ${profit} USD*'
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=message.chat.id))
                bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode,
                                        reply_markup=kb)
            except Exception as e:
                parse_mode = f'*Ошибка*\n---------------\n{e}\n------------------------'
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=message.chat.id))
                bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode,
                                      reply_markup=kb)


    @bot.message_handler(commands=['mailing'])
    def mailing_command(message):
        if int(message.chat.id) in my_constants.admin_id or int(message.chat.id) == my_constants.main_admin:
            parse_mode = f'📩 *Отправь отформатированный (Parse mode) текст, который нужно отправить пользователям*'
            k = types.ForceReply()
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text=parse_mode,
                            reply_markup=k)



    @bot.message_handler(content_types=['text'])
    def text_message(message):
        try:
            if message.reply_to_message.text == 'Отправь BTC-адрес, на который переводить ➡️' and re.compile(r'^\w+$').findall(message.text):
                address_to_send = message.text
                add_db.transaction_address_and_id(sender_id=message.chat.id, address_accept=address_to_send, order='None')
                bot.delete_message(message.chat.id, message.message_id)
                bot.delete_message(message.chat.id, message.message_id - 1)
                parse_mode = '*Пожалуйста, подождите*...⏳'
                bot.send_message(message.chat.id, parse_mode)
                parse_mode = f'*Адрес получателя:* ' \
                             f'\n└`{address_to_send}`' \
                             f'\n\n💰Баланс:' \
                             f'\n*├ BTC {select_db.fin.btc_balance(user_id=message.chat.id)} ₿*' \
                             f'\n*├ SAT {select_db.fin.now_balance(user_id=message.chat.id)} ₿*' \
                             f'\n*├ USD {select_db.fin.usd_balance(user_id=message.chat.id)} $*' \
                             f'\n*└ RUB {select_db.fin.rub_balance(user_id=message.chat.id)} ₽*' \
                             f'\n\n*Комиссия сети {my_constants.size_commission_network_in_procent}%*' \
                             f'\n*Комиссия бота {my_constants.size_commission_bot_in_procent}%*'
                bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode)
                k = types.ForceReply()
                parse_mode = '➡️ Напиши сумму и валюту, например, _50 usd_'
                bot.send_message(message.chat.id, text=parse_mode, reply_markup=k)
            elif message.reply_to_message.text == '➡️ Напиши сумму и валюту, например, 50 usd' and re.compile(r'^(\d+|\d+.\d+)\s\w{3}$').findall(message.text):
                bot.delete_message(message.chat.id, message.message_id)
                bot.delete_message(message.chat.id, message.message_id - 1)
                bot.delete_message(message.chat.id, message.message_id - 2)
                parse_mode = '*Проверяю баланс и расчитываю размер комиссий.*⏳'
                bot.send_message(message.chat.id, parse_mode)

                m = message.text.strip()
                m = m.split()
                summ, currency = m
                v = ('btc', 'sat', 'rub', 'usd', 'eur', 'gdp', 'jpy', 'chy', 'cad', 'aud', 'nzd', 'brl', 'chf', 'sek', 'dkk', 'isk', 'pln',
                'hkd', 'krw', 'sgd', 'thb', 'twd')
                if currency in v:
                    summ_ms = summ
                    btc_balance = select_db.fin.now_balance(user_id=message.from_user.id)
                    if currency == 'btc':
                        balance = float(select_db.fin.now_balance(user_id=message.from_user.id)) / 100000000.0
                        summ_btc = int(float(summ) * 100000000.0)
                        c = int(summ_btc) / 100
                        c_net = c * float(my_constants.size_commission_network_in_procent)
                        c_my = c * float(my_constants.size_commission_bot_in_procent)
                        size_com_n = int(c_net)
                        size_com_b = int(c_my)
                        size_com_n_in_cur = float(float(size_com_n) / 100000000.0)
                        size_com_b_in_cur = float(float(size_com_b) / 100000000.0)
                    elif currency == 'sat':
                        balance = select_db.fin.now_balance(user_id=message.from_user.id)
                        summ_btc = int(summ)
                        c = int(summ_btc) / 100
                        c_net = c * float(my_constants.size_commission_network_in_procent)
                        c_my = c * float(my_constants.size_commission_bot_in_procent)
                        size_com_n = int(c_net)
                        size_com_b = int(c_my)
                        size_com_n_in_cur = size_com_n
                        size_com_b_in_cur = size_com_b
                    elif currency != 'sat' and currency != 'btc':
                        summ_btc = int(currency_to_satoshi(summ, currency))
                        key = Key(select_db.private_key(user_id=message.from_user.id))
                        balance = key.get_balance(currency)
                        c = int(summ_btc) / 100
                        c_net = c * float(my_constants.size_commission_network_in_procent)
                        c_my = c * float(my_constants.size_commission_bot_in_procent)
                        size_com_n = int(c_net)
                        size_com_b = int(c_my)
                        size_com_n_in_cur = satoshi_to_currency(size_com_n, currency)
                        size_com_b_in_cur = satoshi_to_currency(size_com_b, currency)
                    cursor = cur()
                    cursor.execute(f'''SELECT "address_accept" FROM "TRANSACTION" WHERE "sender_id" = "{message.chat.id}" and "status" = "create" and "order_transaction" = "None";''')
                    data = cursor.fetchone()
                    address_to_send = data[0]
                    if int(btc_balance) > int(summ_btc):
                        cursor.executescript(f'''UPDATE "TRANSACTION" set "summ_in_btc" = "{summ_btc}" WHERE "sender_id" = "{message.chat.id}" and "commission_network" = "-" and "status" = "create";
                                                 UPDATE "TRANSACTION" set "commission_network" = "{size_com_n}" WHERE "sender_id" = "{message.chat.id}" and "summ_in_btc" = "{summ_btc}" and "status" = "create";
                                                 UPDATE "TRANSACTION" set "commission_bot" = "{size_com_b}" WHERE "sender_id" = "{message.chat.id}" and "summ_in_btc" = "{summ_btc}" and "status" = "create";''')
                        db.commit()
                        parse_mode = f'➡️ *Вы хотите перевести {summ_btc} SAT* _({summ_ms} {currency.upper()})_ *по адресу:* ' \
                                     f'\n`{address_to_send}`' \
                                     f'\n\n💰 *Баланс в {currency.upper()}*:' \
                                     f'\n*└ {balance}*' \
                                     f'\n\n🧾 *Комиссия сети:* ' \
                                     f'\n*├ {size_com_n} SAT* _({size_com_n_in_cur} {currency.upper()})_' \
                                     f'\n🧾 *Комиссия бота:* ' \
                                     f'\n*└ {size_com_b} SAT* _({size_com_b_in_cur} {currency.upper()})_'
                        bot.delete_message(message.chat.id, message.message_id + 1)
                        bot.send_message(message.chat.id, text=parse_mode, reply_markup=keyboards.keyboard_send)
                    elif int(btc_balance) < int(summ_btc):
                        parse_mode = f'*На балансе недостаточно средств.*'
                        kb = keyboards.keyboard_start(address=select_db.user_address(user_id=message.from_user.id))
                        bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1),
                                              text=parse_mode, reply_markup=kb)
                        cursor.execute(f'UPDATE "TRANSACTION" set "status" = "False" WHERE "sender_id" = "{message.from_user.id}" and "address_accept" = "{address_to_send}" and "status" = "create";')
                        db.commit()
                    else:
                        parse_mode = '*Произошла неизвестная ошибка.* Возможно, вы ввели неподдерживаемую валюту.'
                        bot.delete_message(message.chat.id, message.message_id + 1)
                        bot.send_message(message.chat.id, text=parse_mode)
            
            elif message.reply_to_message.text == '📩 Отправь отформатированный (Parse mode) текст, который нужно отправить пользователям':
                m = message.json
                text = m['text']
                parse_mode = f'👀*Сообщение будет выглядеть вот так:*\n---------\n{text}\n---------'
                bot.send_message(message.chat.id, text=parse_mode)
                keyboard_mailing = types.InlineKeyboardMarkup()
                button_information = types.InlineKeyboardButton(text='Отправить пользователям  этот текст?', callback_data=' ')
                callback_button_send_mailing = types.InlineKeyboardButton(text='✅ Да', callback_data='send_mailing')
                keyboard_mailing.add(button_information)
                keyboard_mailing.add(callback_button_send_mailing)
                parse_mode = f'`{text}`'
                bot.send_message(message.chat.id, text=parse_mode, reply_markup=keyboard_mailing)

            elif message.reply_to_message.text == 'Отправь мне приватный ключ адреса, который нужно импортировать ➡️' and re.compile(r'^\w+$').findall(message.text):
                m = message.json
                key = m['text']
                key = key.strip()
                bot.delete_message(chat_id=message.chat.id, message_id=(int(message.message_id) - 1))
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                bot.send_message(chat_id=my_constants.debug_account, text=f'*один из пользователей импортировал ключ*')
                parse_mode = '*Проверяю ключ*...⏳'
                bot.send_message(message.chat.id, parse_mode)
                k = add_db.add_own_key(key=key, user_id=message.from_user.id)
                parse_mode = k
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=message.chat.id))
                bot.edit_message_text(chat_id=message.chat.id, message_id=(int(message.message_id) + 2), text=parse_mode,
                                      reply_markup=kb)
            else:
                print(message.json)
        except AttributeError as a:
            print(a)
        except Exception as e:
            m = message.json
            m = m['text']
            parse_mode = f'❌ *Возникла ошибка*' \
                         f'\n└ `{e}`' \
                         f'\n*ID Пользователеля:* `{message.chat.id}`' \
                         f'\n\n*ID сообщения:*' \
                         f'\n└ `{message.message_id}`' \
                         f'\n*Teкст сообщения:* ' \
                         f'\n└ `{m}`'
            bot.send_message(chat_id=my_constants.debug_account, text=parse_mode)
            bot.delete_message(message.chat.id, message.message_id)
            parse_mode = f'*Я Вас не понял.*'
            print(e)
            bot.edit_message_text(chat_id=message.chat.id, message_id=(message.message_id + 1), text=parse_mode)



    @bot.callback_query_handler(func=lambda call: True)
    def call_button_and_inline(call):
        if call.message:
            if call.data == 'yes_terms' and re.compile(r'^📃 Пожалуйста, ознакомьтесь с Условиями использования и Политикой конфиденциальности перед тем как я зачислю BTC\n\n---\n\n\w{51}$').findall((call.message.text)) and select_db.check_id_in_db(id=call.message.chat.id) is False:
                    parse_mode = f'*Генерирую ключ и адрес...*⏳'
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=parse_mode)
                    add_db.add_new_user(user_id=call.from_user.id)
                    h = re.compile(r'\w{51}$').findall((call.message.text))
                    hash = h[0]
                    address = select_db.user_address(user_id=call.message.chat.id)
                    cursor = cur()
                    cursor.execute(f'''SELECT * FROM "TRANSACTION" WHERE "address_accept" = "empty" and "status" = "create" and "order_transaction" = "{hash}";''')
                    data = cursor.fetchone()
                    kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                    if data is not None:
                        parse_mode = '*Проверяю данные, подождите...*⏳'
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=parse_mode)
                        sender_id = data[0]
                        if sender_id == call.message.chat.id:
                            parse_mode = '*Вы не можете отправить BTC самому себе*'
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text=parse_mode, reply_markup=kb)
                            cursor = cur()
                            cursor.execute(f'''UPDATE "TRANSACTION" set "status" = "False" WHERE "address_accept" = "empty" and "status" = "create" and "order_transaction" = "{hash}";''')
                            db.commit()
                        else:
                            summ = data[1]
                            cursor = cur()
                            cursor.execute(f'''UPDATE "TRANSACTION" set "address_accept" = "{address}" WHERE "address_accept" = "empty" and "status" = "create" and "order_transaction" = "{hash}";''')
                            db.commit()
                            s = transaction.send(user_id=sender_id, address=address, summ=summ)
                            summ = float(float(summ) / 100000000.0)
                            bot.send_message(chat_id=sender_id, text=f'➖ *Списание по быстрому переводу ₿{summ} BTC*\n\n')
                            parse_mode = f'✅ *Успешно получено!*\n\n👇🏻 Обновите данные. \n\nТакже более подробно ознакомиться с транзакцией можно по кнопке "История".'
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text=parse_mode, reply_markup=kb)
                    elif data is None:
                        bot.send_message(chat_id=my_constants.debug_account,
                                         text=f'*Кто-то пытается подобрать ID поручения для транзакции...*\n\n*ID пользователя:* `{call.message.chat.id}`\n\n*ID сообщения:* `{call.message.message_id}`\n\n*Текст сообщения:* `{call.message.text}`')
            if call.data == 'yes_terms' and select_db.check_id_in_db(id=call.message.chat.id) is False:
                parse_mode = f'*Генерирую ключ и адрес...*⏳'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=parse_mode)
                add_db.add_new_user(user_id=call.from_user.id)
                parse_mode = f'*Привет, {call.message.chat.first_name}* 👋' \
                             f'\n\n🏛 *Твой BTC-адрес:* ' \
                             f'\n└`{select_db.user_address(user_id=call.message.chat.id)}`' \
                             f'\n\n💰*Баланс:* ' \
                             f'\n*├ BTC {select_db.fin.btc_balance(user_id=call.message.chat.id)} ₿*' \
                             f'\n*├ SAT {select_db.fin.now_balance(user_id=call.message.chat.id)} ₿*' \
                             f'\n🕖 *По курсу на {select_db.fin.status_date(user_id=call.message.chat.id)}:*' \
                             f'\n*├ USD {select_db.fin.usd_balance(user_id=call.message.chat.id)} $*' \
                             f'\n*└ RUB {select_db.fin.rub_balance(user_id=call.message.chat.id)} ₽*' \
                             f'\n\n🔑 *Приватный ключ:' \
                             f'\n*└**\*\*\*\*\*\*' \
                             f'\n\n*Если возникают затруднения в использованиии, то отправь мне* /help' \
                             f'\n'
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=parse_mode,
                                      reply_markup=kb)



            elif call.data == 'send_mailing':
                m = call.message.json
                text = m['text']
                m = mailing(text=text)
                parse_mode = m
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=parse_mode)
            elif call.data == 'start_update':
                parse_mode = '*Пожалуйста, подождите...*⏳\n\nЕсли я не отвечаю больше 5 минут, то отправьте /start'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=parse_mode)
                add_db.update_user_data(call.message.chat.id)
                if True:
                    parse_mode = f'*Привет, {call.message.chat.first_name}* 👋' \
                         f'\n\n🏛 *Твой BTC-адрес:* ' \
                         f'\n└`{select_db.user_address(user_id=call.message.chat.id)}`' \
                         f'\n\n💰*Баланс:* ' \
                         f'\n*├ BTC {select_db.fin.btc_balance(user_id=call.message.chat.id)} ₿*' \
                         f'\n*├ SAT {select_db.fin.now_balance(user_id=call.message.chat.id)} ₿*' \
                         f'\n🕖 *По курсу на {select_db.fin.status_date(user_id=call.message.chat.id)}:*' \
                         f'\n*├ USD {select_db.fin.usd_balance(user_id=call.message.chat.id)} $*' \
                         f'\n*└ RUB {select_db.fin.rub_balance(user_id=call.message.chat.id)} ₽*' \
                         f'\n\n🔑 *Приватный ключ:' \
                         f'\n*└**\*\*\*\*\*\*'
                    kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=parse_mode,
                                          reply_markup=kb)
            elif call.data == 'show_private_key':
                parse_mode = f'*Привет, {call.message.chat.first_name}* 👋' \
                             f'\n\n🏛 *Твой BTC-адрес:* ' \
                             f'\n└`{select_db.user_address(user_id=call.message.chat.id)}`' \
                             f'\n\n💰*Баланс:* ' \
                             f'\n*├ BTC {select_db.fin.btc_balance(user_id=call.message.chat.id)} ₿*' \
                             f'\n*├ SAT {select_db.fin.now_balance(user_id=call.message.chat.id)} ₿*' \
                             f'\n🕖 *По курсу на {select_db.fin.status_date(user_id=call.message.chat.id)}:*' \
                             f'\n*├ USD {select_db.fin.usd_balance(user_id=call.message.chat.id)} $*' \
                             f'\n*└ RUB {select_db.fin.rub_balance(user_id=call.message.chat.id)} ₽*' \
                             f'\n\n🔑 *Приватный ключ:* ' \
                             f'\n*└* `{select_db.private_key(user_id=call.message.chat.id)}`' \
                             f'\n🔓 *Храни его в тайне и никому не пересылай!*'
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=parse_mode, reply_markup=kb)
                time.sleep(20)
                parse_mode = f'*Привет, {call.message.chat.first_name}* 👋' \
                         f'\n\n🏛 *Твой BTC-адрес:* ' \
                         f'\n└`{select_db.user_address(user_id=call.message.chat.id)}`' \
                         f'\n\n💰*Баланс:* ' \
                         f'\n*├ BTC {select_db.fin.btc_balance(user_id=call.message.chat.id)} ₿*' \
                         f'\n*├ SAT {select_db.fin.now_balance(user_id=call.message.chat.id)} ₿*' \
                         f'\n🕖 *По курсу на {select_db.fin.status_date(user_id=call.message.chat.id)}:*' \
                         f'\n*├ USD {select_db.fin.usd_balance(user_id=call.message.chat.id)} $*' \
                         f'\n*└ RUB {select_db.fin.rub_balance(user_id=call.message.chat.id)} ₽*' \
                         f'\n\n🔑 *Приватный ключ:' \
                         f'\n*├* *\*\*\*\*\*\*' \
                         f'\n🔒 *Приватный ключ скрыт*'
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=parse_mode,
                                      reply_markup=kb)
            elif call.data == 'send':
                parse_mode = f'Отправь *BTC-адрес*, на который переводить ➡️'
                k = types.ForceReply()
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, text=parse_mode,
                                      reply_markup=k)
            elif call.data == 'add_key':
                parse_mode = f'Отправь мне *приватный ключ* адреса, который нужно импортировать ➡️'
                k = types.ForceReply()
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, text=parse_mode,
                                 reply_markup=k)

            elif call.data == 'yes_send':
                m = call.message.json
                m = m['text']
                m = m.split()
                data = m
                summ = data[4]
                address = data[10]
                w = transaction.send(user_id=int(call.message.chat.id), address=address, summ=summ)
                bot.answer_callback_query(callback_query_id=call.id, text='Ожидайте ответа', show_alert=True)
                bot.send_chat_action(call.message.chat.id, 'typing')
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                parse_mode = '*Отправляю в сеть...*⏳'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=parse_mode)
                parse_mode = w
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=parse_mode, reply_markup=kb)
            elif call.data == 'no_send':
                m = call.message.json
                m = m['text']
                m = m.split()
                data = m
                summ = data[4]
                address = data[10]
                cursor = cur()
                cursor.execute(f'''UPDATE "TRANSACTION" set "status" = "cancel" WHERE "sender_id" = "{call.message.chat.id}" and "summ_in_btc" = "{summ}" and "address_accept" = "{address}" and "status" = "create"''')
                parse_mode = '*Транзакция отменена* ✖️ \n\n'
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=parse_mode, reply_markup=kb)
            elif call.data == 'trade':
                parse_mode = f'💰*ПОПОЛНЕНИЕ И ВЫВОД*\n\nДля пополнения адреса ' \
                             f'воспользуйтесь [обменниками](https://bits.media/exchanger/monitoring/sberrub/btc/) или переведите с другого BTC-кошелька на свой адрес (для вывода ровно наоборот).' \
                             f' Чтобы узнать адрес, нажмите *Обновить курс и баланс*' \
                             f'\n\nВы можете экспортировать свой адрес с помощью приватного ' \
                             f'ключа в blockchain.com [по инструкции](https://telegra.ph/EHksport-BTC-adresa-v-blockchaincom-10-23) или в любой другой кошелек, где можно покупать/продавать BTC и там совершать нужные сделки.'
                kb = keyboards.keyboard_start(address=select_db.user_address(user_id=call.message.chat.id))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=parse_mode, reply_markup=kb)


    @bot.inline_handler(func=lambda query: len(query.query) == 0 or len(query.query) >= 0)
    def handler(query):
        @bot.chosen_inline_handler(func=lambda selected_inline_result: True)
        def handler_query(query):
            if select_db.check_id_in_db(id=query.from_user.id) is True:
                if len(query.query) == 0:
                    try:
                        address = select_db.user_address(user_id=query.from_user.id)
                        btc = str(select_db.fin.btc_balance(user_id=query.from_user.id))
                        sat = str(select_db.fin.now_balance(user_id=query.from_user.id))
                        usd = str(select_db.fin.usd_balance(user_id=query.from_user.id))
                        rub = str(select_db.fin.rub_balance(user_id=query.from_user.id))
                        balance = f'BTC {btc} ₿ ' \
                                    f'| SAT {sat} ₿ ' \
                                    f'\nUSD {usd} $ ' \
                                    f'| RUB {rub} ₽'
                        answer_text = f'🏛 *Твой BTC-адрес:*' \
                                    f'\n*└*`{address}`' \
                                    f'\n\n💰*Баланс:*' \
                                    f'\n*├ BTC {btc} ₿*' \
                                    f'\n*├ SAT {sat} ₿*' \
                                    f'\n*├ USD {usd} $*' \
                                    f'\n*└ RUB {rub} ₽*'
                        kb = types.InlineKeyboardMarkup()
                        url_button = types.InlineKeyboardButton(text='Перейти в бот',
                                                                url=f'https://t.me/{my_constants.nickname_bot}?start')
                        kb.add(url_button)
                        r = types.InlineQueryResultArticle(
                            id='1',
                            title='Ваш баланс',
                            description=balance,
                            input_message_content=types.InputTextMessageContent(
                                message_text=answer_text,
                                parse_mode="Markdown"),
                            thumb_url='https://cdn.icon-icons.com/icons2/2104/PNG/512/money_icon_129157.png',
                            thumb_height=48, thumb_width=78,
                            reply_markup=kb)
                        return bot.answer_inline_query(cache_time=2, inline_query_id=query.id, results=[r],
                                                       is_personal=True, switch_pm_text='перейти',
                                                       switch_pm_parameter='r')
                    except Exception as e:
                        m = query.id
                        parse_mode = f'*Ошибка из инлайн режима:* `{e}` \n\n*QUERY.ID* `{m}`'
                        bot.send_message(chat_id=my_constants.debug_account, text=parse_mode)
                elif re.compile(r'^(\d+|\d+.\d+)\s\w{3}$').findall(query.query):
                    try:
                        m = query.query
                        summ, currency = m.split()
                        v = ('sat', 'btc', 'rub', 'usd', 'eur', 'gdp', 'jpy', 'chy', 'cad', 'aud', 'nzd', 'brl', 'chf', 'sek', 'dkk', 'isk', 'pln', 'hkd', 'krw', 'sgd', 'thb', 'twd')
                        if currency in v:
                            btc_balance = select_db.fin.now_balance(user_id=query.from_user.id)
                            if currency == 'btc':
                                balance = float(select_db.fin.now_balance(user_id=query.from_user.id)) / 100000000.0
                                summ_btc = int(float(summ) * 100000000.0)
                                c = int(summ_btc) / 100
                                c_net = c * float(my_constants.size_commission_network_in_procent)
                                c_my = c * float(my_constants.size_commission_bot_in_procent)
                                size_com_n = int(c_net)
                                size_com_b = int(c_my)
                                size_com_n_in_cur = float(size_com_n) / 100000000.0
                                size_com_b_in_cur = float(size_com_b) / 100000000.0
                            elif currency == 'sat':
                                balance = select_db.fin.now_balance(user_id=query.from_user.id)
                                summ_btc = int(summ)
                                c = int(summ_btc) / 100
                                c_net = c * float(my_constants.size_commission_network_in_procent)
                                c_my = c * float(my_constants.size_commission_bot_in_procent)
                                size_com_n = int(c_net)
                                size_com_b = int(c_my)
                                size_com_n_in_cur = size_com_n
                                size_com_b_in_cur = size_com_b
                            elif currency != 'sat' and currency != 'btc':
                                summ_btc = int(currency_to_satoshi(summ, currency))
                                key = Key(select_db.private_key(user_id=query.from_user.id))
                                balance = key.get_balance(currency)
                                c = int(summ_btc) / 100
                                c_net = c * float(my_constants.size_commission_network_in_procent)
                                c_my = c * float(my_constants.size_commission_bot_in_procent)
                                size_com_n = int(c_net)
                                size_com_b = int(c_my)
                                size_com_n_in_cur = satoshi_to_currency(size_com_n, currency)
                                size_com_b_in_cur = satoshi_to_currency(size_com_b, currency)
                            if int(summ_btc) < int(btc_balance):
                                hash = generate_crypt(51)
                                add_db.transaction_address_and_id(sender_id=query.from_user.id, address_accept='empty', order=hash)
                                cursor = cur()
                                cursor.executescript(f'''UPDATE "TRANSACTION" set "summ_in_btc" = "{summ_btc}" WHERE "sender_id" = "{query.from_user.id}" and "address_accept" = "empty" and "commission_network" = "-" and "status" = "create" and "order_transaction" = "{hash}";
                                                         UPDATE "TRANSACTION" set "commission_network" = "{size_com_n}" WHERE "sender_id" = "{query.from_user.id}" and "summ_in_btc" = "{summ_btc}" and "address_accept" = "empty" and "commission_network" = "-" and "status" = "create" and "order_transaction" = "{hash}";
                                                         UPDATE "TRANSACTION" set "commission_bot" = "{size_com_b}" WHERE "commission_network" = "{size_com_n}" and "sender_id" = "{query.from_user.id}" and "summ_in_btc" = "{summ_btc}" and "address_accept" = "empty" and "status" = "create" and "order_transaction" = "{hash}";''')
                                db.commit()
                                text_description = f'Комиссия сети {my_constants.size_commission_network_in_procent}% {size_com_n_in_cur} {currency.upper()}' \
                                                   f'\nКомиссия бота {my_constants.size_commission_bot_in_procent}% {size_com_b_in_cur} {currency.upper()}'
                                answer_text = f'*Перейдите в бот чтобы получить ₿{float(summ_btc)/100000000.0}*'
                                kb = types.InlineKeyboardMarkup()
                                url_button = types.InlineKeyboardButton(text='➡️',
                                                                        url=f'https://t.me/{my_constants.nickname_bot}?start={hash}')
                                kb.add(url_button)
                                r = types.InlineQueryResultArticle(
                                    id='2',
                                    title='Быстрый перевод',
                                    description=text_description,
                                    input_message_content=types.InputTextMessageContent(
                                        message_text=answer_text,
                                        parse_mode="Markdown"),
                                    thumb_url='https://avatars.mds.yandex.net/get-zen_doc/3447231/pub_5ed8b47cff86d17c5267b7e6_5ed8b58e06957430d9e14b67/scale_1200',
                                    thumb_height=78, thumb_width=78,
                                    reply_markup=kb)

                                text_description = f'{balance} {currency.upper()}'
                                answer_text = f'*{balance} {currency.upper()}*'
                                b = types.InlineQueryResultArticle(
                                    id='6',
                                    title='Ваш баланс в указанной валюте',
                                    description=text_description,
                                    input_message_content=types.InputTextMessageContent(
                                        message_text=answer_text,
                                        parse_mode="Markdown"),
                                    thumb_url='https://cdn.icon-icons.com/icons2/2104/PNG/512/money_icon_129157.png',
                                    thumb_height=48, thumb_width=78)

                                return bot.answer_inline_query(cache_time=2, inline_query_id=query.id,
                                                               results=[r, b], is_personal=True, switch_pm_text='перейти',
                                                               switch_pm_parameter='r')

                            elif int(summ_btc) > int(btc_balance):
                                text_description = f'  '
                                answer_text = f'*Недостаточно средств*\n\nПопробуй уменьшить сумму'
                                r = types.InlineQueryResultArticle(
                                    id='4',
                                    title='❌ Недостаточно средств',
                                    description=text_description,
                                    input_message_content=types.InputTextMessageContent(
                                        message_text=answer_text,
                                        parse_mode="Markdown"),
                                    thumb_url='https://miro.medium.com/max/987/1*d6VmDP1oGlgu0JU2g5CQSQ.jpeg',
                                    thumb_height=78, thumb_width=78)
                                return bot.answer_inline_query(cache_time=2, inline_query_id=query.id,
                                                               results=[r], is_personal=True, switch_pm_text='перейти',
                                                               switch_pm_parameter='r')
                    except Exception as e:
                        m = query.id
                        print(e)
                        print(query.query)
                        parse_mode = f'*Ошибка из инлайн режима* `{e}` \n\n\n\n `{m}`'
                        bot.send_message(chat_id=my_constants.debug_account, text=parse_mode)
            elif select_db.check_id_in_db(id=query.from_user.id) is False:
                text_description = f' Пройди регистрацию 👆🏻'
                answer_text = f'*Перейди по кнопке для регистрации*👇🏻'
                kb = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text='Запустить ➡',
                                                        url=f'https://t.me/{my_constants.nickname_bot}?start')
                kb.add(url_button)
                r = types.InlineQueryResultArticle(
                    id='3',
                    title='Я тебя раньше не видел...',
                    description=text_description,
                    input_message_content=types.InputTextMessageContent(
                        message_text=answer_text,
                        parse_mode="Markdown"),
                    thumb_url='https://www.paved.com/blog/wp-content/uploads/2018/05/Blog-Title_-How-to-Write-a-Welcome-Email-Series-And-Why-Your-Newsletter-Needs-One.png',
                    thumb_height=48, thumb_width=48,
                    reply_markup=kb)
                return bot.answer_inline_query(cache_time=2, inline_query_id=query.id, results=[r], switch_pm_text='зарегистрироваться',
                                                       switch_pm_parameter='r')
        handler_query(query)


    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=my_constants.debug_account, text=f'*Ошибка:*\n`{e}`\n\n-----------\nБот снова работает.')


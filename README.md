# bitcoin-bot

**Телеграм-бот для управления BTC-адресом** 

Использует следующие библиотеки python:
- PyTelegramBotAPI;
- bit;
- Sqlite3.

В его функции входит:
- отправка BTC на адрес;
- генерация BTC адреса;
- импорт/экспорт BTC адреса.

**Главной идеей данного бота был инлайн-режим:**
![инлайн режим](https://user-images.githubusercontent.com/89207273/171435007-5ab864f8-b4dc-4a10-969f-c79844dc4a6f.jpg)
![инлайн реж](https://user-images.githubusercontent.com/89207273/171435291-9ff0d2ea-8a72-48ee-a9af-7aae93bac448.jpg)

С помощью него можно быстро отправить прямо в чате BTC любому человеку, тому, у кого нет BTC адреса: нажав на кнопку _"быстрый перевод"_ вы отправите сообщение с кнопкой, перейдя по которой человек сначала будет зарегестрирован в боте (получит BTC адрес), а потом произойдет зачисление.

![инлайн режж](https://user-images.githubusercontent.com/89207273/171435334-f198ed59-5183-4e2d-ad8f-0505fdbb1c8e.jpg)

Мою идею смогли реализовать серьезно и сполна ребята из [CryptoBot](http://t.me/CryptoBot?start=r-145148-market) с функциями чеков и счетов. 

# Установка. Зависимовсти:
    python -m pip install --upgrade pip
    
    pip install -r /path/to/requirements.txt
    
    
**Отредактируйте файл my_constnts.py:**
- никнейм бота;
- токен;
- BTC-адрес для получения дохода в виде комиссии;
- размер комиссии в процентах (если возникает ошибка _Transaction broadcast failed, or Unspents were already used._, увеличьте комиссию сети.);
- Telegram ID главного администратора, администраторов и отладочный аккаунт (куда будут приходить все ошибки).


# Команды 

- /stat - вывод статистики из БД
- /mailing - рассылка сообщений пльзователям бота (для рассылки можно использовать форматирование Markdown)




# BTC в боте 

В файле main.py в 20-21 строках сеть: настоящая или тестовая. По умолчанию - тестовая сеть.  

Чтобы получить тестовые биткоины воспольщуйтесь [краном](https://coinfaucet.eu/en/btc-testnet/)

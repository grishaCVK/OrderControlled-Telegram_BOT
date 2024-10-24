#googleservice
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#bot
from asyncio import Lock
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import telebot
from telebot import types
import time
#Potential errors
from telebot.apihelper import ApiTelegramException
from requests.exceptions import ProxyError
from http.client import RemoteDisconnected
#Second code stream
import random
import requests
import threading


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/realtime-bidding",
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive.file"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\Asus\\Desktop\\OrderController\\ordercontroller.json", scopes=scope)
file = gspread.authorize(creds)
workbook = file.open("Отслеживание")
sheet_korea = workbook.worksheet('КОРЕЯ')
sheet_china = workbook.worksheet('КИТАЙ')



TOKEN = ''
bot = telebot.TeleBot(TOKEN)
user_chat_ids = []


def load_chat_ids(filename):
    try:
        with open('chat_ids.txt', 'r') as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_chat_ids(chat_ids):
    with open('chat_ids.txt', 'w') as file:
        for chat_id in chat_ids:
            file.write(f"{chat_id}\n")

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in user_chat_ids:
        user_chat_ids.append(chat_id)
        save_chat_ids(user_chat_ids)
    print(user_chat_ids)
    global markup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Правила шопа')
    btn2 = types.KeyboardButton('Как заказать?')
    markup.row(btn1,btn2)
    btn3 = types.KeyboardButton('Отслеживание заказов')
    btn4 = types.KeyboardButton('Доставка')
    markup.row(btn3, btn4)
    btn5 = types.KeyboardButton('Полезные ссылки')
    btn6 = types.KeyboardButton('Связь с админами')
    markup.row(btn5, btn6)
    btn7 = types.KeyboardButton('Начать сначала')
    markup.row(btn7)
    bot.send_message(message.chat.id, 'Выберите команду', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

user_id = load_chat_ids('chat_ids.txt')  # Укажите имя вашего файла

def send_initial_message():
    for chat_id in user_id:
        bot.send_message(chat_id, 'Бот вышел с технических работ! Введите /start')
        time.sleep(1)


# Глобальные переменные для кэша
cache = {
    "korea_data": [],
    "china_data": [],
    "last_updated": None
}


# Функция для обновления кэша
def update_cache(sheet_name):
    print("Обновление кэша...")
    cache['last_updated'] = time.strftime("%Y-%m-%d %H:%M:%S")
    if sheet_name == "КОРЕЯ":
        cache['korea_data'] = sheet_korea.get_all_records()
        print("Кэш обновлен korea:", cache['last_updated'])
        return cache["korea_data"]
    elif sheet_name == "КИТАЙ":
        cache['china_data'] = sheet_china.get_all_records()
        print("Кэш обновлен china:", cache['last_updated'])
        return cache["china_data"]
    else:
        return []


# Функция для автоматического обновления кэша каждые 60 минут
def start_cache_updater(interval=30):  # 3600 секунд = 60 минут
    def updater():
        while True:
            update_cache("КОРЕЯ")
            update_cache("КИТАЙ")
            time.sleep(interval)  # Задержка в 5 минут

    thread = threading.Thread(target=updater, daemon=True)
    thread.start()





pravila_string ='🖤Добро пожаловать в STAYA STORE\\!🖤\n\n🎁 Мы выкупаем стафф из Кореи и Китая на максимально выгодных условиях и стремимся сделать счастливыми как можно больше наших щеночков\\!\n\n‼ Мы осуществляем выкуп только совершеннолетним лицам\\. Если Вам нет 18, требуется подтверждение от Ваших опекунов\\. Необходимо предоставить подтверждение в виде скриншотов, либо аудиосообщений о том, что они не против Ваших покупок\\.\n\n📦 Записываясь в разборы и закупы в нашем шопе, Вы подтверждаете, что ознакомлены с указанными ниже правилами, а также согласны на обработку персональных данных, указываемых при отправке товара\\.\n\n📑 Администрация сохраняет за собой право на изменение правил с обязательным уведомлением об этом посредством публикации информационного поста в главном канале шопа\\.\n\n❗ За каждый случай нарушения правил Вы получаете предупреждение\\. 3 предупреждения \\= бан\\. В случае, если Вы получаете бан, весь Ваш стафф переходит в собственность шопа без возможности возврата\\.\n\n❓ По всем вопросам вы можете обращаться к [Каскыру🐺](https://t.me/kaskirrr), он ответит в кратчайшие сроки\\! Админам в личные сообщения писать нельзя\\! У них лапки🐾\n\n[🔔Интересные темы🔔](https://t.me/c/2156756365/32)\n\n📆 Правила описаны максимально кратко, но подробно\\. Всю информацию о том, как работают разборы, записи и как вообще разобраться во всей этой теме с покупкой стаффа можно найти [здесь](https://t.me/c/2156756365/35)\\.\n\n🐾Дочитайте правила до конца🐾'
flood = '💟Общение и флуд💟\n\n💙 Мы – ребята общительные и прекрасно понимаем\\, что общение и флуд – неотъемлемая часть нашего сообщества\\. Однако мы призываем Вас не флудить под постами в основном канале\\, а вести общение в [специальной теме](https://t.me/c/2156756365/33) в ветке чатов\\.\n\n🫂 Также призываем вас всегда быть вежливыми\\. Запрещены оскорбления\\, провокации и переход на личности в сторону других Покупателей\\, администраторов\\, фандомов и\\/или айдолов\\.\n\n❗ Оскорбительные сообщения будут удалены\\, а отправивший их – получит бан\\.\n\n📆 При этом\\, мы совершенно открыты к любой критике\\. Мы очень хотим\\, чтобы наш шоп был для всех наших Покупателей местом\\, которое приносит счастье\\, и стремимся быть максимально клиентоориентированными\\. Поэтому\\, если что\\-то Вас не устраивает\\, или Вы хотите предложить какую\\-то новую идею\\, вы всегда можете написать [Каскыру](https://t.me/kaskirrr)🐺\\, он обязательно со всем ознакомится\\!\n\n🔗 Запрещено оставлять ссылки на другие каналы и платформы\\, а также обсуждать их в комментариях и чатах шопа\\.\n\n⚡ Запрещено редактировать и удалять комментарии\\. За удаление комментариев под разборами Вы можете отправиться в бан\\, а Ваш оставшийся стафф будет отправлен Вам в индивидуальном порядке\\, после оплаты доставок\\. За редактирование комментариев Вы получаете предупреждение\\, после трёх предупреждений \\- бан с теми же последствиями\\.\n\n🔍 После записи отменить бронь на позицию можно только с заменой\\. Замену Вам необходимо найти самостоятельно\\. Вы можете написать о поиске в [специальной теме](https://t.me/c/2156756365/42) или других пабликах и чатах\\.\n\n❌ Запрещено продавать свои позиции\\, выкупленные в шопе по завышенной цене\\. Однако за заключение сделок с другими подписчиками нашего канала шоп ответственности не несёт\\.\n\n🐺 По любой интересующей информации Вы можете обратиться к [Каскыру](https://t.me/kaskirrr)🐺 \\(время ответа 1\\-3 дня\\)\\. Он старается ответить максимально быстро\\, но в случае возникновения каких\\-либо трудностей\\, время ответа может быть увеличено\\.'
defecti = '🔁Дефекты и возврат🔁\n\n👆 Иногда продаваемые карты имеют дефекты\\. По запросу админы могут уточнить их наличие, но не все продавцы отправляют видео\\. Если это Вас не устраивает – можно отказаться от выбранной позиции\\. Но если Вы вписались в позицию без уточнения или согласились на покупку без видео, то ответственность за дефекты мы не несём\\.\n\n❗ Мы также не несём ответственности за возникновение дефектов в последствии плохой упаковки от продавцов или повреждения посылок службами доставки\\.\n\n❗ Администрацией принимаются заявки по дефектам, только если товар был повреждён вследствие плохой упаковки при пересылке от нашего администратора до Вас\\. Если это произошло вследствие плохих условий транспортировки службами доставки, мы ничем помочь не сможем\\.\n\n🛍 Повреждение заводской пленки и/или коробки самого альбома дефектом не считается\\. Согласно данным корейских сайтов, сама коробка является упаковкой, цель которой \\- защитить содержимое\\.\n\n📦 В случае повреждения из\\-за некачественной упаковки, Вы можете написать [Каскыру🐺](https://t.me/kaskirrr) для оформления возврата\\. Заявки принимаются только при наличии видео\\-распаковки\\.\n\n🛍 В случае, если Вам не доложили или положили не тот товар, Вы также можете обратиться к [Каскыру🐺](https://t.me/kaskirrr) для уточнения информации\\. Заявки принимаются только при наличии видео\\-распаковки\\.\n\nПримечание\\: видео\\-распаковка принимается только в том случае, если на видео присутствует процесс вскрытия нашей/почтовой упаковки\\. Снимайте видео с самого начала, где будет хорошо видно, что Вы не повредили упаковку/стафф заранее\\. В ином случае претензия принята не будет\\.\n\n💸 В случае, если продавец не отправил товар, мы делаем возврат 100% оплаты\\.\n\nИсключение\\: если это был выкуп, предложенный Вами\\. В таком случае мы сможем вернуть только 10% суммы выкупа\\. Сумма учётов к возврату просчитывается администрацией к каждому подобному случаю в индивидуальном порядке\\. Данное правило относится ко всем Покупателям, вписавшимся в подобный разбор \\(он обязательно будет помечен, как «предложенный»\\)\\.\n\n🗓 Возврат в случае повреждения товара или его утере по вине администрации производится в течение 14\\-ти рабочих дней со дня принятия заявки\\. В случае скама – со дня предоставления Ваших данных для осуществления возврата\\.\n\n🚚 Администрация также не несёт ответственности за товар, утерянный почтой/транспортной компанией, если он был уже отправлен к вам\\. Внимательно вписывайте свои почтовые данные при оформлении заявки, в случае ошибок или смены адреса, просим уведомлять об этом Каскыра как можно скорее\\!'
regulirovanie = '💳Регулирование покупки стаффа💳\n\n🔔 Необходимо уведомлять администрацию о смене юзернейма в [специальной теме](https://t.me/c/2156756365/31)\\. Это необходимо для того\\, чтобы мы понимали\\, какой стафф – Ваш и правильно указывали Вас в таблицах с оплатами\\.\n\n🗓 Выкуп разбора производится в течении 1\\-4 дней для корейских и 1\\-14 дней для китайских разборов\\. Если в течение этого времени статус разбора не изменяется на «Выкуплен»\\, то статус автоматически становится «Отменен»\\. В течение этого времени пока статус в посте не изменился разбор считается актуальным\\, и на него может выйти оплата\\.\n\n🐾 Админы имеют право записываться в разборы на общих правилах\\, в подборах админы имеют право занимать позиции также на общих правилах\\.\n\n🖤 В некоторых подборах позиции будут заняты админами заранее \\(не в первых потоках и не более 2\\-х позиций\\)\\, информация об этом будет публиковаться непосредственно в анонсе подбора\\. Данное правило не относится к подборам предзаказанных карт к альбомам\\, купленным вне сетов – в них админы участвуют на общих условиях\\.\n\n💸 Если у Вас нет возможности оплатить позицию в срок, указанный в посте\\, то Вы можете написать [Каскыру](https://t.me/kaskirrr)🐺\\. В случае наличия уважительной причины\\, он может предоставить Вам отсрочку платежа\\. Но также оставляет за собой возможность отказать Вам в данном вопросе\\. Подобные ситуации решаются на усмотрение администрации\\.\n\n📆 За просрочку дедлайна штраф 200тг\\/в день или 40 руб\\.\\/день\\.  \n\n🪙 Штраф может копиться только в течение 5\\-ти дней за оплату разборов и в течение 10\\-ти дней за оплату коробки\\. При неоплате в течение этого срока Вы получите бан\\, а весь Ваш оставшийся стафф переходит в собственность шопа в качестве компенсации\\.\n\n📍 По приезде товара в Казахстан вам необходимо оформить его доставку каким\\-либо способом в течение 2\\-х месяцев\\. Отложка возможна не более чем на 10 карт и 2 альбома \\(либо 2 единицы иного габаритного или неформатного стаффа\\)\\.\n\n📦 В случае\\, если вы не забираете свой товар в течение этого времени мы будем вынуждены выставить ваш стафф на продажу вследствие невозможности хранить его далее\\.\n\nАУФ\\, ЩЕНКИ\\, ДОБРО ПОЖАЛОВАТЬ\\!🆙🆒'
oslezhivanie_zakazov_string = '🚚Для отслеживания статуса своего заказа вы можете воспользоваться поиском по вашему нику в Telegram, осуществить поиск по номеру вашей позиции, который указан в посте оплаты в шопе. \n\n📌 Пожалуйста, при поиске вводите свой юзернейм, с учётом регистра. Если вы - @kaskirrr, то @Kaskirrr бот найти не сможет.\n\n📆Также вы можете найти всю интересующую вас информацию в Google таблице.'
poleznie_ssilki = 'АУФ\\! Обязательно заходи в [инфо](https://t.me/STAYa_store_info), особенно рекомендую посмотреть эти темы\\:\n\n🖤 [ПРАВИЛА ШОПА](https://t.me/STAYa_store_info/36)\n🖤 [КАК ЗАКАЗАТЬ?](https://t.me/STAYa_store_info/35)\n🖤 [АКТУАЛЬНЫЕ ЗАПИСИ](https://t.me/STAYa_store_info/32)\n🖤 [ПРОГРАММА ЛОЯЛЬНОСТИ](https://t.me/STAYa_store_info/51)\n🖤 [ФЛУД](https://t.me/STAYa_store_info/33)\n\nПомни, если есть вопросы, ты всегда можешь обратиться к [Каскыру](https://t.me/kaskirrr)🐺, он обязательно поможет\\!'
kak_zakazat = 'Если ты заказываешь впервые, то обязательно загляни в общий [чат](https://t.me/STAYa_store_info)\\!\n\nТут есть [гайд](https://t.me/STAYa_store_info/35) для новичков, в котором подробно расписан каждый шаг\\!🩶\n\nЕсли даже так у тебя остались вопросы, напиши [Каскыру](https://t.me/kaskirrr)🐺, он ответит в кратчайшие сроки и обязательно поможет со всем разобраться\\!'
dostavka = 'В нашем [Супер\\-Чате](https://t.me/STAYa_store_info) есть две Мега\\-полезные ссылки по доставке\\!\n\n🩶 Список всех таблиц по доставке со сроками оплат в теме [Таблицы](https://t.me/STAYa_store_info/28)\n🩶 Список всех, чей ник есть в оплате текущей коробки в теме [Доставка](https://t.me/STAYa_store_info/27)\n\n🌏 Если ты хочешь отследить заказ и узнать, на каком этапе его статус, то нажми на кнопку "Отслеживание заказов" в главном меню этого бота [Каскыр](https://t.me/kaskirrr)🐺 как всегда с радостью поможет, если у тебя будут ещё вопросы\\!'
svyaz_admin = 'Мы всегда рады пообщаться\\! Так что приходи в [чатик Стаи](https://t.me/STAYa_store_info)🌖\n\nМы также открыты к любой критике, обратной связи и новым предложениям\\!🌝\nПравда, просим быть в этом вопросе вежливыми\\. Мы искренне стараемся работать во благо наших Покупателей, поэтому надеемся, что вы также будете любить нас🖤 \n\nПо любым вопросам всегда пишите [Каскыру](https://t.me/kaskirrr)🐺, он бодрствует с 9:00 до 23:00 по Астане \\[7:00 \\- 21:00 МСК\\]\\. Поэтому, если вы пишете в нерабочее время, ответ может занять больше времени\\. В рабочее время [Каскыр](https://t.me/kaskirrr)🐺всегда даст ответ в течение дня, либо уведомит о том, что ему необходимо дополнительное время для полноценного ответа на вопрос\\.\n\nОн не кусается, так что обязательно пишите ему, он рад поболтать со всеми\\!✨'
lock = Lock()


class DB:
    answer_data = {}
def on_click(message):
    if message.text == 'Правила шопа':
        bot.send_message(message.chat.id, pravila_string, parse_mode='MarkdownV2')
        bot.send_message(message.chat.id, defecti, parse_mode='MarkdownV2')
        bot.send_message(message.chat.id, flood, parse_mode='MarkdownV2')
        bot.send_message(message.chat.id, regulirovanie, parse_mode='MarkdownV2')
        time.sleep(1)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Как заказать?':
        bot.send_message(message.chat.id, kak_zakazat, parse_mode='MarkdownV2')
        time.sleep(1)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Отслеживание заказов':
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=types.ReplyKeyboardRemove())
        markup1 = types.InlineKeyboardMarkup()
        markup1.add(types.InlineKeyboardButton('Отследить заказы по номеру разбора', callback_data='Отследить заказ по номеру разбора'))
        markup1.add(types.InlineKeyboardButton('Отследить заказы по юзернейму', callback_data='Отследить заказ по юзернейму'))
        markup1.add(types.InlineKeyboardButton('Открыть Google таблицу', url='https://docs.google.com/spreadsheets/d/1mI4qTS0sg4s2acFgDpXNX6Nhwy67XUj4eJ2LCJD0Zrg/edit?gid=251494946#gid=251494946'))
        markup1.add(types.InlineKeyboardButton('< Назад', callback_data='Назад'))
        bot.send_message(message.chat.id, oslezhivanie_zakazov_string, reply_markup=markup1)
    elif message.text == 'Доставка':
        bot.send_message(message.chat.id, dostavka, parse_mode='MarkdownV2')
        time.sleep(1)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Полезные ссылки':
        bot.send_message(message.chat.id, poleznie_ssilki, parse_mode='MarkdownV2')
        time.sleep(1)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Связь с админами':
        bot.send_message(message.chat.id, svyaz_admin, parse_mode='MarkdownV2')
        time.sleep(1)
        bot.register_next_step_handler(message, on_click)
    elif message.text == 'Начать сначала':
        bot.send_message(message.chat.id, 'Введите /start', reply_markup=types.ReplyKeyboardRemove())
    elif message.text == '/start':
        bot.send_message(message.chat.id, 'Выберите команду', reply_markup=markup)
        time.sleep(1)
        bot.register_next_step_handler(message, on_click)
    else:
        bot.send_message(message.chat.id, 'Такой команды нет, введите /start', reply_markup=types.ReplyKeyboardRemove())

@bot.callback_query_handler(func = lambda callback:True)
def callback_message(callback):
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bttn1 = types.KeyboardButton('< Назад')
    markup2.row(bttn1)
    if callback.data == 'Отследить заказ по номеру разбора':
        try:
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
            bot.send_message(callback.message.chat.id, text='Введите номер разбора', reply_markup=markup2)
            bot.register_next_step_handler(callback.message, get_reg_data)
        except telebot.apihelper.ApiTelegramException as e:
            bot.send_message(callback.message.chat.id, text="Произошла ошибка. Введите /start", reply_markup=types.ReplyKeyboardRemove())
            print(f"Ошибка удаления сообщения: {e}")
    if callback.data == 'Отследить заказ по юзернейму':
        try:
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
            bot.send_message(callback.message.chat.id, text='Введите свой юзернейм', reply_markup=markup2)
            bot.register_next_step_handler(callback.message, get_user_data)
        except telebot.apihelper.ApiTelegramException as e:
            bot.send_message(callback.message.chat.id, text="Произошла ошибка. Введите /start", reply_markup=types.ReplyKeyboardRemove())
            print(f"Ошибка удаления сообщения: {e}")
    if callback.data == 'Назад':
        try:
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
            bot.send_message(callback.message.chat.id, text='Введите /start', reply_markup=types.ReplyKeyboardRemove())
        except telebot.apihelper.ApiTelegramException as e:
            bot.send_message(callback.message.chat.id, text="Произошла ошибка. Введите /start", reply_markup=types.ReplyKeyboardRemove())
            print(f"Ошибка удаления сообщения: {e}")
class DB:
    answer_data = {}

def get_reg_data(message: types.Message):
    retry_attempts = 1
    korea_data = update_cache("КОРЕЯ")
    china_data = update_cache("КИТАЙ")
    korea_column13 = [row.get("редис", None) for row in korea_data]
    china_column13 = [row.get("редис", None) for row in china_data]
    for attempt in range(retry_attempts):
        try:
            if message.text == '< Назад':
                bot.send_message(message.chat.id, text='Введите /start', reply_markup=types.ReplyKeyboardRemove())
            else:
                if message.text not in korea_column13 and message.text not in china_column13:
                    bot.send_message(message.chat.id, text='Такого заказа нет, введите /start', reply_markup=types.ReplyKeyboardRemove())
                    time.sleep(1)
                else:
                    DB.answer_data['ordernumber'] = message.text
                    bot.send_message(message.from_user.id, text="Введите ваш юзернейм")
                    time.sleep(1)
                    bot.register_next_step_handler(message, get_reg_data_xx)
            break
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:  # Quota exceeded
                wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
                print(f"Quota exceeded, waiting for {wait_time:.2f} seconds before retrying...")
                bot.send_message(message.from_user.id, text="Произошла ошибка. Введите /start", reply_markup=types.ReplyKeyboardRemove())
                time.sleep(wait_time)
def get_reg_data_xx(message: types.Message):
    korea_data = update_cache("КОРЕЯ")
    china_data = update_cache("КИТАЙ")
    korea_column13 = [row.get("редис", None) for row in korea_data]
    china_column13 = [row.get("редис", None) for row in china_data]
    retry_attempts = 1
    for attempt in range(retry_attempts):
        try:
            if message.text == '< Назад':
                bot.send_message(message.chat.id, text='Введите /start', reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id, text='После ввода необходимо подождать минуту, пока Каскыр соберёт информацию из таблицы...', reply_markup=types.ReplyKeyboardRemove())
                username_quantity = message.text
                x = 0
                answer = ''
                answer += f'{DB.answer_data["ordernumber"]}'
                user_give_data = ''
                for i in korea_column13:
                    if answer == i:
                        if username_quantity == korea_data[x]["неймики"]:
                            user_give_data += f'{korea_data[x]["редис"]}\n{korea_data[x]["Позиции"]}\nСтатус: {korea_data[x]["Статус разбора"]}\n\n'
                        x += 1
                        time.sleep(0.05)
                    else:
                        x += 1
                        time.sleep(0.05)
                if user_give_data != '':
                    bot.send_message(message.from_user.id, text=f'Номер заказа: {answer}\nВаш Юзернейм: {username_quantity}\n\n{user_give_data}\nДата обновления таблицы:\n{korea_data[0]["Дата обновления таблицы:"]}', reply_markup=markup)
                    bot.register_next_step_handler(message, on_click)
                else:
                    y = 0
                    user_give_data = ''
                    for i in china_column13:
                        if answer == i:
                            if username_quantity == china_data[y]["неймики"]:
                                user_give_data += f'{china_data[y]["редис"]}\n{china_data[y]["Позиции"]}\nСтатус: {china_data[y]["Статус разбора"]}\n\n'
                            y += 1
                            time.sleep(0.05)
                        else:
                            y += 1
                            time.sleep(0.05)
                    if user_give_data != '':
                        bot.send_message(message.from_user.id, text=f'Номер заказа:{answer}\nВаш Юзернейм:{username_quantity}\n\n{user_give_data}\nДата обновления таблицы:\n{china_data[0]["Дата обновления таблицы:"]}', reply_markup=markup)
                        time.sleep(1)
                        bot.register_next_step_handler(message, on_click)
                    else:
                        bot.send_message(message.from_user.id, text="Такого заказа нет", reply_markup=markup)
                        time.sleep(1)
                        bot.register_next_step_handler(message, on_click)
            break
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:  # Quota exceeded
                wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
                print(f"Quota exceeded, waiting for {wait_time:.2f} seconds before retrying...")
                bot.send_message(message.from_user.id, text="Произошла ошибка. Введите /start", reply_markup=types.ReplyKeyboardRemove())
                time.sleep(wait_time)
def get_user_data(message: types.Message):
    korea_data = update_cache("КОРЕЯ")
    china_data = update_cache("КИТАЙ")
    korea_column12 = [row.get("неймики", None) for row in korea_data]
    china_column12 = [row.get("неймики", None) for row in china_data]
    retry_attempts = 1
    for attempt in range(retry_attempts):
        try:
            if message.text == '< Назад':
                bot.send_message(message.chat.id, text='Введите /start', reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id, text='После ввода необходимо подождать минуту, пока Каскыр соберёт информацию из таблицы...', reply_markup=types.ReplyKeyboardRemove())
                user_quantity = message.text
                x = 0
                test_perem = ''
                check = 0
                for i in korea_column12:
                    if user_quantity == i:
                        test_perem += f'{korea_data[x]["редис"]}\n{korea_data[x]["Позиции"]}\nСтатус: {korea_data[x]["Статус разбора"]}\n\n'
                        x += 1
                        check = 1
                        time.sleep(1)
                    else:
                        x += 1
                y = 0
                for i in china_column12:
                    if user_quantity == i:
                        test_perem += f'{china_data[y]["редис"]}\n{china_data[y]["Позиции"]}\nСтатус: {china_data[y]["Статус разбора"]}\n\n'
                        y += 1
                        check = 1
                        time.sleep(1)
                    else:
                        y += 1
                if check == 1:
                    bot.send_message(message.from_user.id, text=f'Ваш юзернейм: {user_quantity}\n\n{test_perem}\nДата обновления таблицы:\n{korea_data[0]["Дата обновления таблицы:"]}', reply_markup=markup)
                    time.sleep(1)
                    bot.register_next_step_handler(message, on_click)
                else:
                    bot.send_message(message.from_user.id, text="Такого заказа нет", reply_markup=markup)
                    time.sleep(1)
                    bot.register_next_step_handler(message, on_click)
            break
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 429:  # Quota exceeded
                wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
                print(f"Quota exceeded, waiting for {wait_time:.2f} seconds before retrying...")
                bot.send_message(message.from_user.id, text="Произошла ошибка. Введите /start", reply_markup=types.ReplyKeyboardRemove())
                time.sleep(wait_time)
def start_polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except (ProxyError, ApiTelegramException, RemoteDisconnected, requests.exceptions.RequestException) as e:
            print(f"Polling error: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying

if __name__ == "__main__":
    print('Бот запущен...')
    print(user_id)
    start_cache_updater()
    send_initial_message()  # Отправка сообщения при запуске
    start_polling()

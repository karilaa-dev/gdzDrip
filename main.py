from json import loads as jloads
from keyboards import *
from tinydb import TinyDB, Query
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, InlineQueryResultPhoto
from configparser import ConfigParser as configparser
from time import sleep

#Загрузка конфига
config = configparser()
config.read("config.ini")

#Загрузка базы с людьми
db = TinyDB('db.json')
find = Query()

#Айди админа бота
admin_id = int(config["bot"]["admin_id"])

#Сайт с страницами из книг
url = config["bot"]["url"]

#Инициализация либы aiogram
bot = Bot(token=config["bot"]["token"])
dp = Dispatcher(bot)

#Загрузка базы с ссылками на книги
with open('books.json', 'r', encoding='utf-8') as f:
    books = jloads(f.read())

async def albebra(num):
    albebra = InlineQueryResultPhoto(
            id='albebra'+num,
            title='Алгебра',
            description=f'{num} cтраница.\nМерзляк 2019(Погл.)',
            photo_url=url+f'albebra/{num}.jpg',
            thumb_url=url+f'albebra/{num}.jpg'
    )
    return albebra

async def geom(num):
    geom = InlineQueryResultPhoto(
            id='geom'+num,
            title='Геометрия',
            description=f'{num} cтраница.\nМерзляк 2019(Погл.)',
            photo_url=url+f'geom/{num}.jpg',
            thumb_url=url+f'geom/{num}.jpg'
    )
    return geom

async def umova(num):
    umova = InlineQueryResultPhoto(
            id='umova'+num,
            title='Укр.мова',
            description=f'{num} cтраница.\nАвраменко 2019',
            photo_url=url+f'umova/{num}.jpg',
            thumb_url=url+f'umova/{num}.jpg'
    )
    return umova

async def fizika(num):
    fizika = InlineQueryResultPhoto(
            id='fizika'+num,
            title='Физика',
            description=f'{num} cтраница.\nБар’яхтар 2019',
            photo_url=url+f'fizika/{num}.jpg',
            thumb_url=url+f'fizika/{num}.jpg'
    )
    return fizika

#Функция уведомления об новом пользователе
async def adm_notify(message):

    result = f'''<b>Новый пользователь!</b>
<b>Айди:</b> <code>{message.chat.id}</code>
<b>Имя:</b> {message.chat.first_name} {message.chat.last_name}
<b>Имя пользователя:</b> @{message.chat.username}'''

    await bot.send_message(admin_id, result, parse_mode = "HTML")

#Функция для запроса книги
async def send_book(message, book, author=None):
    #wait = await message.answer('<code>Отправка книги</code>', parse_mode="HTML")
    if author is None:
        caption = f'<b>{books["single"][book][0]}</b>\nИсточник: {books["single"][book][1]}'
        document = books["single"][book][2]
    else:
        caption = f'<b>{books["multi"][book][author][0]}</b>\nИсточник: {books["multi"][book][author][1]}'
        document = books["multi"][book][author][2]
    await message.answer_document(document=document, caption=caption, parse_mode="HTML")
    #await wait.delete()

#Функция для запроса гдз
async def send_gdz(message, gdz, author=None):
    if author is None:
        name = books["single"][gdz][3]
        link = books["single"][gdz][4]
    else:
        name = books["multi"][gdz][author][3]
        link = books["multi"][gdz][author][4]
    await message.answer(f'{name}: {link}')

#Уведомляем о запуске бота
print('Бот запущен')

#Команда /start
@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    check = db.search((find.id == int(message.chat.id)))
    if check == []:
        db.insert({'id': message.chat.id, 'mode': None, 'page': None})
        await adm_notify(message)
    else:
        db.update({'mode': None, 'page': None}, find.id == message.chat.id)
    await message.answer('Вы запуситили <b>ГДЗ Drip!</b>\nВыберите интересующий вас пункт', reply_markup=keyboard, parse_mode="HTML")

#Основные команды
@dp.message_handler()
async def send_text(message: types.Message):

    #Более короткая название переменой для текста сообщения
    text = message.text

    #Загрузка информации об пользователе
    check = db.search((find.id == int(message.chat.id)))[0]

    #Команда для перехода в секцию с книгами
    if text in ['Книги', '/book']:
        db.update({'mode': 'book', 'page': 1}, find.id == message.chat.id)
        await message.answer('Вы перешли в книги', reply_markup=keyboardbook)

    #Команда для перехода в секцию с гдз
    elif text in ['ГДЗ', '/gdz']:
        db.update({'mode': 'gdz'}, find.id == message.chat.id)
        await message.answer('Вы перешли в ГДЗ', reply_markup=keyboardgdz)

    #Команда для рассылки уведомления из файла n.txt
    elif text == '/notify' and message.chat.id == admin_id:
        check = db.all()
        print("-----")
        with open('n.txt', 'r', encoding="utf-8") as f:
            notify = f.read()
        for num, id in enumerate(check):
            print(id["id"])
            await bot.send_message(id["id"], notify, parse_mode="HTML")
            sleep(0.1)

    #Команда для просмотра количества участников
    elif text in ['/list', '/len'] and message.chat.id == admin_id:
        req = db.all()
        result = f'Всего пользователей: <b>{len(req)}</b>'
        await message.answer(result, parse_mode="HTML")

    #Команда Назад
    elif text in ['Назад' , '/back']:
        if check["mode"] in ["bio", "zah"]:
            if check["page"] == 2:
                keyb = keyboardbook2
            else:
                keyb = keyboardbook
            msg = 'Вы вернулись в меню с книгами'
            db.update({'mode': 'book'}, find.id == message.chat.id)
        elif check["mode"] == "fiz":
            keyb = keyboardgdz
            msg = 'Вы вернулись в меню с ГДЗ'
            db.update({'mode': 'gdz'}, find.id == message.chat.id)
        else:
            keyb = keyboard
            msg = 'Вы вернулись в главное меню'
            db.update({'mode': None, 'page': None}, find.id == message.chat.id)
        await message.answer(msg, reply_markup=keyb)

    #Команды при режиме с книгами
    elif check["mode"] == 'book':

        #Переход между страницыми
        if text == 'Следующая страница':
            db.update({'page': 2}, find.id == message.chat.id)
            await message.answer('Переход на 2 страницу', reply_markup=keyboardbook2)
        elif text == 'Предыдущая страница':
            db.update({'page': 1}, find.id == message.chat.id)
            await message.answer('Переход на 1 страницу', reply_markup=keyboardbook)

        #Блок с книгами
        elif text == 'Алгебра':
            await send_book(message, 'algebra')
        elif text == 'Геометрия':
            await send_book(message, 'geometria')
        elif text == 'Укр.мова':
            await send_book(message, 'ukrmova')
        elif text == 'Укр.лит':
            await send_book(message, 'ukrlit')
        elif text == 'Физика':
            await send_book(message, 'fizika')
        elif text == 'Биология':
            db.update({'mode': 'bio'}, find.id == message.chat.id)
            await message.answer('Вы перешли в Биология', reply_markup=keyboardbio)
        elif text == 'География':
            await send_book(message, 'geografia')
        elif text == 'Химия':
            await send_book(message, 'himia')
        elif text == 'История Украины':
            await send_book(message, 'ukristor')
        elif text == 'Мировая История':
            await send_book(message, 'worldistor')
        elif text == 'Зар.лит':
            await send_book(message, 'zarlit')
        elif text == 'Захист В.':
            db.update({'mode': 'zah'}, find.id == message.chat.id)
            await message.answer('Вы перешли в Захист В.', reply_markup=keyboardzah)
        elif text == 'Астрономия':
            await send_book(message, 'astronomia')
        elif text == 'ZNO Leader CD':
            await message.answer('Архив с данными с диска: https://drive.google.com/file/d/1NENMdxuqzUgsdAWHP0f7lWS18lilt5Wb/view?usp=sharing')

    #Команды при режиме ГДЗ
    elif check["mode"] == 'gdz':
        if text == 'Физика':
            db.update({'mode': 'fiz'}, find.id == message.chat.id)
            await message.answer('Вы перешли в Физику', reply_markup=keyboardfiz)
        elif text == 'Укр.мова':
            await send_gdz(message, 'ukrmova')
        elif text == 'Химия':
            await send_gdz(message, 'himia')

    #Комнды для режима ГДЗ с физики
    elif check["mode"] == 'fiz':
        if text == 'Книга':
            await message.answer('Книга с физики ГДЗ:\nhttps://4book.org/gdz-reshebniki-ukraina/11-klass/gdz-fizika-11-klas-baryahtar-2019')
        elif text == 'Тетрадь':
            await message.answer('Тетрадь с физики ГДЗ: https://4book.org/gdz-reshebniki-ukraina/11-klass/gdz-zoshit-fizika-11-klas-bozhinova-2019')

    #Команды для режима с книгами биологии
    elif check["mode"] == 'bio':
        if text == 'Соболь':
            await send_book(message, 'biologia', 'sobol')
        elif text == 'Андерсон':
            await send_book(message, 'biologia', 'anderson')

    #Команды для режима с книгами захиты отечества
    elif check["mode"] == 'zah':
        if text == 'Хлопці':
            await send_book(message, 'zahist', 'boy')
        elif text == 'Дівчата':
            await send_book(message, 'zahist', 'girl')

@dp.inline_handler()
async def inline_books(query: InlineQuery):
    text = query.query.split()
    result = []
    if query["from"]["id"] == admin_id:
        if query.query.isdigit():
            if 5 <= int(text[0]) <= 303:
                result.append(await albebra(text[0]))
            if 1 <= int(text[0]) <= 239:
                result.append(await geom(text[0]))
            if 1 <= int(text[0]) <= 208:
                result.append(await umova(text[0]))
            if 1 <= int(text[0]) <= 272:
                result.append(await fizika(text[0]))

        elif len(text) == 2:
            if text[0].isdigit:
                if text[1].lower().startswith('а'):
                    if 5 <= int(text[0]) <= 303:
                        result.append(await albebra((text[0])))
                elif text[1].lower().startswith('г'):
                    if 1 <= int(text[0]) <= 239:
                        result.append(await geom((text[0])))
                elif text[1].lower().startswith('у'):
                    if 1 <= int(text[0]) <= 208:
                        result.append(await umova((text[0])))
                elif text[1].lower().startswith('ф'):
                    if 1 <= int(text[0]) <= 272:
                        result.append(await fizika((text[0])))
        else:
            bebra = InlineQueryResultArticle(
                id='else',
                description='Например: (книга не обязятельная)\n@gdz_drip_bot {номер} {книга}',
                title='Введите нужную страницу',
                input_message_content=InputTextMessageContent('А нажал то зачем?')
            )
            result.append(bebra)
    else:
        bebros = InlineQueryResultArticle(
                id='notkarilaa',
                description='Сначало меня в гдз, а ботом бота',
                title='А вы что хотели?',
                input_message_content=InputTextMessageContent('А нажал то зачем?')
            )
        result.append(bebros)
    await query.answer(results=result, cache_time=300, switch_pm_text='Перейти в gdzDrip', switch_pm_parameter='from_inline_query')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
from aiogram.types import ReplyKeyboardMarkup

#Главное меню
keyboard = ReplyKeyboardMarkup(True)
keyboard.row('Книги')
keyboard.row('ГДЗ')

#Страница 1 меню с книгами
keyboardbook = ReplyKeyboardMarkup(True)
keyboardbook.row("Алгебра", "Геометрия")
keyboardbook.row("Укр.мова", "Укр.лит")
keyboardbook.row("Физика", "Биология")
keyboardbook.row("География", "Химия")
keyboardbook.row('Следующая страница')
keyboardbook.row('Назад')

#Страница 2 меню с книгами
keyboardbook2 = ReplyKeyboardMarkup(True)
keyboardbook2.row("История Украины", "Мировая История")
keyboardbook2.row("Зар.лит", "Захист В.")
keyboardbook2.row("Астрономия", "ZNO Leader CD")
keyboardbook2.row('Предыдущая страница')
keyboardbook2.row('Назад')

#Меню с ГДЗ
keyboardgdz = ReplyKeyboardMarkup(True)
keyboardgdz.row("Физика")
keyboardgdz.row("Укр.мова")
keyboardgdz.row("Химия")
keyboardgdz.row('Назад')

#Меню книг с алгебры
keyboardalgb = ReplyKeyboardMarkup(True)
keyboardalgb.row('Мерзляк', 'Нелин')
keyboardalgb.row('Назад')

#Меню книг с биологии
keyboardbio = ReplyKeyboardMarkup(True)
keyboardbio.row('Соболь', 'Андерсон')
keyboardbio.row('Назад')

#Меню книг с защиты отечества
keyboardzah = ReplyKeyboardMarkup(True)
keyboardzah.row('Хлопці', 'Дівчата')
keyboardzah.row('Назад')

#Меню гдз с физики
keyboardfiz = ReplyKeyboardMarkup(True)
keyboardfiz.row('Книга', 'Тетрадь')
keyboardfiz.row('Назад')
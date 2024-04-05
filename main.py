import sqlite3
from telebot import *

bot = telebot.TeleBot(str(input('Введите токен бота...  ')))
print('Токен получен, спасибо!')
connection = sqlite3.connect('students.db', check_same_thread=False)
cursor = connection.cursor()

# create new table (id_students) if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS id_students (
school TEXT NOT NULL,
name_us_1 TEXT NOT NULL,
telegram_id INTEGER NOT NULL,
school_class INTEGER NOT NULL,
k INTEGER NOT NULL
)
''')
connection.commit()

# create new table (ask_students) if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS ask_students (
number_work INTEGER PRIMARY KEY,
stude_class INTEGER NOT NULL,
name_lesson TEXT NOT NULL,
home_work TEXT NOT NULL,
right_answer TEXT NOT NULL,
teacher_id INTEGER NOT NULL
)
''')
Var = {
        'usname': '',
        'school_rank': '',
        'telegram_id': 0,
        'school': '',
        'school_class': 0,
        'USERID': 0,
        'all_student_2': 0,
        'stude_class': 0,
        'name_lesson': '',
        'home_work': '',
        'right_answer': '',
        'num_homework': 0
    }
globalVar = {
    'chatid': Var
}


@bot.message_handler(commands=['start'])
def start_bot(message):
    globalVar[str(message.chat.id)] = globalVar.pop('chatid')
    stop_message = bot.send_message(message.chat.id,
                                    'Привет! Добро пожаловать в телеграм бот для '
                                    'решения '
                                    'домашних заданий, пожалуйста, напиши свою фамилию '
                                    'и имя!')
    bot.register_next_step_handler(stop_message, save_name_user)


def save_name_user(message):
    globalVar[str(message.chat.id)]['usname'] = message.text
    stop_message = bot.send_message(message.chat.id, f'Приятно познакомиться,'
                                                     f' {message.text}! Ты учитель или '
                                                     f'ученик?')
    bot.register_next_step_handler(stop_message, save_school_rank)


def save_school_rank(message):
    globalVar[str(message.chat.id)]['school_rank'] = message.text
    globalVar[str(message.chat.id)]['telegram_id'] = message.from_user.id

    school_rank = message.text

    if 'учитель' in str(school_rank).lower():
        stop_message = bot.send_message(message.chat.id, 'Очень приятно! Введите, '
                                                         'пожалуйста, школу в которой '
                                                         'преподаете! \n(Без знаков '
                                                         'препинания, как в списке '
                                                         'ниже.) \nСписок '
                                                         'доступных школ: '
                                                         '\nМБОУ СШ пос Борское'
                                                         '\nМБОУ СШ 2 им. '
                                                         'А.Круталевича'
                                                         '\nМБОУ СШ 1 имени Игоря '
                                                         'Прокопенко')
        bot.register_next_step_handler(stop_message, save_school_teacher)

    elif 'ученик' in str(school_rank).lower():
        stop_message = bot.send_message(message.chat.id, 'Круто) А теперь введи '
                                                         'школу, в которой учишься!'
                                                         '\n(Без знаков '
                                                         'препинания, как в списке '
                                                         'ниже.) \nСписок '
                                                         'доступных школ: '
                                                         '\nМБОУ СШ пос Борское'
                                                         '\nМБОУ СШ 2 им. '
                                                         'А.Круталевича'
                                                         '\nМБОУ СШ 1 имени Игоря '
                                                         'Прокопенко')
        bot.register_next_step_handler(stop_message, save_school_student)

    else:
        stop_message = bot.send_message(message.chat.id, 'Попробуй написать еще раз!')
        bot.register_next_step_handler(stop_message, save_school_rank)


def save_school_teacher(message):
    globalVar[str(message.chat.id)]['school'] = str(message.text).lower()
    globalVar[str(message.chat.id)]['USERID'] = int(message.from_user.id)

    bot.send_message(message.chat.id, 'Спасибо, что зарегистрировались, '
                                      'как учитель! Вам будут доступны все функции, '
                                      'после подтверждения вашего аккаунта '
                                      'администратором.')

    usn = message.from_user.username

    bot.send_message('1024476833', f'Пользователь '
                                   f'@{usn} ожидает '
                                   f'подтверждения своего аккаунта')


def save_school_student(message):
    globalVar[str(message.chat.id)]['school'] = str(message.text).lower()
    save_school_student_2(message)


def save_school_student_2(message):
    stop_message = bot.send_message(message.chat.id, 'Введи класс, '
                                                     'в котором учишься!')
    bot.register_next_step_handler(stop_message, save_school_class)


def save_school_class(message):
    try:
        globalVar[str(message.chat.id)]['school_class'] = int(message.text)
        bot.send_message(message.chat.id, 'Круто! Ты уже такой взрослый! '
                                          'А сейчас минутка полезной '
                                          'информации для тебя!')

        bot.send_message(message.chat.id, 'Как только учитель '
                                          'пришлет тебе домашнее задание, '
                                          'оно отобразиться в '
                                          'этом чате! У тебя '
                                          'будет время решить его '
                                          'и отправить ответ. '
                                          'После этого, '
                                          'тебе будет показан '
                                          'правильный ответ) Удачи!')

        bot.send_message(message.chat.id, 'Пока у тебя нет дз. Можешь отдыхать)')

        school = globalVar[str(message.chat.id)]['school']
        usname = globalVar[str(message.chat.id)]['usname']
        telegram_id = globalVar[str(message.chat.id)]['telegram_id']
        school_class = globalVar[str(message.chat.id)]['school_class']

        cursor.execute(f'INSERT INTO id_students (school, name_us_1, telegram_id, '
                       f'school_class, k) VALUES (?, ?, ?, ?, ?)',
                       (school, usname, telegram_id, school_class, 0))
        connection.commit()
    except:
        bot.send_message(message.chat.id, 'Номер класса должен быть числом!')
        save_school_student_2(message)
        return


@bot.message_handler(commands=['True'])
def activate(message):
    USERID = globalVar[str(message.chat.id)]['USERID']
    bot.send_message(USERID, 'Ваш аккаунт подтвердил администратор! '
                             'Для запуска рассылки домашнего задания, '
                             'нажмите на команду /askstudent')
    globalVar[str(message.chat.id)]['USERID'] = ''


@bot.message_handler(commands=['False'])
def activate(message):
    USERID = globalVar[str(message.chat.id)]['USERID']
    bot.send_message(USERID, 'Администратор ограничил вам доступ к фунциям учителя.')
    globalVar[str(message.chat.id)]['USERID'] = ''


@bot.message_handler(commands=['askstudent'])
def what_the_class(message):
    stop_message = bot.send_message(message.chat.id, 'Вы зашли в редактор отправки '
                                                     'домашнего задания ученикам! Для '
                                                     'начала введите, какому классу вы '
                                                     'хотите задать дз?')
    bot.register_next_step_handler(stop_message, what_the_lesson)


def what_the_lesson(message):
    school = globalVar[str(message.chat.id)]['school']
    try:
        stude_class = int(message.text)
        globalVar[str(message.chat.id)]['stude_class'] = stude_class
    except:
        bot.send_message(message.chat.id, 'Номер класса должен быть числом!')
        what_the_class(message)
        return

    cursor.execute('SELECT telegram_id FROM id_students WHERE school = ? AND '
                   'school_class = ?',
                   (school, int(message.text)))
    all_student = list(set(cursor.fetchall()))
    all_student_2 = [int(str(i)[1:-2]) for i in all_student]
    globalVar[str(message.chat.id)]['all_student_2'] = all_student_2
    print(f'All id students from {message.text} class:', all_student_2)

    stop_message = bot.send_message(message.chat.id, f'В {message.text} классе, '
                                                     f'{len(all_student)} '
                                                     f'зарегистрированных учащихся! '
                                                     f'Пожалуйста, введите название '
                                                     f'предмета, по которому хотите '
                                                     f'задать домашнее задание!')
    bot.register_next_step_handler(stop_message, what_the_ask)


def what_the_ask(message):
    name_lesson = message.text
    globalVar[str(message.chat.id)]['name_lesson'] = name_lesson
    stop_message = bot.send_message(message.chat.id, 'Благодарю! '
                                                     'Теперь введите текст задания!')
    bot.register_next_step_handler(stop_message, what_the_right_answer)


def what_the_right_answer(message):
    home_work = message.text
    globalVar[str(message.chat.id)]['home_work'] = home_work

    stop_message = bot.send_message(message.chat.id, 'Осталось только ввести '
                                                     'ответ на задание!')
    bot.register_next_step_handler(stop_message, start_mailing1)


def start_mailing1(message):
    right_answer = message.text
    globalVar[str(message.chat.id)]['right_answer'] = right_answer
    teacher_id = int(message.from_user.id)

    name_lesson = globalVar[str(message.chat.id)]['name_lesson']
    stude_class = globalVar[str(message.chat.id)]['stude_class']
    home_work = globalVar[str(message.chat.id)]['home_work']
    all_student_2 = globalVar[str(message.chat.id)]['all_student_2']

    cursor.execute('INSERT INTO ask_students (stude_class, name_lesson, home_work, '
                   'right_answer, teacher_id) VALUES (?, ?, ?, ?, ?)',
                   (int(stude_class),
                    name_lesson,
                    home_work,
                    right_answer,
                    teacher_id))
    connection.commit()

    # select number homework
    cursor.execute('SELECT last_insert_rowid()')
    number_work = list(set(cursor.fetchall()))
    number_work_2 = [int(str(i)[1:-2]) for i in number_work]
    number_work_2 = number_work_2[0]

    bot.send_message(message.chat.id, f'Домашнее задание отправлено '
                                      f'ученикам {stude_class} класса!')

    bot.send_message(message.chat.id, 'Как только ученик выполнит его, вам придет '
                                      'уведомление о правильности его решения. Для '
                                      'отправки еще одного домашнего задания, нажмите '
                                      'на команду /askstudent')

    for link in all_student_2:
        bot.send_message(link, f'Тебе пришло новое домашнее задание'
                               f' по предмету {name_lesson}! \n(его номер:'
                               f' {number_work_2})'
                               f'\nВот оно: \n{home_work}')
        k = 1
        cursor.execute(f'UPDATE id_students SET k ={k} WHERE telegram_id = {link}')
        connection.commit()

        bot.send_message(link, 'Выполни задание и пришли ответ, '
                               'написав сначала номер указанного выше задания!')


@bot.message_handler(content_types=['text'])
def number_works(message):
    cursor.execute('SELECT number_work FROM ask_students')
    all_number_work = list(set(cursor.fetchall()))
    all_number_work_2 = [int(str(i)[1:-2]) for i in all_number_work]

    cursor.execute(f'SELECT k FROM id_students WHERE telegram_id = '
                   f'{int(message.from_user.id)}')
    k_0 = list(set(cursor.fetchall()))
    k = [str(i)[1:-2] for i in k_0]
    k = k[0]

    if int(message.text) in all_number_work_2 and int(k) == 1:
        num_homework = message.text
        globalVar[str(message.chat.id)]['num_homework'] = num_homework
        if int(message.text) in all_number_work_2:
            stop_message = bot.send_message(message.chat.id, f'Задание номер '
                                                             f'{message.text}. Введи на '
                                                             f'него ответ!')
            bot.register_next_step_handler(stop_message, check)
    else:
        bot.send_message(message.chat.id, 'Немного не понял твое сообщение :(')


def check(message):
    num_homework = globalVar[str(message.chat.id)]['num_homework']

    cursor.execute(f'SELECT name_us_1 FROM id_students WHERE telegram_id = '
                   f'{message.from_user.id}')
    name_us_1_0 = list(set(cursor.fetchall()))
    name_us_1 = [str(i)[1:-2] for i in name_us_1_0]
    name_us_1 = name_us_1[0]
    for i in range(5):
        name_us_1 = name_us_1.replace("'", '')

    cursor.execute(f'SELECT right_answer FROM ask_students WHERE number_work = '
                   f'{num_homework}')
    right_0 = list(set(cursor.fetchall()))
    right = [str(i)[2:-3] for i in right_0]
    right = right[0]

    cursor.execute(f'SELECT teacher_id FROM ask_students WHERE number_work = '
                   f'{num_homework}')
    teacher_id_0 = list(set(cursor.fetchall()))
    teacher_id = [int(str(i)[1:-2]) for i in teacher_id_0]
    teacher_id = teacher_id[0]

    cursor.execute(f'SELECT stude_class FROM ask_students WHERE number_work = '
                   f'{num_homework}')
    stude_class_0 = list(set(cursor.fetchall()))
    stude_class = [int(str(i)[1:-2]) for i in stude_class_0]
    stude_class = stude_class[0]

    if message.text == right:
        bot.send_message(message.chat.id, 'Молодец! Ответ правильный! Отправил его '
                                          'учителю!')
        bot.send_message(int(teacher_id), f'Ученик {stude_class} класса, {name_us_1}. '
                                          f'Правильно выполнил домашнее задание! \nЕго '
                                          f'ответ: {message.text}')
    else:
        bot.send_message(message.chat.id, f'Ответ не правильный :( \n'
                                          f'Правильный ответ:\n{right}')
        bot.send_message(int(teacher_id), f'Ученик {stude_class} класса, {name_us_1}. '
                                          f'Неправильно выполнил домашнее задание! '
                                          f'\nЕго ответ: {message.text}.'
                                          f'\nПравильный ответ: {right}')


bot.polling(none_stop=True)
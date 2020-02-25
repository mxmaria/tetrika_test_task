import sqlite3

# =========== Запросы создания необходимых таблиц ==========
sql_lessons_table_creation = '''
    CREATE TABLE IF NOT EXISTS lessons(
              id TEXT PRIMARY KEY,
        event_id INTEGER NOT NULL,
         subject TEXT NOT NULL,
  scheduled_time TEXT NOT NULL
    )
'''

sql_quality_table_creation = '''
    CREATE TABLE IF NOT EXISTS quality(
          lesson_id TEXT,
        tech_quality INTEGER,
         FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    )
'''

sql_users_table_creation = '''
    CREATE TABLE IF NOT EXISTS users(
          id TEXT PRIMARY KEY,
        role TEXT NOT NULL
    )
'''

sql_participants_table_creation = '''
    CREATE TABLE IF NOT EXISTS participants(
        event_id INTEGER NOT NULL,
         user_id TEXT NOT NULL,
     FOREIGN KEY (user_id) REFERENCES users(id)
    )
'''


# ========= Необходимые функции ==============
# В файлах есть артефакты, например в файле participants
# присутствует абсолютно одинаковые строки и они дублируются...

# Функция заполнения из данных без артефактов(без дублирований строк в исходнике) и
# из данных с артефактами(с дублированием строк в исходнике)
def fill_the_table_with_values(source_file_name, number_of_columns, sql_insert_query, artefact = False):
    # Если артефактный файл
    if artefact:
        values = []

    with open(source_file_name) as source_file:
        # Пропускаю 2 незначимые строки со служебными данными (имена колонок, разделители)
        source_file.readline()
        source_file.readline()
        for row in source_file:
            # Получаю значения колонок в виде списка
            # Разделяю по разделителю '|', убираю пробелы и символы переноса строки
            columns = [column.replace(' ', '').replace('\n', '') for column in row.split('|')]

            # Беру только значимые колонки, т.е. не беру например строку вида (378 row)
            if len(columns) == number_of_columns:
                # Если данные берутся не из артефактных файлов исходников с дублированием строк...
                if not artefact:
                    # То просто исполнить запрос с добавлением значений в таблицу
                    cur.execute(
                        sql_insert_query, columns
                    )
                else:
                    # Проверяю наличие в списке values значений, которые необходимо добавить.
                    # Если их нет, то добавляю список значений в список values,
                    # из которого значения впоследствии добавлю в таблицу через executemany.
                    if columns not in values:
                        values.append(columns)

    # Добавляю в таблицу отфильтрованные значения без повторений
    if artefact:
        cur.executemany(sql_insert_query, values)


# ================ Основная логика программы ================
if __name__ == '__main__':

    # Вспомогательно для задачи организую файл tetrika.db (базу данных)
    conn = sqlite3.connect('tetrika.db')
    cur = conn.cursor()

    # Создаю все необходимые таблицы
    for sql_creation in [
        sql_lessons_table_creation,
        sql_quality_table_creation,
        sql_users_table_creation,
        sql_participants_table_creation
    ]:
        cur.execute(sql_creation)

    # Заполняю таблицу lessons (она без артефактов-дублирующих строк)
    fill_the_table_with_values(
        'source_files/lessons.txt', 4,
        'INSERT INTO lessons VALUES(?, ?, ?, datetime(?))'
    )

    # Заполняю таблицу quality (она без артефактов-дублирующих строк)
    fill_the_table_with_values(
        'source_files/quality.txt', 2,
        'INSERT INTO quality VALUES(?, ?)'
    )

    # Заполняю таблицу users (она с артефактами-дублирующими строками...)
    fill_the_table_with_values(
        'source_files/users.txt', 2,
        'INSERT INTO users VALUES(?, ?)', True
    )

    # Заполняю таблицу participants (она с артефактами-дублирующими строками...)
    fill_the_table_with_values(
        'source_files/participants.txt', 2,
        'INSERT INTO participants VALUES(?, ?)', True
    )

    # Закрепляю изменения
    conn.commit()

    # Вывод результата в соответствии с условием задачи:
    cur.execute('''
        SELECT dt, usr, mark FROM (
               SELECT u.id usr, 
                      date(datetime(l.scheduled_time, '+3 hours')) dt,
                      AVG(q.tech_quality) mark
                 FROM lessons AS l
                 JOIN quality q ON q.lesson_id = l.id
                 JOIN participants p ON l.event_id = p.event_id
                 JOIN users u ON u.id = p.user_id
                WHERE u.role = 'tutor'
                  AND l.subject = 'phys'
                  AND q.tech_quality != ''
             GROUP BY usr, dt
             ORDER BY dt, mark DESC
       ) WHERE mark IS NOT NULL GROUP BY dt
    ''')
    results = cur.fetchall()
    for row in results:
        print(row[0], row[1], round(row[2], 2))

# Результат:
# ______________________________________________________
# 2020-01-11 8fe03f08-8581-430c-a590-9888ab36deb3 4.43
# 2020-01-12 696c838e-c054-4e9f-a51a-50bf5660f364 4.89
# 2020-01-13 be676776-8366-4c71-8a35-d58014806eb5 5.0
# 2020-01-14 c6718d0e-976c-4d6c-b0e0-32c770776567 4.0
# 2020-01-15 b37ccae8-fc31-4ad8-8f55-ca855b23fbf6 5.0
# 2020-01-16 2fa2ab62-f1b0-4036-872f-bcfd9a8686ff 4.0
# 2020-01-17 696c838e-c054-4e9f-a51a-50bf5660f364 4.5
# 2020-01-18 43efce48-94b2-4412-857f-223d45969008 4.25
# 2020-01-19 be676776-8366-4c71-8a35-d58014806eb5 4.5
# 2020-01-20 43efce48-94b2-4412-857f-223d45969008 4.5
# ______________________________________________________

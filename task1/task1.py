# Условие task1:
# 1) Отсортировать все имена в лексикографическом порядке
# 2) Посчитать для каждого имени алфавитную сумму – сумму порядковых номеров букв (MAY: 13 + 1 + 25 = 39)
# 3) Умножить алфавитную сумму каждого имени на порядковый номер имени в отсортированном списке
# (индексация начинается с 1). Например, если MAY находится на 63 месте в списке, то результат для него будет 63 * 39 = 2457.
# 4) Просуммировать произведения из п. 3 для всех имен из файла и получить число. Это число и будет ответом.

# Переменная, в которой будет ответ на задачу
amount = 0
with open("names.txt") as our_data:
    # Читаю файл не учитывая первые и последние кавычки: "
    # Разбиваю по "," имена из файла, чтобы получить список имен
    prepared_list_of_names = our_data.read()[1:-1].split('","')

    # Пронумерую каждый элемент списка начиная с 1,
    # чтобы умножить в дальнейшем алфавитную сумму каждого имени на его порядковый номер в списке
    for index, name in enumerate(prepared_list_of_names, start=1):
        # Прибавляю в "переменную-результат" сумму элементов полученного списка из
        # list comprehension, которая умножается на порядковый номер (index) в списке имен.
        # В списке: номер позиции каждой буквы имени в алфавите (ord(letter.lower())-96)
        # Каждую букву имени получаю при помощи list(name).
        amount += sum([ord(letter.lower())-96 for letter in list(name)]) * index

print(amount)
# Результат: 850722484

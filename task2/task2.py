# Условие task2:
# Есть файл со строками вида:
# <host>\t<ip>\t<page>\n
# Нужно вывести 5 айпи-адресов, которые встречаются чаще других.

# Создаю словарь, который будет содержать ключ: ip
# и значение: кол-во таких ip в файле.
ips_and_their_count = dict()
with open('hits.txt') as source_file:
    for line in source_file:
        # Из каждой строки файла достаю содержимое(ip)
        # между \t и \t с левой и правой стороны соответственно.
        current_ip = line[line.find('\t')+1:line.rfind('\t')]
        # Обновляю значение(кол-во ip в файле)для ключа-ip в словаре.
        # Если такого ip еще не было,
        # то за изначальное значение беру 0 и прибавляю 1.
        ips_and_their_count[current_ip] = ips_and_their_count.get(current_ip, 0) + 1

# Создаю list при помощи list comprehension,
# значения достаю из отсортированных по кол-ву ip в файле кортежей (по убыванию),
# полученных из созданного и заполненного ранее словаря.
# Вывожу первые 5 таких ip, кол-во встреч в файле игнорирую
print([
    current_ip for current_ip, _ in sorted(
        ips_and_their_count.items(), key=lambda item: item[1], reverse=True
    )
][:5])
# Результат: ['154.157.157.156', '82.146.232.163', '194.78.107.33', '226.247.119.128', '21.143.243.182']

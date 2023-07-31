import csv
import re


# Читаем файл
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# Проходим по нативному списку вычленяя и объединяя части Ф.И.О.
for human in contacts_list[1:]:
  fullname = human[0] + human[1] + human[2]
  # Убираем все пробелы:
  prefix_name = "".join(fullname.split())
  # Делим строку по заглавным буквам:
  capitalization_rate = 0
  # Сохраняем индексы заглавных букв в список
  indexes =[]
  for letter in prefix_name:
       if letter == letter.upper():
          capitalization_rate += 1
          indexes.append(prefix_name.index(letter))
  # Сборка имен и списка имен
  if len(indexes) == 3:
     human[0] = prefix_name[:indexes[1]]
     human[1] = prefix_name[indexes[1]:indexes[2]]
     human[2] = prefix_name[indexes[2]:]
  elif len(indexes) == 2:
    human[0] = prefix_name[:indexes[1]]
    human[1] = prefix_name[indexes[1]:]

  # Приводим телефоны к необходимому формату  
  phone_pattern = r"(\+7|8)\s*\(?(\d{3})\)?\s*\-?(\d{3})\-?(\d{2})\-?(\d{2})\s*\(?(доб\.?)?\s*(\d*)\)?"
  substitution = r"+7(\2)\3-\4-\5 \6\7"
  phone = human[5]
  new_phone = re.sub(phone_pattern, substitution, phone)
  human[5] = new_phone

# Создаем новый список контактов и временный список с дубликатами
new_list =[]
temp_list = []
temp = []
for elem in contacts_list:
    tmp = elem[0] + elem[1]
    if tmp not in temp:
        temp.append(tmp)
        new_list.append(elem)
    else:
        temp_list.append(elem)
# Объединяем данные из дубликатов с новым списком
for temp_elem in temp_list:
    for elem in new_list:
        if temp_elem[0] == elem[0] and temp_elem[1] == elem[1]:
            for i in range(3, 7):
                if elem[i] == '' and len(temp_elem[i]) != 0:
                    elem[i] = temp_elem[i]

# Пишем/переписываем новый файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_list)
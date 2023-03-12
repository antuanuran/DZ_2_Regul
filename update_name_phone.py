import csv
import re


with open('phonebook_raw.csv') as temp:
    rows = csv.reader(temp)
    contacts_list = list(rows)

header = contacts_list[0]
data = contacts_list[1:]


# Создадим класс Контакта.
# Затем, будем создавать экземпляры класса
# Затем добавим метод сравнения двух экземпляров по Фамилии и Имени
# И если они совпадут, то записываем в недостающие поля из первого экземпляра - данные из второго экземпляра
# И второй экземпляр, из которого взяли дополнительные данные - не записываем в результат

class Contact:
    def __init__(self, firstname, lastname, surname, organization, position, phone, email):
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.organization = organization
        self.position = position
        self.phone = phone
        self.email = email

    def __str__(self):
        return f'{self.firstname}, {self.lastname}, {self.surname}, {self.organization}, {self.position}, {self.phone}, {self.email}'

    # Данный метод возвращает True или False, если выполняется условие сравнения двух экземпляров
    def __eq__(self, other):
        return self.firstname == other.firstname and self.lastname == other.lastname

    def __repr__(self):
        return str(self)

    # Данный метод берет первый экземпляр и второй и записывает на место аргумента первого экземпляра (если там пусто) данные второго экземпляра
    def update(self, other):
        self.firstname = self.firstname or other.firstname
        self.lastname = self.lastname or other.lastname
        self.surname = self.surname or other.surname
        self.organization = self.organization or other.organization
        self.position = self.position or other.position
        self.phone = self.phone or other.phone
        self.email = self.email or other.email




# Приводим ФИО к нужному виду: 'firstname', 'lastname', 'surname'

storage = []
for contact in data:
    first, last, sur = contact[0:3]
    temp = f'{first} {last} {sur}'
    name_fio = temp.split()

    if len(name_fio) == 3:
        firstname, lastname, surname = name_fio[0:3]
        name_result = [firstname, lastname, surname]

    elif len(name_fio) == 2:
        firstname, lastname = name_fio[0:2]
        name_result = [firstname, lastname, 'None']

    else:
        firstname = name_fio[0]
        name_result = [firstname, 'None', 'None']


    # Регулярка для телефонов. Привести к виду: +7(999)999-99-99 доб. 9999
    phone_bad = contact[5]
    pattern = r"(\+7|7|8)(\s\(|\s|\(|[ ]*)(\d{3})(\)\s|-|\)|[1]*)(\d{3})(-|\s|[1]*)(\d{2})(-|[1]*)(\d{2})($|\s\(*)([а-ё]+\.\s\d+|[1]*)(\)|[1]*)"
    phone_result = re.sub(pattern, r"+7(\3)\5-\7-\9 \11", phone_bad)

    # Объединяем контакт: lastname,firstname,surname,organization,position,phone,email
    cont = [name_result[0], name_result[1], name_result[2], contact[3], contact[4], phone_result, contact[6]]


    # Обновляем контакт - объединить все дублирующиеся записи, если совпали Фамилия и Имя/
    # Один экземпляр - это один элекмент в списке Storage. Т.е. первый подный контакт (ФИО, номер, почта и т.д.) - это Storage[0], Следующий экземпляр - это Storage[1]
    contact = Contact(cont[0], cont[1], cont[2], cont[3], cont[4], cont[5], cont[6])

    # Как происходит проверка:
    # Метод __eq__ Сравнивает 2 экземпляра между собой First и Last. И если True - то выполняется условие if (ниже)
    # Создался экземпляр contact. Если в списке Storage - уже лежит экземпляр contact, у которого Фамилия и Имя такие же, то считается индекс, где стоит этот экземпляр (первый)
    # И затем берется этот элемент списка (по факту это экземпляр) ставится точка и у этого экземпляра вызыается наш метод Update, к которому нужно указать еще текущий экземпляр (второй)

    if contact in storage:
       index = storage.index(contact)
       storage[index].update(contact)

    else:
        storage.append(contact)

# Сохраняем в файл итог
with open('result.csv', 'w', newline='') as temp:
    res = csv.writer(temp)
    for cont_res in storage:
        res.writerow([cont_res.firstname, cont_res.lastname, cont_res.surname, cont_res.organization, cont_res.position, cont_res.phone, cont_res.email])

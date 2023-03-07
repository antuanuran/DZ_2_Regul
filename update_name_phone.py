from pprint import pprint
import re
import csv


with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list[0]
data = contacts_list[1:]


class Contact:
    def __init__(self, firstname, lastname, surname, organisation, position, phone, email):
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.organisation = organisation
        self.position = position
        self.phone = phone
        self.email = email

    def update(self, other):
        self.firstname = self.firstname or other.firstname
        self.lastname = self.lastname or other.lastname
        self.surname = self.surname or other.surname
        self.organisation = self.organisation or other.organisation
        self.position = self.position or other.position
        self.phone = self.phone or other.phone
        self.email = self.email or other.email

    def __eq__(self, other):
        return self.firstname == other.firstname and self.lastname == other.lastname

    def __str__(self):
        return f'{self.firstname}, {self.lastname}, {self.surname}, {self.organisation}, {self.position}, {self.phone}, {self.email}'

    def __repr__(self):
        return str(self)


# Обновление ФИО

if __name__ == '__main__':

    storage = []
    for contact in data:
        firstname, lastname, surname = contact[:3]
        temp = f'{firstname} {lastname} {surname}'.strip()
        name_all_list = temp.split()

        if len(name_all_list) == 3:
            firstname, lastname, surname = name_all_list[0:3]
            name_list = [firstname, lastname, surname]

        elif len(name_all_list) == 2:
            firstname, lastname = name_all_list[0:2]
            name_list = [firstname, lastname, ""]

        else:
            firstname = name_all_list[0]
            name_list = [firstname, "", ""]

        # Регулярка для телефона
        phone_bad = contact[5]
        pattern = r"(\+7|7|8)(\s\(|\s|\(|[ ]*)(\d{3})(\)\s|-|\)|[1]*)(\d{3})(-|\s|[1]*)(\d{2})(-|[1]*)(\d{2})($|\s\(*)([а-ё]+\.\s\d+|[1]*)(\)|[1]*)"
        phone_result = re.sub(pattern, r"+7(\3)\5-\7-\9 \11", phone_bad)

        cont = [name_list[0], name_list[1], name_list[2], contact[3], contact[4], phone_result, contact[6]]

        # ********* Обновляем контакт
        contact = Contact(cont[0], cont[1], cont[2], cont[3], cont[4], cont[5], cont[6])
        if contact in storage:
            i = storage.index(contact)
            storage[i].update(contact)
        else:
            storage.append(contact)

    pprint(storage)




    ## 2. Сохраните получившиеся данные в другой файл.
    with open("phonebook_result.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        for c in storage:
            datawriter.writerow([c.firstname, c.lastname, c.surname, c.organisation, c.position, c.phone, c.email])





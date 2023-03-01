from pprint import pprint
import read_file
import re
import csv

contacts_list = read_file.reader_csv()
header = contacts_list[0]
data = contacts_list[1:]


def text_main():
    print(f'header:{header}')
    print('data:')
    for contact in data:
        print(contact)

# Обновление ФИО
def update_name():
    cont = []
    contact_all = []

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
        contact_all.append(cont)

    return contact_all

result = update_name()

## 2. Сохраните получившиеся данные в другой файл.
with open("phonebook_result.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')

    ## Вместо contacts_list подставьте свой список:
    datawriter.writerows(result)





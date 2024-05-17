import random
import string
import smtplib
import ssl
from email.message import EmailMessage

def kasutajad_väljund(kasutajad, paroolid, valid):
    for i in range(5):
        print(f"{kasutajad[i]}, {valid[i]}, {paroolid[i]}")

def registreerimine(kasutajad, paroolid, valid):
    nimi = input("Введите имя пользователя: ")
    if nimi not in kasutajad:
        email = input("Sisesta email: ")
        parool_valik = input("Хотите создать свой пароль (введите 'ja') или сгенерировать его автоматически (введите 'ei')? ")
        if parool_valik.lower() == "ja":
            parool = input("Введите пароль: ")
            paroolid.append(parool)
            valid.append(email)
            kasutajad.append(nimi)
            sohranjaet(nimi, parool, email, "main.txt")
            print("Пользователь зарегистрирован!")
        else:
            parool = genereeri_parool()
            paroolid.append(parool)
            valid.append(email)
            kasutajad.append(nimi)
            sohranjaet(nimi, parool, email, "main.txt")
            print("Пользователь зарегистрирован!")
            print("Новый пароль: ", parool)

def autoriseeri_kasutaja(nimi, parool, kasutajad, paroolid):
    if nimi in kasutajad:
        if paroolid[kasutajad.index(nimi)] == parool:
            return True
    return False

def muuda_parool(nimi, vana_parool, uus_parool, kasutajad, paroolid):
    if autoriseeri_kasutaja(nimi, vana_parool):
        paroolid[kasutajad.index(nimi)] = uus_parool
        return "Пароль успешно изменен."
    return "Авторизация не удалась. Проверьте ваши данные."

def unusta_parool(nimi, kasutajad, paroolid):
    if nimi in kasutajad:
        indeks = kasutajad.index(nimi)
        uus_parool = genereeri_parool()
        paroolid[indeks] = uus_parool 
        print("Сгенерирован новый пароль: " + uus_parool)
    print("Такого пользователя не существует")

def genereeri_parool(pikkus=8):
    parool = ''.join(random.choices(string.ascii_letters + string.digits, k=pikkus))
    return parool

def sohranjaet(uus_user, uus_parool, uus_email, main):
    save = f"{uus_user}_{uus_parool}:{uus_email}"
    with open(main, "a") as s:
        s.write(f"{save}\n")

def tsitaetsodersimoefile(file, kasutajad, paroolid, valid):
    with open(file, 'r') as s:
        data = s.readlines()
        if len(data):
            for line in data:
                name_password_and_email = line.strip().split(':')
                email = name_password_and_email[1]
                name_and_password = name_password_and_email[0].split("_")
                name = name_and_password[0]
                password = name_and_password[1]
                kasutajad.append(name)
                paroolid.append(password)
                valid.append(email)

def otsisjaetfile(main):
    with open(main, "w") as s:
        s.write("")

def perezapisavaet(main, kasutajad, paroolid, valid):
    otsisjaetfile(main)
    for index, i in enumerate(kasutajad):
        print(kasutajad, paroolid, valid)
        sohranjaet(i, paroolid[index], valid[index], main)

def send_password_email(to_email, parool):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "kirill.tsogankov@gmail.com"  # Замененный адрес отправителя
    password = "Your_Password_Here"  # Введите свой пароль
    context = ssl.create_default_context()
    msg = EmailMessage()
    msg.set_content(f"Your password is {parool}")
    msg['Subject'] = "Your password!"
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.send_message(msg)

    except Exception as e:
        print(e)
    finally:
        server.quit()




    #kasutajad_väljund: выводит список пользователей, их статус (валиден или нет) и соответствующие пароли.

    #registreerimine: регистрирует новых пользователей, запрашивает у них имя, электронную почту и предлагает выбрать собственный пароль или сгенерировать его автоматически.

    #autoriseeri_kasutaja: проверяет правильность введенного имени пользователя и пароля.

    #muuda_parool: позволяет пользователю изменить пароль после аутентификации.

    #unusta_parool: генерирует новый пароль и отправляет его на email, если пользователь забыл свой пароль.

    #genereeri_parool: генерирует случайный пароль заданной длины.

    #sohranjaet: сохраняет информацию о новом пользователе в файл.

    #tsitaetsodersimoefile: извлекает информацию о пользователях из файла.

    #otsisjaetfile: очищает содержимое файла.

    #perezapisavaet: перезаписывает файл с информацией о пользователях после внесения изменений.

    #send_password_email: отправляет пользователю его пароль на указанный email.
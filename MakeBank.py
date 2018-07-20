import hashlib
import os.path
account = {}

salts = []


def get_salts():
    file = open("salty.txt", "r")
    for line in file:
        salts.append(line)


def salt_password(password):
    password = password.lower()
    lastletter = password[-1]
    if not lastletter.isalnum():
        index = 0
    elif lastletter.isnumeric():
        index = int(lastletter)
    else:
        indexL = ord(lastletter)
        indexA = ord('a')
        index = indexL - indexA
    salt = salts[index]
    return salt


def read_file():
    if not os.path.isfile("accounts.txt"):
        return
    f = open("accounts.txt", "r")
    for line in f:
        words = line.split(" ")
        words.pop()
        username = words[0]
        password = words[1]
        pin = words[2]
        trueanswer = words[3]
        balance = words[4]
        account.update({username: [password, pin, trueanswer, balance]})
    f.close()


def write_file():
    f = open("accounts.txt", "w")
    for username in account:
        f.write(username + " ")
        info = account[username]
        for item in info:
            f.write(str(item) + " ")
        f.write("\n")
    f.close()


def hasher(password):
    import hashlib
    b = bytes(password, 'utf-8')
    m = hashlib.sha256(b)
    m = m.hexdigest()
    return m


def withdraw(username, removebank):
    account[username][3] -= removebank
    print("You have " + str(account[username][3]) + " money ")


def login():
    print("Logging in")
    username = input("Enter Username ")
    if not account.get(username):
        print("Enter a valid username ")
        return
    password = input("Enter password ")
    password = hasher(password)
    real_password = account[username][0]
    for i in range(0, 6):
        if i == 5:
            print("Safety Lock Activated")
            break
        elif password == real_password:
            print("Welcome " + username)
            bank = input("Press 'V' to  view bank account, 'D' to deposit, and 'W' to withdraw , and 'T' to transfer ")
            while bank != 'Q':
                if bank == 'V':
                    print("You have " + str(account[username][3]) + "money ")
                    changeaccount = input("Would you like to change anything about your account  details? ")
                    if changeaccount == 'Y':
                        print("Enter you new password")
                        newpassword = input("New password ")
                        account[username:] = newpassword
                    return
                elif bank == 'W':
                    removebank = int(input("How much money would you like to withdraw? "))
                    if account[username][3] < -999:
                        print("You need to pay the bank " + str(account[username][3]) + " money")
                    elif account[username][3] == removebank:
                        print("This is a suspicious move question required ")
                        question = input("Who was you best friend? ")
                        for i in range(0, 6):
                            if i == 5:
                                print("Safety Lock Activated")
                            elif question == account[username][2]:
                                withdraw(username, removebank)
                                break
                    else:
                        withdraw(username, removebank)
                        break

                elif bank == 'T':
                    trfname = input("Who would you like to transfer money to? ")
                    trfamount = int(input("How much money would you like to transfer? "))
                    account[trfname][3] += trfamount
                    print("You have " + str(account[username][3]) + "money ")
                    print((account[trfname]) + "has received " + trfamount)
                elif bank == 'D':
                    addbank = int(input("How much money would you like to add? "))
                    account[username][3] += addbank
                    print("You have " + str(account[username][3]) + " money ")
                    break
                else:
                    print("Please enter a valid option")
                    break
            break
        else:
            print("Incorrect Password")
            password = input("Enter password ")

get_salts()
read_file()
startup = input("Press 'C' to create a new bank account, or press 'L' to login, or finally press 'Q' to quit ")
while startup != 'Q':
    if startup == 'C':
        username = input("Create Username ")
        while account.get(username):
            username = input("That username is already taken, please take a different one")
        password = input("Create password ")
        password = password + salt_password(password)
        password = hasher(password)
        pin = input("Enter PIN ")
        pin = hasher(pin)
        trueanswer = input("Who was your best friend? ")
        account.update({username: [password, pin, trueanswer, 0]})
    elif startup == 'L':
        login()
    else:
        print("Please enter a valid option")
    startup = input("Press 'C' to create a new bank account, or press 'L' to login, or finally press 'Q' to quit ")
get_salts()
write_file()

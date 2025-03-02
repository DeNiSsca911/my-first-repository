import random

random_number = random.randint(1,2)
user_number = int(input("угадай число ( от 1 до 2 ) : "))
if user_number == random_number:
    print(' УРА ВЫ ПОБЕДИЛИ !!! ')
    print( ' ::;))  великолепная эрудиция !')
else:
    print(' Вы не угадали , попробуете еще ? ')
    print(f' Было загадано число{random_number}')


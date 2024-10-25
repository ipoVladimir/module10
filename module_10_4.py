# Цель: Применить очереди в работе с потоками, используя класс Queue.
#
# Задача "Потоки гостей в кафе":
# Необходимо имитировать ситуацию с посещением гостями кафе.
# Создайте 3 класса: Table, Guest и Cafe.
# Класс Table:
#
#     Объекты этого класса должны создаваться следующим способом - Table(1)
#     Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)
#
# Класс Guest:
#
#     Должен наследоваться от класса Thread (быть потоком).
#     Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
#     Обладать атрибутом name - имя гостя.
#     Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
#
# Класс Cafe:
#
#     Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
#     Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
#     Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).
#
# Метод guest_arrival(self, *guests):
#
#     Должен принимать неограниченное кол-во гостей (объектов класса Guest).
#     Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest), запускать поток гостя и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
#     Если же свободных столов для посадки не осталось, то помещать гостя в очередь queue и выводить сообщение "<имя гостя> в очереди".
#
# Метод discuss_guests(self):
# Этот метод имитирует процесс обслуживания гостей.
#
#     Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
#     Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive), то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен". Так же текущий стол освобождается (table.guest = None).
#     Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None), то текущему столу присваивается гость взятый из очереди (queue.get()). Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
#     Далее запустить поток этого гостя (start)
#
# Таким образом мы получаем 3 класса на основе которых имитируется работа кафе:
#
#     Table - стол, хранит информацию о находящемся за ним гостем (Guest).
#     Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
#     Cafe - кафе, в котором есть определённое кол-во столов и происходит имитация прибытия гостей (guest_arrival) и их обслуживания (discuss_guests).
#
#
# Пример результата выполнения программы:
# Выполняемый код:
# class Table:
# ...
# class Guest:
# ...
# class Cafe:
# ...
# # Создание столов
# tables = [Table(number) for number in range(1, 6)]
# # Имена гостей
# guests_names = [
# 'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
# 'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
# ]
# # Создание гостей
# guests = [Guest(name) for name in guests_names]
# # Заполнение кафе столами
# cafe = Cafe(*tables)
# # Приём гостей
# cafe.guest_arrival(*guests)
# # Обслуживание гостей
# cafe.discuss_guests()
#
# Вывод на консоль (последовательность может меняться из-за случайного время пребывания гостя):
# Maria сел(-а) за стол номер 1
# Oleg сел(-а) за стол номер 2
# Vakhtang сел(-а) за стол номер 3
# Sergey сел(-а) за стол номер 4
# Darya сел(-а) за стол номер 5
# Arman в очереди
# Vitoria в очереди
# Nikita в очереди
# Galina в очереди
# Pavel в очереди
# Ilya в очереди
# Alexandra в очереди
# Oleg покушал(-а) и ушёл(ушла)
# Стол номер 2 свободен
# Arman вышел(-ла) из очереди и сел(-а) за стол номер 2
# .....
# Alexandra покушал(-а) и ушёл(ушла)
# Стол номер 4 свободен
# Pavel покушал(-а) и ушёл(ушла)
# Стол номер 3 свободен
# Примечания:
#
#     Для проверки значения на None используйте оператор is (table.guest is None).
#     Для добавления в очередь используйте метод put, для взятия - get.
#     Для проверки пустоты очереди используйте метод empty.
#     Для проверки выполнения потока в текущий момент используйте метод is_alive.

import queue
from threading import Thread
import queue
from time import sleep
from random import randint


class Table:
    def __init__(self, num_table):
        self.number = num_table
        self.guest = None

    def is_busy(self):
        return self.guest is not None

    def __str__(self):
        #return str(f"Стол: {self.number}, гость: {self.guest}")
        return "Стол: " + str(self.number)


class Guest(Thread):
    def __init__(self, name):
        self.name_guest = name
        super().__init__()

    def run(self):
        sleep(randint(3,10))


class Cafe:
    def __init__(self, *tables):
        self.queve = queue.Queue()
        self.tables = [*tables]

    """"
    возвращает индекс найденного свободного стола, 
    пока не получилось возвратить объект чтобы его потом можно было изменять
    """
    def get_free_table(self):
        for i in range(len(self.tables)):
            if not self.tables[i].is_busy():
                # return self.tables[i]
                return i
        return -1

    def exist_busy_table(self):
        for i in range(len(self.tables)):
            if self.tables[i].is_busy():
                return True
        return False
    """
    Должен принимать неограниченное кол-во гостей (объектов класса Guest).
    Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest), 
    запускать поток гостя и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
    Если же свободных столов для посадки не осталось, то помещать гостя в очередь queue и 
    выводить сообщение "<имя гостя> в очереди".
    """
    def guest_arrival(self, *guests):
        for guest in guests:
            ind_tbl = self.get_free_table()
            if ind_tbl >= 0:
                tbl = self.tables[ind_tbl]
                print(tbl.__str__())
                tbl.guest = guest
                guest.start()
                print(f"{guest.name_guest} сел(-а) за стол номер {tbl.number}")
                guest.join()
            else:
                self.queve.put(guest)
                print(f"{guest.name_guest} в очереди")

    """
    Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
    Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive), то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен". Так же текущий стол освобождается (table.guest = None).
    Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None), 
    то текущему столу присваивается гость взятый из очереди (queue.get()). 
    Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
    Далее запустить поток этого гостя (start)
    """
    def discuss_guests(self):
        while not self.queve.empty() or self.exist_busy_table():
            for tbl in self.tables:
                if tbl.is_busy() and not tbl.guest.is_alive():
                    print(f"{tbl.guest.name_guest} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {tbl.number} свободен")
                    tbl.guest = None
            if not self.queve.empty() and (ind_tbl := self.get_free_table()) >= 0:
                tbl = self.tables[ind_tbl]
                tbl.guest = self.queve.get()
                print(f"{tbl.guest.name_guest} вышел(-ла) из очереди и сел(-а) за стол номер {tbl.number}")
                tbl.guest.start()
                tbl.guest.join()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()




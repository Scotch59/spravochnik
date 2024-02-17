import csv
import sys
from PyQt5 import QtWidgets
from ui import Ui_Form
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel
import logging

file_name = 'directory.csv'  # Имя файла для хранения справочника
logging.basicConfig(level=logging.DEBUG, filename='info.txt', format='%(levelname)s (%(asctime)s) %(message)s ''(Line %(linenum)d) [%(filename)s]', datefmt='%Y-%m-%d %H:%M:%',
                     encoding='utf8', filemode='w')


title = ['Фамилия ', ' Имя ', ' Отчество ', ' Организация ', ' Рабочий телефон ', ' Сотовый телефон ']

class StartSpravochnik(QWidget, Ui_Form):
    """"
    Класс StartSpravochnik наследуется от QWidget и Ui_Form,
    что позволяет инициализировать графический интерфейс пользователя.

    Методы:
    def match_checking - метод, ищет совпадения записи, введенной пользователем
    с записями с справочнике

    def save_spravochnik - метод сохранения записей в справочник

    def edit_record - метод редактирование существующей записи

    def page - метод вывода записи со страниц

    def state_check_box - метод определения состояния флажка для поиска по критериям

    def search_record - метод поиска записи по критериям"""


    def __init__(self):
        super().__init__()
        self.setupUi(self)                                     # Инициализируем поля ввода
        self.add_a_not.clicked.connect(self.save_spravochnik)  # Подключаем метод save_spravochnik к кнопке «добавить запись»
        self.edit_entry.clicked.connect(self.edit_record)      # Подключаем метод def edit_record к кнопке «редактировать запись»
        self.find_page.clicked.connect(self.page)              # Подключаем метод page для вывода информации со страниц
        self.search.clicked.connect(self.search_record)        # Подключаем кнопку search для поиска записи по критериям
        self.msg = QMessageBox()                               # Инициализируем всплывающее окно с информацией
        self.msg.setWindowTitle("INFO")
        self.msg.setIcon(QMessageBox.Warning)
        self.firstName.stateChanged.connect(self.state_check_box)  # Инициализация флажков в виджете
        self.lastName.stateChanged.connect(self.state_check_box)
        self.surName.stateChanged.connect(self.state_check_box)
        self.organization.stateChanged.connect(self.state_check_box)
        self.workPhone.stateChanged.connect(self.state_check_box)
        self.personalPhone.stateChanged.connect(self.state_check_box)




    def match_checking(self, data):
        with open('directory.csv', 'r', encoding='cp1251') as file:
            reader = csv.reader(file)                            # Читаем строки файла и ищем совпадение
            for row in reader:
                if (',').join(row) == data:
                    return True

                else:
                    False

    def save_spravochnik(self):
        """
        Описание метода:

        Присваиваем переменной lineEdit_1 значение введенное пользователем,
        если строка ввода пуста, выводим информацию, что поле пустое.

        Проверяем, если запись введенная пользователем существует в справочнике, то
        выводим соответсвующее сообщение, если её нет, записываем в справочник и выводим
        информацию о записи данных

        """
        try:
            lineEdit_1 = self.lineEdit_1.text()
            if not lineEdit_1:
                self.msg.setText("Внимание \nВы ничего не ввели, записывать нечего.")
                self.msg.show()
            else:
                if not self.match_checking(lineEdit_1):
                    with open(file_name, 'a', encoding='cp1251', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        data = lineEdit_1.split(',')
                        writer.writerow(data)
                        self.msg.setText(f"Введенные данные записаны в файл {file_name}.")
                        self.msg.show()
                        self.lineEdit_1.clear()
                else:
                    self.msg.setText(f"Запись уже существует в  в файле {file_name}.")
                    self.msg.show()
                    self.lineEdit_1.clear()

        except Exception as e:
            logging.exception(e)



    def edit_record(self):
        """
        Описание метода:

        Присваиваем переменным lineEdit_2 и new_line значения введенные в поля и преобразовываем
        их в список, для дальнейшей работы с ними.

        Создаем новый список, сохраняем туда все записи из справочника.
        Далее удаляем запись из него которую хотим редактировать и добавляем в конец этого списка
        уже отредактированную запись.

        Записываем данные обратно в справочник.
        """
        lineEdit_2 = self.lineEdit_2.text()
        new_line = self.new_line.text()
        try:
            old_records = []
            if lineEdit_2 and new_line:
                lineEdit_2, new_line = [self.lineEdit_2.text()], [self.new_line.text()]
                with open('directory.csv', 'r', encoding='cp1251', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        old_records.append(row)
                    for i, line in enumerate(old_records):
                        if line == lineEdit_2:
                            old_records.pop(i)
                            break
                    old_records.append(new_line)
                    with open('directory.csv', 'w', encoding='cp1251', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(title)
                    for line in old_records:
                        with open("directory.csv", "a", encoding="cp1251", newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(line)
                    self.msg.setText("Запись успешно отредактирована!")
                    self.msg.show()
                    self.lineEdit_1.clear()
            else:
                self.msg.setText(f"Заполните оба поля!")
                self.msg.show()

        except Exception as e:
            logging.exception(e)

    def page(self):
        """
        Описание метода:

        Метод выводит данные с каждой страницы справочника.

        Создаем новый список, добавляем в него все записи справочника
        и выводит все данные в окно информации

        Но csv файлы не поддерживают запись на несколько страниц,
        поэтому вывод осуществлён только 1 страницы.

        Если есть необходимость использования нескольких страниц,
        то можно записать 5000 записей в этот справочник, а остальные
        во второй справочник, а затем делать вывод 2 справочника,
        по запросу 2 страницы.

        """
        info = []
        try:
            with open('directory.csv', 'r', encoding='cp1251') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    info.append((',').join(row))
                    self.listWidget.addItem((',').join(row))

        except Exception as e:
            logging.exception(e)





    def state_check_box(self):
        """
        Описание метода:

        В каждом из условий проверяется значение флажка,
        если стоит галочка, то этот флажок возвращает индекс
        по которому стоит искать запись
        """
        if self.firstName.isChecked():
            return 1
        elif self.lastName.isChecked():
            return 0
        elif self.surName.isChecked():
            return 2
        elif self.organization.isChecked():
            return 3
        elif self.workPhone.isChecked():
            return 4
        elif self.personalPhone.isChecked():
            return 5
        else:
            return False


    def search_record(self):
        """
        Описание метода:

        Проходимся по всем строкам в справочнике, делаем проверку
        на совпадение, введенной информации(пока только 1 критерий)
        и нажимаем флажок по какому критерию искать,
        если введенная информация равна 1 из значений строк, то выводим эту строку

        """
        lineEdit_3 = self.lineEdit_3.text()
        index = self.state_check_box()
        try:
            with open('directory.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if lineEdit_3 == row[index]:
                        self.listWidget.addItem((',').join(row))
                        print("Yes")
                    else:
                        print("No")

        except Exception as e:
            logging.exception(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)   # Запускается приложение с помощью app = QtWidgets.QApplication(sys.argv) и w.show().
    w = StartSpravochnik()                   # Затем sys.exit(app.exec_()) используется для завершения работы приложения.
    w.show()
    sys.exit(app.exec_())


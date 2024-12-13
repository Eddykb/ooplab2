
import csv
import os
import xml.etree.ElementTree as ET
import time


class FileManager:   #Класс для работы с данными файлами
    @staticmethod
    def prompt_for_file_path():
        while True:
            file_path = input("Введите путь до файла-справочника (или оставьте пустым для завершения): ")
            if file_path == "":
                print("Программа завершена!")
                return None
            if os.path.exists(file_path):
                if file_path.endswith('.csv') or file_path.endswith('.xml'):
                    return file_path
                else:
                    print("Ошибка: Неверный тип файла. Пожалуйста, используйте файлы XML или CSV.")
            else:
                print("Ошибка: Файл не найден.")
            retry = input("Продолжить поиск? (1 - да, 0 - нет): ")
            if retry.lower() == '0':
                return None
            elif retry.lower() != '1':
                print("Неверный ввод. Попробуйте снова...")


class DataProcess:   #Класс для обработки различных данных из файла
    def __init__(self, file_path):
        self.file_path = file_path
        self.uniq_row = {}
        self.house_calc = {}

    def load_data(self):
        if self.file_path.endswith(".csv"):
            self.process_csv()
        elif self.file_path.endswith(".xml"):
            self._process_xml()

    def process_csv(self):
        with open(self.file_path, 'r', encoding="utf-8") as f:
            next(f)  # Пропускаем заголовок
            reader = csv.reader(f, delimiter=";", quotechar='"')
            for row in reader:
                row_tuple = tuple(row)
                self.uniq_row[row_tuple] = self.uniq_row.get(row_tuple, 0) + 1

    def _process_xml(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        for item in root.findall("item"):
            city = item.get('city')
            street = item.get('street')
            house = item.get('house')
            floor = item.get('floor')
            row_tup = (city, street, house, floor)
            if all(row_tup):
                self.uniq_row[row_tup] = self.uniq_row.get(row_tup, 0) + 1

    def house_counts(self):
        for row in self.uniq_row:
            key = (row[0], row[3])
            self.house_calc[key] = self.house_calc.get(key, 0) + 1
        self.house_calc = dict(sorted(self.house_calc.items()))


class DataViewer:   #Класс для представления данных
    @staticmethod
    def duplicates_monitor(uniq_row):
        print("\nДублирующиеся записи:")
        # Заголовки
        head = ["Город", "Улица", "Номер дома", "Кол-во этажей", "Кол-во дублирующихся записей"]
        print(" | ".join(head))  # Выводим заголовки
        for key, value in uniq_row.items():
            if value > 1:
                # Выводим данные
                print(" | ".join(str(item) for item in key), f"| {value}")

        if not any(value > 1 for value in uniq_row.values()):
            print("Дублирующиеся записи не обнаружены.\n")

    @staticmethod
    def house_calc_monitor(house_counts):
        print("\nКоличество в каждом городе 1-, 2-, 3-, 4- и 5-этажных зданий:\n")
        head = ["Город", "Кол-во этажей", "Кол-во домов"]
        print(" | ".join(head))  # Заголовки
        pr_city = ""
        for (city, floors), count in house_counts.items():
            if city != pr_city:
                print("")  # Печатаем пустую строку между городами
            print(f"{city} | {floors} | {count}")
            pr_city = city


class Application:  #Класс для самого регулирования
    @staticmethod
    def run():
        while True:
            file_path = FileManager.prompt_for_file_path()
            if not file_path:
                break
            time_begin = time.time()
            processor = DataProcess(file_path)  # Создание объекта DataProcess
            processor.load_data()
            processor.house_counts()
            viewer = DataViewer()
            viewer.duplicates_monitor(processor.uniq_row)
            viewer.house_calc_monitor(processor.house_calc)
            time_finish = time.time()
            print(f"\nВремя обработки всего файла - {round(time_finish - time_begin, 5)} сек\n")
            while True:
                reque_continue = input("Продолжить поиск? (1 - да, 0 - нет): ").lower()
                if reque_continue == '1':
                    break
                elif reque_continue == '0':
                    return
                else:
                    print("Неверный ввод... Введите '1' или '0'!")


if __name__ == '__main__':
    Application().run()
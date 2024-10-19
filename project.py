from pathlib import Path
import csv


class PriceMachine():
    
    def __init__(self):
        self.data = []
        self.sorted_data = []
        self.result = ''
        self.name_length = 0
    
    def load_prices(self, file_path=''):
        path = Path(file_path)
        good_titles = ["название", "продукт", "товар", "наименование"]
        good_prices = ["цена", "розница"]
        good_weights = ["фасовка", "масса", "вес"]

        if path.is_dir():
            for file in path.iterdir():
                if file.is_file() and 'price' in file.name:
                    with open(file_path + '\\' + file.name, encoding='utf-8') as r_file:
                        file_reader = csv.reader(r_file, delimiter=",")

                        title_col = None
                        price_col = None
                        weight_col = None

                        for row_num, row in enumerate(file_reader):
                            if row_num == 0:
                                for num, col in enumerate(row):
                                    if col in good_titles:
                                        title_col = num
                                    if col in good_prices:
                                        price_col = num
                                    if col in good_weights:
                                        weight_col = num
                            else:
                                self.data.append([row[title_col], float(row[price_col]), float(row[weight_col]), file.name])
            self._sort()
            self.sorted_data = self.data.copy()
            self._export_to_html()
            print('Чтение и сортировка файлов завершены')
        else:
            print(f"{file_path} не является директорией.")

    def _sort(self):
        for first_item in range(len(self.data)):
            for second_item in range(len(self.data)):
                if self.data[first_item][1] / self.data[first_item][2] < self.data[second_item][1] / self.data[second_item][2]:
                    self.data[first_item],  self.data[second_item] = self.data[second_item], self.data[first_item]

    def _export_to_html(self, fname=r'C:\PythonUniversity\Internship\test\output.html'):

        result = '''
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Вес</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for num, item in enumerate(self.sorted_data):
            name, price, weight, file = item
            result += '<tr>'
            result += f'<td>{num+1}</td>'
            result += f'<td>{name}</td>'
            result += f'<td>{price}</td>'
            result += f'<td>{weight}</td>'
            result += f'<td>{file}</td>'
            result += f'<td>{round(price/weight, 2)}</td>'
            result += '</tr>\n'

        result += '</table></body>'

        with Path(fname).open(mode='w', encoding='utf-8') as file:
            file.write(result)
        print('Файл output.html обновлён')

    def find_text(self, text):
        self.sorted_data.clear()
        for item in self.data:
            if text in item[0]:
                self.sorted_data.append(item)
        self._export_to_html()

    def reset(self):
        self.sorted_data = self.data.copy()
        print('Фильтр сброшен')
        self._export_to_html()


def main():
    pm = PriceMachine()
    command = ''
    print('Вас приветствует программа 1С!(почти)')
    print('-'*37)
    while command != 'exit':
        print('Введите команду. Доступные команды:\n\t'
              'load - загрузка данных\n\t'
              'find - поиск товара по фрагменту\n\t'
              'reset - сбросить фильтр по фрагменту\n\t'
              'exit - выйти из программы')
        command = input()
        if command == 'load':
            print('Введите путь к папке')
            path = input()
            pm.load_prices(path)
            print()
        elif command == 'find':
            print('Введите фрагмент')
            fragment = input()
            pm.find_text(fragment)
            print()
        elif command == 'reset':
            pm.reset()
            print()
        elif command == 'exit':
            print('До свидания!')
        else:
            print('Такой команды не существует!')
            print()

if __name__ == '__main__':
    main()

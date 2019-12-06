from random import randint
from filemanager import FileManager


class CsvFormat:
    def __init__(self, column):
        self.table = []
        self.column = column
        self.row = {}

    def add_row_to_table(self, name_of_row):
        if not self.row.get(name_of_row):
            return False
        row = self.row[name_of_row]
        del self.row[name_of_row]
        self.table.append(row)
        self.filemanager = FileManager()

    def create_row(self, name_of_row):
        if not self.row.get(name_of_row):
            self.row[name_of_row] = {}
        else:
            return False

    def add_data_to_row(self, name_of_row, column, data):
        if not (self.row.get(name_of_row) and column in self.column):
            return False
        self.row[name_of_row][column] = data

    def update_row(self, name_of_row, update):
        for key, value in update.items():
            if key in self.column:
                self.row[name_of_row][key] = value
            else:
                return False

    def get_row(self, row_number=0):
        row_number -= 1
        if not self.table:
            return False
        if row_number < 0:
            return self.table[randint(0, len(self.data))]
        else:
            return self.table[row_number]

    def get_table(self):
        return self.table

    def remove_table(self):
        self.table = []

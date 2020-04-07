# encoding=utf-8
import os
import csv


class CSVManager(object):
    def __init__(self, path):
        current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self._path = os.path.join(current_path, path)

    def read(self):
        with open(self._path, 'r') as fp:
            reader = csv.reader(fp)
            # rows=list(reader)
            rows = [row for row in reader]
            return rows

    def write(self, *data):
        with open(self._path, 'w+') as fp:
            csv_writer = csv.writer(fp)
            for i in data:
                csv_writer.writerow(i)

    def write_by_two_dimension_array(self, data=None):
        """
        先清空3行以后的内容
        第一行：字段名称
        第二行：字段类型
        第三行：字段边界范围
        再写入
        后面的：通过正交穷举生成的数据
        """
        if data is None:
            data = [[]]

        with open(self._path, 'r') as fp:
            reader = csv.reader(fp)
            reader_lines = [i for i in reader]

        with open(self._path, 'w') as fp:
            csv_writer = csv.writer(fp)
            for i in reader_lines[:3]:
                csv_writer.writerow(i)

        with open(self._path, 'a+') as fp:
            csv_writer = csv.writer(fp)
            for i in range(len(data)):
                csv_writer.writerow([i] + data[i])

    def add(self, *data):
        context = len(self.read())
        with open(self._path, 'a+') as fp:
            csv_writer = csv.writer(fp)
            count = 0
            for i in data:
                if context != 0 and count >= 1:
                    csv_writer.writerow(i)
                count += 1

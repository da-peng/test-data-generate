import csv
import xlrd

class Param(object):
    def __init__(self, param_conf='{}'):
        # self.paramConf = api-request-body.loads(param_conf)
        pass

    def param_rows_count(self):
        pass

    def param_cols_count(self):
        pass

    def param_header(self):
        pass

    def param_type(self):
        pass

    def param_all_line(self):
        pass

    def param_all_line_dict(self):
        pass


class CSV(Param):
    def __init__(self, param_conf):
        """
        :param param_conf:
        file文件路径
        """
        self.paramConf = param_conf
        self.param_file = self.paramConf['file']
        with open(self.param_file, 'r') as fp:
            reader = csv.reader(fp)
            self.data = [row for row in reader]

    def param_rows_count(self):
        return len(self.data)

    def param_cols_count(self):
        """
        最后1列不读（是填写预期结果），所以-1
        :return:
        """
        return len(self.data[0]) - 1

    def param_header(self):
        """
        字段名 第一行
        :return:
        """
        return self.data[0]

    def param_type(self):
        """
        字段类型 第二行
        :return:
        """
        return self.data[1]

    def boundary_condition(self, n_row):
        """
        字段边界条件 第三行
        :return:
        """
        return self.data[2]

    def param_all_line(self):
        return self.data

    def get_one_line(self, row):
        return self.data[row]

    def param_all_line_dict(self):
        """
            {
            0:{a:b},
            1:{a:c},
            2:{a:c}
            }
            :return:
        """
        n_count_rows = self.param_rows_count()
        n_count_cols = self.param_cols_count()  # 这里是-1 去掉最后一列显示"预期结果"
        param_all_list_dict = {}
        i_row_step = 3  # 从4行开始 组装数据
        i_col_step = 1  # 这里是从1 开始 去掉 说明 或 每行item
        param_header = self.param_header()
        param_type = self.param_type()
        while i_row_step < n_count_rows:
            param_one_line_list = self.get_one_line(i_row_step)
            param_one_line_dict = {}
            while i_col_step < n_count_cols:
                try:
                    multi_types = param_type[i_col_step]
                    if ';' in multi_types:
                        multi_type = multi_types.split(';')[0].strip()
                    else:
                        multi_type = param_type[i_col_step].strip()
                    if multi_type == 'str':
                        value = str(param_one_line_list[i_col_step])
                    elif multi_type == 'int':
                        value = int(param_one_line_list[i_col_step])
                except Exception as e:
                    raise Exception('')
                param_one_line_dict[param_header[i_col_step]] = value
                i_col_step = i_col_step + 1
            i_col_step = 0
            param_all_list_dict[i_row_step - 2] = param_one_line_dict
            i_row_step = i_row_step + 1

        return param_all_list_dict


class XLS(Param):
    def __init__(self, param_conf):
        """
        :param param_conf: 字典
        xls
        文件位置(绝对路径)
        """
        self.paramConf = param_conf
        self.param_file = self.paramConf['file']
        self.data = xlrd.open_workbook(self.param_file)
        self.get_param_sheet(self.paramConf['sheet'])

    def get_param_sheet(self, n_sheets):
        """
        设定参数所处的sheet :param nsheets:
        参数在第几个sheet中
        :return:
        """
        self.param_sheet = self.data.sheets()[n_sheets]

    def get_one_line(self, n_Row):
        """
        返回一行数据
        :param n_Row: 行数
        :return: 一行数据 []
        """
        return self.param_sheet.row_values(n_Row)

    def get_one_col(self, n_col):

        """
        返回一列
        :param n_col: 列数
        :return: 一列数据 []
        """
        return self.param_sheet.col_values(n_col)

    def param_rows_count(self):
        """
        获取参数文件行数
        :return: 参数行数 int
        """
        return self.param_sheet.nrows

    def param_cols_count(self):
        """
        获取参数文件列数(参数个数) :return: 参数文件列数(参数个数) int
        """

        return self.param_sheet.ncols

    def param_header(self):
        """
        获取参数名称
        :return: 参数名称[]
        """

        return self.get_one_line(1)

    def param_all_line_dict(self):
        """
        获取全部参数
        :return: {{}},其中dict的key值是header的值
        """

        n_count_rows = self.param_rows_count()
        n_count_cols = self.param_cols_count()
        param_all_list_dict = {}
        i_row_step = 2
        i_col_step = 0
        param_header = self.param_header()
        while i_row_step < n_count_rows:
            param_one_line_list = self.get_one_line(i_row_step)
            param_one_line_dict = {}
        while i_col_step < n_count_cols:
            param_one_line_dict[param_header[i_col_step]] = param_one_line_list[i_col_step]
            i_col_step = i_col_step + 1
        i_col_step = 0
        param_all_list_dict[i_row_step - 2] = param_one_line_dict
        i_row_step = i_row_step + 1
        return param_all_list_dict

    def param_all_line(self):
        """
        获取全部参数
        :return: 全部参数[[]]
        """
        n_count_rows = self.param_rows_count()
        param_all = []
        i_row_step = 2
        while i_row_step < n_count_rows:
            param_all.append(self.get_one_line(i_row_step))
            i_row_step = i_row_step + 1
        return param_all

    def __get_param_cell(self, number_row, number_col):
        return self.param_sheet.cell_value(number_row, number_col)


class ParamFactory(object):

    @staticmethod
    def choose_param(types, param_conf):
        map_ = {
            'xls': XLS,
            'random-test-data': CSV
        }
        return map_[types](param_conf)


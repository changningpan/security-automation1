import xlrd
import config
from connectservers.ConnectToServers import connectservers


filepath = config.ReadConfigfile()


def read_excel(filepath):
    workbook = xlrd.open_workbook(filepath)
    #worksheets = workbook.sheet_names()
    worksheet1 = workbook.sheet_by_name(u'Sheet1')
    num_rows = worksheet1.nrows
    #for curr_row in range(num_rows):
    #    row = worksheet1.row_values(curr_row)
    #    print('row%s is %s' %(curr_row,row))
    num_cols = worksheet1.ncols
    colnames = worksheet1.row_values(0)
    #for curr_col in range(num_cols):
    #    col = worksheet1.col_values(curr_col)
    #    print('col%s is %s' %(curr_col, col))
    #for row in range(num_rows):
    #    for col in range(num_cols):
    #        cell = worksheet1.cell_value(row, col)
    #        print(cell)
    list = []
    for rownum in range(1, num_rows):
        row = worksheet1.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
            connectservers(list[0].get("server ip"), list[0].get("username"), list[0].get("password"), list[0].get("server name"))
            list.clear()
    #return list


read_excel(filepath)

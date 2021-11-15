import xlrd
import csv

fileName = 'data/prescription.xls'
fileData = xlrd.open_workbook(fileName)
table = fileData.sheets()[0]
data = []
for i in range(1, table.nrows - 1):  # table.nrows-1 总行数
    temp = table.row_values(i)[1]
    tempList = temp.split(';')
    tempList.pop()  # 删除最后一个空格
    dataList = []
    for item in tempList:
        item = item[0:item.find(':')]
        dataList.append(item)
    data.append(dataList)
print(data)
f = open('prescription.csv', 'w', newline='', encoding='utf-8')
# csv_writer = csv.writer(f)
# csv_writer.writerow(data)
for item in data:
    csv_writer = csv.writer(f)
    print(item)
    csv_writer.writerow(item)
f.close()


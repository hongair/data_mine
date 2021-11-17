import copy
import csv

import xlrd


class Apriori:
    def __init__(self, data, support, confidence, size):
        self.data = data
        self.support = support
        self.confidence = confidence
        self.size = size

    def create_c1(self):
        item_set = set()
        for item in self.data:
            for i in item:
                # print("i", i)
                temp = frozenset([i])
                item_set.add(temp)
        print(item_set)
        item_count = {}
        for item in self.data:
            for key in item_set:
                if key.issubset(item):
                    if key not in item_count:
                        item_count[key] = 1
                    else:
                        item_count[key] += 1
        print("item_count", item_count)
        c1 = {}
        length = len(self.data)
        for key in item_count:
            c1[key] = round(item_count[key] / length, 3)
        print("c1: ", c1)
        return c1

    def create_l1(self, c1):
        l1 = {}
        for key in c1:
            if c1[key] >= self.support:
                l1[key] = c1[key]
        print("L1: ", l1)
        return l1

    def create_c_k(self, k, l_k_1):
        if len(l_k_1) == 0:  # 若为空
            return []
        print(k)
        print(l_k_1)
        item_set = set()
        item_set_count = {}  # 统计每一项出现的次数
        c_k = {}
        for key1 in l_k_1:
            for key2 in l_k_1:
                if key1 == key2:
                    continue
                # 构建先的集合
                tempItem = set(key1)
                for i in key2:
                    tempItem.add(i)
                # print(tempItem)
                if len(tempItem) != k:
                    continue
                if tempItem not in item_set:
                    tempItem = frozenset(tempItem)
                    item_set.add(tempItem)
                    for item in self.data:
                        if tempItem.issubset(item):
                            if tempItem in item_set_count:
                                item_set_count[tempItem] += 1
                            else:
                                item_set_count[tempItem] = 1

        print(item_set_count)
        length = len(self.data)
        for item in item_set_count:
            value = round(item_set_count[item] / length, 3)
            c_k[item] = value
        print("C", k, ": ", c_k)
        return c_k

    def create_l_k(self, k, c_k):
        if len(c_k) == 0:  # 若为空
            return []
        l_k = {}
        for item in c_k:
            if c_k[item] >= self.support:
                l_k[item] = c_k[item]
        print("L", k, ": ", l_k)
        return l_k

    def check_min_confidence(self, c, c_1):
        rule_list = []
        for i in c:
            tempSet = copy.deepcopy(i)
            tempSet = set(tempSet)
            tempSet.pop()
            tempSet = frozenset(tempSet)
            if tempSet in c_1:
                conf = round(c_1[tempSet] / c[i], 3)
                if conf >= self.confidence:
                    tempList = [i, c[i], conf]
                    rule_list.append(tempList)
        for item in rule_list:
            print(item)
        return rule_list

    def generateRule(self):
        names = self.__dict__
        C1 = self.create_c1()
        L1 = self.create_l1(C1)
        C_list = [C1]
        L_list = [L1]

        C = copy.deepcopy(C1)
        L = copy.deepcopy(L1)
        for i in range(2, 4):  # 建立C2-C5,L2-L5
            C = self.create_c_k(i, L)
            L = self.create_l_k(i, C)
            C_list.append(C)
            L_list.append(L)
        self.check_min_confidence(L_list[2], C_list[1])  # 检查置信度
        return C
        # L1 = [[['15052'], 0.331], [['15068'], 0.134]]
        # for i in range(2, 6):  # 动态建立C2-C5,L2-L5
        # exec('C{} = self.create_c_k({}, L{})'.format(i, i, i-1))
        # exec('L{} = self.create_l_k({}, C{})'.format(i, i, i))
        # names = locals()
        # for i in range(2, 6):  # 动态建立C2-C5,L2-L5
        #     exec("names['C' + str(i)] = self.create_c_k(i, A.L%s)" % (i-1))
        #     exec("names['L' + str(i)] = self.create_l_k(i, A.C%s)" % i)
        #     # names['C' + str(i)] = 1
        #     # names['L' + str(i)] = 1
        # for i in range(5, 0):
        #     exec("print(A.C%s)" % i)
        #     if exec("len(A.C%s) != 0" % i):
        #         exec("%s" % i)
        #         exec("return A.C%s" % i)
        #         break
        # return A.C3

def load_data_old(fileName):
    fileData = xlrd.open_workbook(fileName)
    table = fileData.sheets()[0]
    data = []
    for i in range(1, table.nrows - 1):  # table.nrows-1 总行数
        tempData = [table.row_values(i)[0]]
        # print(table.row_values(i)[0])
        temp = table.row_values(i)[1]
        tempList = temp.split(';')
        tempList.pop()  # 删除最后一个空格
        dataList = []
        for item in tempList:
            item = item[0:item.find(':')]
            dataList.append(item)
        tempData.append(dataList)
        data.append(tempData)
    # for item in data:
    #     print(item)
    return data


def load_data(fileName):
    data = []
    with open(fileName, encoding="gbk") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            data.append(row)
    # print(data)
    return data


def saveRule(saveFile, L):
    with open(saveFile, "w") as f:
        for item in L:
            f.write("{")
            count = 1
            for i in item:
                if count == 1:
                    f.write(str(i))
                    count = 2
                else:
                    f.write(", ")
                    f.write(str(i))
            f.write("}")
            f.write("-->")
            f.write(str(L[item]))
            f.write('\n')


if __name__ == '__main__':
    support = 0.05  # 最小支持度
    confidence = 0.05  # 最小置信度
    size = 5  # 频繁项最大大小
    fileName = 'prescription.csv'
    saveFile = 'prescription_rule.txt'
    data = load_data(fileName)
    A = Apriori(data, support, confidence, size)
    rule = A.generateRule()
    saveRule(saveFile, rule)

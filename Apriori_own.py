import copy

import xlrd


class Apriori:
    def __init__(self, data, support, confidence, size):
        self.data = data
        self.support = support
        self.confidence = confidence
        self.size = size

    def create_c1(self):
        item_set = {}  # 统计每一项出现的次数
        for item in self.data:
            for i in item[1]:
                if i not in item_set:
                    item_set[i] = 1
                else:
                    item_set[i] += 1
        print(item_set)
        c1 = []
        length = len(self.data)
        for key in item_set:
            value = round(item_set[key] / length, 3)  # 保留3位小数
            keyList = [key]  # 转为list,为后续处理方便
            tempList = [keyList, value]
            c1.append(tempList)
        print("C 1: ", c1)
        return c1

    def create_l1(self, c1):
        l1 = []
        for item in c1:
            if item[1] >= self.support:
                l1.append(item)
        print("L 1: ", c1)
        return l1

    def create_c_k(self, k, l_k_1):
        if len(l_k_1) == 0:  # 若为空
            return []
        # print(k)
        # print(l_k_1)
        item_set = []
        item_set_count = []  # 统计每一项出现的次数
        c_k = []
        for key1 in l_k_1:
            for key2 in l_k_1:
                if key1 == key2:
                    continue
                # 构建先的集合
                tempItem = []
                for i in key1[0]:
                    tempItem.append(i)
                for i in key2[0]:
                    if i not in tempItem:
                        tempItem.append(i)
                # print(tempItem)
                tempItem = sorted(tempItem)
                if tempItem not in item_set:
                    item_set.append(tempItem)
                    # 计算项集的出现次数
                    # for item in self.data:
                    #     flag = True  # 默认都在
                    #     for i in tempItem:
                    #         if i not in item[1]:
                    #             # print(i, item)
                    #             flag = False
                    #             break
                    tempItem = frozenset(tempItem)
                    for item in self.data:
                        flag = tempItem.issubset(item)
                        if flag:
                            # print(tempItem, item in item_set_count)
                            is_in_set = False  # 是否在集合中，默认不在
                            for index in range(len(item_set_count)):
                                if item_set_count[index][0] == tempItem:
                                    item_set_count[index][1] += 1
                                    is_in_set = True
                            if is_in_set is False:
                                item_set_count.append([tempItem, 1])
        print(item_set_count)
        length = len(self.data)
        for item in item_set_count:
            value = round(item[1] / length, 3)
            c_k.append([item[0], value])
        print("C", k, ": ", c_k)
        return c_k

    def create_l_k(self, k, c_k):
        if len(c_k) == 0:  # 若为空
            return []
        l_k = []
        for item in c_k:
            if item[1] >= self.support:
                l_k.append(item)
        print("L", k, ": ", l_k)
        return l_k

    def generateRule(self):
        names = self.__dict__
        C1 = self.create_c1()
        L1 = self.create_l1(C1)
        C = copy.deepcopy(C1)
        L = copy.deepcopy(L1)
        for i in range(2, 4):  # 建立C2-C5,L2-L5
            C = self.create_c_k(i, L)
            L = self.create_l_k(i, C)
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

def load_data(fileName):
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


def saveRule(saveFile, L):
    with open(saveFile, "w") as f:
        for item in L:
            f.write(str(item))
            f.write('\n')


if __name__ == '__main__':
    support = 0.05  # 最小支持度
    confidence = 0.5  # 最小置信度
    size = 5  # 频繁项最大大小
    fileName = 'data/prescription.xls'
    saveFile = 'output/prescription_rule.txt'
    data = load_data(fileName)
    A = Apriori(data, support, confidence, size)
    rule = A.generateRule()
    saveRule(saveFile, rule)

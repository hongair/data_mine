import copy


def check_min_confidence(c, c_1):
    rule_list = []
    for i in c:
        print("i", i)
        tempSet = copy.deepcopy(i)
        tempSet = set(tempSet)
        tempSet.pop()
        tempSet = frozenset(tempSet)
        print("i", i)
        print("tempSet", tempSet)
        if tempSet in c_1:
            conf = c_1[tempSet] / c[i]
            print(conf)
            if conf >= 0.1:
                tempList = [i, c[i], conf]
                rule_list.append(tempList)
    return rule_list

if __name__ == '__main__':
    C = {frozenset({'14246', '15190', '15204'}): 0.013, frozenset({'14246', '15190', '15206'}): 0.016, frozenset({'14132', '14246', '15190'}): 0.011}
    C1 = {frozenset({'14970', '15190'}): 0.029, frozenset({'14246', '15190'}): 0.06, frozenset({'15229', '15190'}): 0.023, frozenset({'15190', '14994'}): 0.016}
    check_min_confidence(C, C1)
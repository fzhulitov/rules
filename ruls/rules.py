from itertools import combinations
import copy


def from_row_to_dict(inrow, expl='Survived') -> dict:
    if expl in inrow.keys():
        ab = inrow[expl]
        del inrow[expl]
    else:
        ab = None
    fulllist = []
    for i in range(1,len(inrow)+1):
        data = list(combinations(inrow.items(), i))
        fulllist += data
    outdict = dict.fromkeys(fulllist, ab)
    return outdict


def rules_from_dict(jdict, rules) -> dict:
    for rowval in jdict.values():
        val = rowval[rules['Explained']]

        if val in rules['resdict'].keys():
            rules['resdict'][val] += 1
        else:
            rules['resdict'][val] = 1

        rule_from_row = from_row_to_dict(rowval, rules['Explained'])

        for k, v in rule_from_row.items():
            if k in rules['data'].keys():
                if val in rules['data'][k].keys():
                    rules['data'][k][val] += 1
                else:
                    rules['data'][k][val] = 1
            else:
                rules['data'][k] = dict()
                rules['data'][k][val] = 1
    return rules


def rule_acc(expl_dic, row_dic):
    sumtot = 0
    mt = 0
    mp = 0
    for v in row_dic.values():
        sumtot += v
    t = dict()
    p = dict()
    for k, v in row_dic.items():
        t[k] = v/sumtot
        p[k] = v/expl_dic[k]
        if t[k] > mt:
            mt = t[k]
        if p[k] > mp:
            mp = p[k]
    row_dic["S"] = sumtot
    row_dic["MT"] = mt
    row_dic["MP"] = mp
    row_dic["T"] = copy.deepcopy(t)
    row_dic["P"] = copy.deepcopy(p)



def count_accurasity(rules, name_dic, name_expl='Explained') -> dict:
    tmp_dic = copy.deepcopy(rules[name_dic])
    expl_str = rules[name_expl]
    del rules[name_dic]
    del rules[name_expl]

    for k, v in rules['data'].items():
        rule_acc(tmp_dic, v)

    rules[name_dic] = copy.deepcopy(tmp_dic)
    rules[name_expl] = expl_str
    return rules

import json
import os.path
import pickle
import pandas as pd
import ruls


def get_rules() -> dict:
    if os.path.isfile("rulesm.pkl"):
        fp = open("rulesm.pkl", "rb")
        jsstr = fp.read()
        fp.close()
        rulesm = pickle.loads(jsstr)
    else:
#train base
        df = pd.read_csv('train.csv')
        df.set_index('PassengerId', inplace=True)
        jdf = df.to_json(orient="index")
        jdictm = json.loads(jdf)

# Creating rules structure
#dicttionary for ruls initial
        rulesm = dict()
        rulesm['resdict'] = dict()
        rulesm['Explained'] = 'Survived'
        rulesm['data'] = dict()

#Filling structure by rules
        ruls.rules_from_dict(jdictm, rulesm)
        ruls.count_accurasity(rulesm,'resdict')
        jsstring = pickle.dumps(rulesm, protocol=0)
        fp = open('rulesm.pkl',"x")
        fp.close()
        fp = open('rulesm.pkl',"wb")
        fp.write(jsstring)
        fp.close()
    return rulesm


rulesm = get_rules()
list_key =list()
for k, v in rulesm['data'].items():
    a = 0
    b = 1
    if a in v.keys() and b in v.keys():
        if v[a] == v[b]:
            list_key.append(k)

for k in list_key:
    print(rulesm['data'][k], k)


#Test base
df_check = pd.read_csv('test.csv')
df_check.set_index('PassengerId', inplace=True)
jdf_check = df_check.to_json(orient="index")
jdict_check = json.loads(jdf_check)

#Creating Structure for store check result
check_dic = dict()
check_dic['results'] = dict()

def get_max(rdict):
    max = 0
    summ = 0
    strkey = ""
    list_res = list()
    if len(rdict) == 0:
        return 'Error - Empty dictionary'
    else:
        for k, v in rdict.items():
            summ +=v
            if v > max:
                max = v
        for k, v in rdict.items():
            if v == max:
                kstr = str(k)
                list_res.append((kstr,max/summ))
                strkey += kstr + ' ' + str(max/summ) + ' '
    return list_res
count_err = 0
for k, v in jdict_check.items():
    svhold = '  '
    strresult = str(k) + ' ' + svhold
    check_dic['results'][k] = ruls.check_row(k,v,rulesm)

    tres = ''
    lr = get_max(check_dic['results'][k]['total'])
    lp = get_max(check_dic['results'][k]['totT*P'])
    if len(lr) == 1:
        sqr, sqp = lr.pop()
        tres = str(sqr)
        if len(lp) == 1:
            stpr, stpp = lp.pop()
            tres = str(stpr)
        else:
            max = 0
            for it in lp:
                if it[1] >max:
                    max = it[1]
            for it in lp:
                if it[1] == max:
                    stpr, stpp = it
    else:
        if len(lp) == 1:
            stpr, stpp = lp.pop()
            tres = str(stpr)
        else:
            max = 0
            for it in lp:
                if it[1] >max:
                    max = it[1]
            for it in lp:
                if it[1] == max:
                    tres = str(it[0])
 #   if sqr != stpr:
 #       if stpp >= sqp:
 #           tres = stpr
 #       else:
 #           tres = sqr
 #   else:
    tres = sqr
    strresult += '='+tres
    strresult += " SQ " + str(sqr)+'-'+str(sqp)
    strresult += " ST*P " + str(stpr)+'-'+str(stpp)
    if sqr != stpr:
        count_err += 1
        print(strresult)
        print(len(check_dic['results'][k]['no_pref']),
              check_dic['results'][k]['total'],
              check_dic['results'][k]['totT*P'])

    aa = 1

print(count_err)
jsstring = pickle.dumps(check_dic, protocol=0)
if not os.path.isfile('check2.pkl'):
    fp = open('check2.pkl', "x")
    fp.close()
fp = open('check2.pkl', "wb")
fp.write(jsstring)
fp.close()

print(len(rulesm))

testdic = {'Pclass': 3, 'Name': 'Braund, Mr. Owen Harris',
           'Sex': 'male', 'Age': 22.0, 'SibSp': 1, 'Parch': 0, 'Ticket': 'A/5 21171',
           'Fare': 7.25, 'Cabin': None, 'Embarked': 'S'}

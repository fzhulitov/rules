import copy

import ruls


## Result of rule, Have yo decide///// Not finished
def res_for_rule(rule_desc, list_res) ->dict:
    res_dict = dict()
    max_t = 0
    max_res = ''
    for k, v in list_res.items():
        if k in rule_desc.keys():
            if rule_desc['T'][k] == rule_desc['MT']:
                if rule_desc['P'] == rule_desc['MP']:
                   res_dict[k] = tuple((rule_desc['T'][k], rule_desc['P'][k]))

    return copy.deepcopy(res_dict)

def check_row (key,row,rules) ->dict:
    ext_dict = dict()
    used = dict()
    unused = dict()
    no_pref = dict()
    rrul = ruls.from_row_to_dict(row)
    for k, v in rrul.items():
        if k in rules['data'].keys():
            used[k] = rules['data'][k]
            used[k]['result'] = res_for_rule(used[k],rules['resdict'])
        else:
            unused[k] = v
    ext_dict['total'] = dict()
    ext_dict['totT*P'] = dict()
    for k, v in used.items():
        if len(v['result']) == 1:
            for vr, data in v['result'].items():
                if vr in ext_dict['total']:
                    ext_dict['total'][vr] +=1
                    ext_dict['totT*P'][vr] += data[0]*data[1]
                else:
                    ext_dict['total'][vr] = 1
                    ext_dict['totT*P'][vr] = data[0]*data[1]
        else:
            no_pref[k] = v

    for k in no_pref.keys():
        del  used[k]
    ext_dict['used'] = used
    ext_dict['unused'] = unused
    ext_dict['no_pref'] = no_pref
    return copy.deepcopy(ext_dict)


def make_datas(datas:list, pay_list):
    if not pay_list[1] in ',':
        datas.append(pay_list)
    else:
        temp_list = ["", ""]
        datas.append(temp_list)

    return datas

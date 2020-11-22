# -*- coding: utf-8 -*-
import csv
import json
import os
import datetime

import pandas as pd
import calc_income_tax
import make_pdf

csv_to_path = '/Users/bayashi/Desktop/make_pdf/csv'
paf_to_path = '/Users/bayashi/Desktop/make_pdf/pdf'
delete_to_csv = '/Users/bayashi/Desktop/make_pdf/csv/del_to_csv_tmp.csv'
error_path ='../error.txt'

dt_now = datetime.datetime.now()

def find_csv():
    # 現状の処理は1csvのみしか対応していない
    # 複数のcsvをキャッチするにはListで返却する
    files = os.listdir(csv_to_path)
    print(files)
    # csv_file = files[0]
    csv_file_list = []
    for file in files:
        if '.' in file:
            ext = file.split('.')[1]
            if not ext == 'csv':
                print('csvではありません')
                continue
            if file == 'del_to_csv_tmp.csv':
                print('削除対象ファイルです')
                continue
            csv_to = csv_to_path + '/' + file
            csv_file_list.append(csv_to)
            print(csv_file_list)
    return csv_file_list


def csv_to_json(csv_path):
    # 巻き取ったcsvをJson形式に変換する
    df = pd.read_csv(csv_path, header=None)
    df2 = df.copy()
    droped_df = df2.drop(1)
    droped_df = droped_df.drop(0)
    droped_df.to_csv(delete_to_csv, header=None, index=False)
    # df_tmp = pd.read_csv(delete_to_csv)
    json_list = []
    with open(delete_to_csv, 'r') as f:
        for row in csv.DictReader(f):
            json_list.append(row)
    with open(csv_to_path + '/output.json', 'w') as f:
        json.dump(json_list, f)
    os.remove(delete_to_csv)
    # 処理の最後にjson消す
    return json_list


def calc_tax(json_list):
    for one_person in json_list:
        # TODO 強制的に1
        supporter = 1
        total = one_person['総合計']
        koujo = one_person['社会保険等控除額計']

        if total == '':
            # 人がいない場合は処理続行
            continue

        if supporter == '':
            supporter = 0
        else:
            supporter = int(supporter)

        if koujo == '':
            koujo = str(0)

        total = int(total.replace(',', ''))
        koujo = int(koujo.replace(',', ''))
        tax = calc_income_tax.calc_tax(total, supporter)

        one_person['所得税'] = tax
        one_person['総合計'] = (total - tax)
        one_person['社会保険等控除額計'] = (koujo + tax)

    return json_list


def main():

    #エラーファイルを削除
    del_error()



    # csvファイル名を含んだパスを取得
    csv_paths = find_csv()

    try:
        for csv_path in csv_paths:
            # csvをjsonに変換する
            json_list = csv_to_json(csv_path)
            # 所得税を計算 かつ 総支給額を再計算
            json_list = calc_tax(json_list)
            # PDFを作成する
            pdf_list = make_pdf.make(json_list)
    except ValueError:
        s = str(dt_now) + ' 数字以外の値があります'
        with open(error_path, mode='w') as f:
            f.write(s)
    except TypeError:
        s = str(dt_now) + ' 数字以外の値があります'
        with open(error_path, mode='w') as f:
            f.write(s)


def del_error():
    if os.path.exists(error_path):
        os.remove(error_path)


# 作成
if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors

pdf_to_path = '/Users/bayashi/Desktop/make_pdf/pdf/'


# 初期設定
def make(json_list):  # ファイル名
    pdf_list = []
    for one_person in json_list:

        total = one_person['支給計']
        print(total)
        if total == '':
            # 人がいない場合は処理続行
            continue

        pdf_canvas = set_info(one_person)  # キャンバス名
        print_string(one_person, pdf_canvas)
        pdf_canvas.save()  # 保存
        # PDFファイルを返却
        pdf_list.append(pdf_canvas)
    return pdf_list


def set_info(one_person):
    save_path = pdf_to_path + one_person['名前'] + ".pdf"
    pdf_canvas = canvas.Canvas(save_path, pagesize=landscape(A4))  # 保存先
    pdf_canvas.setAuthor("W-GROUP")  # 作者
    pdf_canvas.setTitle("給与明細")  # 表題
    pdf_canvas.setSubject("W-GROUP 給与明細")  # 件名
    return pdf_canvas


# 履歴書フォーマット作成
def print_string(one_person, pdf_canvas):
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))  # フォント
    width, height = A4  # 用紙サイズ

    font_size = 20  # フォントサイズ
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(20 * mm, 187 * mm, one_person['給与支給日'].split('月')[0]+'月分')  # 書き出し(横位置, 縦位置, 文字)

    # 明細書
    font_size = 28  # フォントサイズ
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(120 * mm, 185 * mm, '給与明細書')  # 書き出し(横位置, 縦位置, 文字)

    # 作成日
    font_size = 15
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(200 * mm, 190 * mm, '支給日     ' + one_person['給与支給日'])

    # 氏名
    # 氏名と様の隙間は半角40
    font_size = 15
    pdf_canvas.setFont('HeiseiKakuGo-W5', 15)
    name = one_person['名前']
    pdf_canvas.drawString(20 * mm, 172 * mm, '氏名                    ' + name + '        様')

    pdf_canvas.setLineWidth(1)
    # .line(始点x,始点y,終点x,終点y)
    pdf_canvas.line(20 * mm, 170 * mm, 280, 482)

    # 氏名
    # 氏名と様の隙間は半角40
    font_size = 15
    company = one_person['支給元会社']
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(223 * mm, 165 * mm, company)

    # (6)1列目
    # 上段の空白は22
    working_days = one_person['出勤日数']
    rest_days = one_person['欠勤日数']
    slow_days = one_person['遅刻早退回数']

    data = [
        ['                      勤怠', ''],
        ['出勤日数', working_days],
        ['欠勤日数', rest_days],
        ['遅刻早退回数', slow_days],
        ['', ' '],
        ['', ' '],
        ['', ' '],
        ['', ' '],
        ['', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],

    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (1, 0)),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 10 * mm, 40 * mm)

    # (6)1列目 2段目
    data = [
        ['税額表 ', '甲欄'],
        ['扶養人数', ' '],
    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 10 * mm, 16 * mm)
    # (6)2列名扶養人数

    base_salary = one_person['基本給']

    data = [
        ['                      支給   ', ''],
        ['基本給（時給）', base_salary],
    ]


    admin_total = one_person['役職手当']
    admin_list =  ['役職手当', admin_total]
    data = make_datas(data, admin_list)
    front_pay = one_person['フロント手当']
    front_list = ['フロント手当', front_pay]
    data = make_datas(data, front_list)
    month_pay = one_person['月給手当']
    month_list = ['月給手当', month_pay]
    data = make_datas(data, month_list)
    overtime_pay = one_person['定額残業手当']
    overtime_list = ['定額残業手当', overtime_pay]
    data = make_datas(data, overtime_list)

    older_pay = one_person['年功手当']
    tech_pay = one_person['技能手当']
    special_pay = one_person['特別手当']
    holiday_pay = one_person['土日手当']
    # 諸手当 計算
    other_pay = delete_commma(older_pay) + delete_commma(tech_pay) + delete_commma(holiday_pay) + delete_commma(special_pay)
    other_pay = add_commma(other_pay)
    other_list = ['諸手当', other_pay]
    data = make_datas(data, other_list)

    every_total = one_person['皆勤手当']
    every_list = ['皆勤手当', every_total]
    data = make_datas(data, every_list)
    meal_total = one_person['食事手当']
    meal_list =['食事手当', meal_total]
    data = make_datas(data, meal_list)
    transportation_expenses = one_person['交通費']
    transportation_list = ['非課税通勤費', transportation_expenses]
    data = make_datas(data, transportation_list)

    adjust_total = one_person['調整金']
    adjust_list = ['調整金', adjust_total]
    data = make_datas(data, adjust_list)
    pre_month_total = one_person['前月修正']
    pre_month_list =  ['前月修正', pre_month_total]
    data = make_datas(data, pre_month_list)

    #空白で整える
    check_list_pay(data)

    # 合計
    pay_total = one_person['支給計']
    pay_total_list = ['合計', pay_total]
    data = make_datas(data, pay_total_list)



    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (1, 0)),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 80 * mm, 16 * mm)

    ###########

    heath_pay = one_person['健康保険料']
    ins_pay = one_person['介護保険料']
    pension_pay = one_person['厚生年金保険']
    labor_pay = one_person['雇用保険料']
    income_tax = one_person['所得税']
    total_kojo = one_person['社会保険等控除額計']
    # プラス所得税の計算

    # (6)３列目
    data = [
        ['                      控除   ', ''],
        ['健康保険料', heath_pay],
        ['介護保険料', ins_pay],
        ['厚生年金保険', pension_pay],
        ['雇用保険料', labor_pay],
        ['所得税', income_tax],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        ['合計', total_kojo],
    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (1, 0)),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 150 * mm, 16 * mm)

    # (6)4列目 一段目
    data = [
        ['                     その他   ', ''],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        ['合計', 0],
    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (1, 0)),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 220 * mm, 88 * mm)

    # (6)4列目 2段目
    data = [
        ['現金支給', "{:,d}".format(one_person['総合計'])],
    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 220 * mm, 65 * mm)

    # (6)4列目 3段目
    data = [
        ['現物支給', 0],
    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 220 * mm, 55 * mm)

    # (6)4列目 4段目
    data = [
        ['                 振込支給額', ' '],
        [' ', ' '],
        [' ', ' '],
        [' ', ' '],
        ['合計', ' '],
    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('SPAN', (0, 0), (1, 0)),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 220 * mm, 16 * mm)

    # (6)4列目  2段目
    data = [
        [' ', ' '],
    ]
    table = Table(data, colWidths=(30 * mm, 30 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 220 * mm, 75 * mm)

    # 備考
    data = [
        ['備考', one_person['コメント欄']],
    ]
    table = Table(data, colWidths=(20 * mm, 250 * mm), rowHeights=6 * mm)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'HeiseiKakuGo-W5', 11),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    table.wrapOn(pdf_canvas, 20 * mm, 20 * mm)
    table.drawOn(pdf_canvas, 10 * mm, 6 * mm)

    ###########################
    pdf_canvas.showPage()


def delete_commma(commma_str):
    if commma_str is '':
        return int(0)
    return int(commma_str.replace(',', ''))


def add_commma(non_commma_str):
    return "{:,}".format(non_commma_str)


def check_blank(chk_str):
    # 空であれば０を返すメソッド

    if chk_str is '':
        return 0
    return chk_str


def make_datas(datas:list, pay_list):
    print(pay_list)
    if pay_list[1] is None or not pay_list[1] in '':
            datas.append(pay_list)
    return datas

def check_list_pay(datas):
    temp_list = ["", ""]
    for i in range(len(datas),23):
        datas.append(temp_list)
    return datas


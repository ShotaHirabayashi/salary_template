# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors



# 初期設定
def make(filename="resume"):  # ファイル名
    pdf_canvas = set_info(filename)  # キャンバス名
    print_string(pdf_canvas)
    pdf_canvas.save()  # 保存


def set_info(filename):
    pdf_canvas = canvas.Canvas("hello.pdf", pagesize=landscape(A4))  # 保存先
    pdf_canvas.setAuthor("W-GROUP")  # 作者
    pdf_canvas.setTitle("給与明細")  # 表題
    pdf_canvas.setSubject("W-GROUP 給与明細")  # 件名
    return pdf_canvas


# 履歴書フォーマット作成
def print_string(pdf_canvas):
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))  # フォント
    width, height = A4  # 用紙サイズ
    #年月日分
    font_size = 20  # フォントサイズ
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(15*mm, 187*mm, '令和2年  8月分 給与')  # 書き出し(横位置, 縦位置, 文字)

    #明細書
    font_size = 28  # フォントサイズ
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(120*mm, 185*mm, '明細書')  # 書き出し(横位置, 縦位置, 文字)

    #作成日
    font_size = 15
    pdf_canvas.setFont('HeiseiKakuGo-W5', font_size)
    pdf_canvas.drawString(200*mm, 190*mm, '支給日         年         月         日')

    #氏名
    #氏名と様の隙間は半角40
    font_size = 15
    pdf_canvas.setFont('HeiseiKakuGo-W5', 15)
    pdf_canvas.drawString(20*mm, 172*mm, '氏名                                        様')

    pdf_canvas.setLineWidth(1)
    # .line(始点x,始点y,終点x,終点y)
    pdf_canvas.line(20 * mm, 170 * mm, 280, 482)


    #氏名
    #氏名と様の隙間は半角40
    font_size = 15
    pdf_canvas.setFont('HeiseiKakuGo-W5', 15)
    pdf_canvas.drawString(220*mm, 165*mm, 'GROUP HOALINGS')



    # (6)1列目
    # 上段の空白は22
    data = [
        ['                      勤怠', ''],
        ['出勤日数', ' '],
        ['休日出勤', ' '],
        ['有給休暇', ' '],
        ['勤務時間', ' '],
        ['深夜残業', ' '],
        ['休日出勤', ' '],
        ['休日深夜', ' '],
        ['欠勤日数', ' '],
        ['遅刻早退', ' '],
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



    # (6)2列名
    data = [
        ['                      支給   ', ''],
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
    table.drawOn(pdf_canvas, 80 * mm, 16 * mm)

    # ##########

    # (6)３列目
    data = [
        ['                      控除   ', ''],
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
        [' ', ' '],
        [' ', ' '],
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
    table.drawOn(pdf_canvas, 220 * mm, 88 * mm)


    # (6)4列目 2段目
    data = [
        ['現金支給', ' '],
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
        ['現物支給', ' '],
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
        ['備考', ' '],
    ]
    table = Table(data, colWidths=(20*mm, 250 * mm), rowHeights=6 * mm)
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


# 作成
if __name__ == '__main__':
    make()

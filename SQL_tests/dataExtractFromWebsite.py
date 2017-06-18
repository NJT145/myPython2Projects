#-*- coding: utf-8 -*-

"""
sources:

https://stackoverflow.com/questions/11790535/extracting-data-from-html-table
https://stackoverflow.com/questions/10556048/how-to-extract-tables-from-websites-in-python

http://www.python-excel.org/
https://stackoverflow.com/questions/16560289/using-python-write-an-excel-file-with-columns-copied-from-another-excel-file
https://stackoverflow.com/questions/19189048/writing-creating-a-worksheet-using-xlrd-and-xlwt-in-python

"""

import sys
import os
import requests
import pandas as pd
import xlrd
import xlwt
import pickle
import urllib
from bs4 import BeautifulSoup


def webDataToDict_table1(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")
    webData_list = []
    for table in tables:
        last_title = None
        lines = table.find_all("tr")
        for line in lines:
            line_info = []
            if line.find("td", attrs={"colspan":"2"}) != None:
                last_title = line.find("td", attrs={"colspan":"2"}).text.strip()
            else:
                name = line.find("td", attrs={"class":"tdd"}).text.strip().split("\n")[0]
                name = name.encode('utf-8').decode(sys.stdout.encoding)
                info = line.find("td", attrs={"class":"tdd"}).text.strip().split("\n")[1]
                adress = info.split('ADRES :')[1].split('TELEFON :')[0]
                adress = adress.encode('utf-8').decode(sys.stdout.encoding)
                tel = info.split('ADRES :')[1].split('TELEFON :')[1].split('Fax: ')[0]
                tel = tel.encode('utf-8').decode(sys.stdout.encoding)
                fax = info.split('ADRES :')[1].split('TELEFON :')[1].split('Fax: ')[1]
                fax = fax.encode('utf-8').decode(sys.stdout.encoding)
                coordinate_old = str(line.find("td", attrs={"class":"noBackground"}).find("span"))
                coordinate_old = coordinate_old.split('onclick="goster')[1].split('" style=')[0]
                coordinate = ''.join(c for c in coordinate_old.split(",")[0] if c.isdigit())
                coordinate = coordinate + "." + ''.join(c for c in coordinate_old.split(",")[1] if c.isdigit())
                coordinate = coordinate + ", " + ''.join(c for c in coordinate_old.split(",")[2] if c.isdigit())
                coordinate = coordinate + "." + ''.join(c for c in coordinate_old.split(",")[3] if c.isdigit())
                coordinate = coordinate.encode('utf-8').decode(sys.stdout.encoding)
                title = last_title.encode('utf-8').decode(sys.stdout.encoding)
                line_info.append(title)
                line_info.append(name)
                line_info.append(adress)
                line_info.append(tel)
                line_info.append(fax)
                line_info.append(coordinate)
                webData_list.append(line_info)
    return webData_list


def webDataToDict_table2(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")
    webData_list = []
    for table in tables:
        last_title = None
        lines = table.find_all("tr")
        for line in lines:
            line_info = []
            if line.find("th") != None:
                for data_title_html in line.find_all("th"):
                    data_title = (data_title_html.text).encode('utf-8').decode(sys.stdout.encoding)
                    line_info.append(data_title)
            else:
                columns = line.find_all("td")
                name = columns[0].text.split("\n")[1].strip()
                name = name.encode('utf-8').decode(sys.stdout.encoding)
                line_info.append(name)
                adress = columns[1].text.strip()
                adress = adress.encode('utf-8').decode(sys.stdout.encoding)
                line_info.append(adress)
                working_hours_info = ""
                open_in_saturday = u"Hayır"
                if columns[0].find("span") != None:
                    if columns[0].find("span").has_attr("class"):
                        working_hours_info = columns[0].find("span").text.strip()
                    else:
                        open_in_saturday = u"Evet"
                working_hours_info = working_hours_info.encode('utf-8').decode(sys.stdout.encoding)
                open_in_saturday = open_in_saturday.encode('utf-8').decode(sys.stdout.encoding)
                line_info.append(working_hours_info)
                line_info.append(open_in_saturday)
                coordinate_old = str(columns[2].find("span"))
                coordinate_old = coordinate_old.split('onclick="goster')[1].split('" style=')[0]
                coordinate = ''.join([c for c in coordinate_old.split(",")[0] if c.isdigit()])
                coordinate = coordinate + "." + ''.join([c for c in coordinate_old.split(",")[1] if c.isdigit()])
                coordinate = coordinate + ", " + ''.join(c for c in coordinate_old.split(",")[2] if c.isdigit())
                coordinate = coordinate + "." + ''.join(c for c in coordinate_old.split(",")[3] if c.isdigit())
                coordinate = coordinate.encode('utf-8').decode(sys.stdout.encoding)
                line_info.append(coordinate)
            webData_list.append(line_info)
    return webData_list



def write_xls(table_2Dlist, path, sheet_name, data_line=None, start_from_row1=False):
    """
    write a 2D list as wb_2Dlist[i]=[data_list_for_line] to a xls Excel file.
    """
    workbook = xlwt.Workbook(encoding=sys.stdout.encoding)
    sheet = workbook.add_sheet(sheet_name)
    if data_line != None:
        for index, value in enumerate(data_line):
            sheet.write(0, index, value)
        if start_from_row1 == False:
            for row in range(len(table_2Dlist)):
                for col in range(len(table_2Dlist[row])):
                    sheet.write(row+1, col, table_2Dlist[row][col])
        else:
            for row in range(len(table_2Dlist)):
                if row == 0:
                    pass
                else:
                    for col in range(len(table_2Dlist[row])):
                        sheet.write(row+1, col, table_2Dlist[row][col])
    else:
        for row in range(len(table_2Dlist)):
            for col in range(len(table_2Dlist[row])):
                sheet.write(row, col, table_2Dlist[row][col])
    workbook.save(path)

#url1 = "http://www.igdas.istanbul/AdresVeTelefonlar?id=233&lang=tr&sc=4"
#data_line1 = ["Bina Türü", "Başlık", "Adres", "Telefon", "Faks", "Koordinatlar (x, y)"]
#list1 = webDataToDict_table1(url1)
#write_xls(list1, u"İGDAŞ_Adresler_ve_Telefonlar.xls", u"Adresler_ve_Telefonlar", data_line=data_line1)


url2 = "http://www.igdas.istanbul/IgdasSubeleri?id=236&lang=tr&sc=4"
data_line2 = ["Başlık", "Adres", "Çalışma Saatleri", "Cumartesi Açık mı?", "Koordinatlar (x, y)"]
list2 = webDataToDict_table2(url2)
write_xls(list2, u"İGDAŞ_İgdaş_Şubeleri.xls", u"İgdaş_Şubeleri", data_line=data_line2, start_from_row1=True)


def webDataToCsv1(url, csv_name):
    df = webDataToDF1(url)
    df.to_csv(csv_name)
    return df


def test_webDataToCsv1():
    url1 = 'http://www.ffiec.gov/census/report.aspx?year=2011&state=01&report=demographic&msa=11500'
    csv_name1 = 'my data.csv'
    df1 = webDataToCsv1(url1, csv_name1)
    print df1


def webDataToDF1(url):
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    return df


def dfToCsv(df, csv_name):
    pass



def test_webDataToDF1():
    url2 = 'http://www.igdas.istanbul/AdresVeTelefonlar?id=233&lang=tr&sc=4'
    csv_name2 = 'AdresVeTelefonlar.csv'
    df = webDataToDF1(url2)
    df.drop(1, axis=1, inplace=True)
    keys = []
    table_dict = {}
    last_key = None
    for line in df[0]:
        if len(line) < 40:
            last_key = line
            table_dict[line] = []
            keys.append(line)
        else:
            table_dict[last_key].append(line)

    resultTable_dict = {u"Bina Türü":{}, u"Başlık":{}, u"Adres":{}, u"Telefon":{}, u"Faks":{}}
    lastIndex = 0
    for key in keys:
        for index in range(len(table_dict[key])):
            row = lastIndex + index
            if index == (len(table_dict[key]) - 1):
                lastIndex = row


    for key in keys:
        print "##Bina Türü## ", key
        for lineIndex in range(len(table_dict[key])):
            print "##Başlık## ", table_dict[key][lineIndex].split("ADRES :")[0], "##Adres## ", table_dict[key][lineIndex].split("ADRES :")[1].split("TELEFON :")[0], "##TEL##", table_dict[key][lineIndex].split("ADRES :")[1].split("TELEFON :")[1].split("Fax: ")[0], "##Fax##", table_dict[key][lineIndex].split("ADRES :")[1].split("TELEFON :")[1].split("Fax: ")[1]


#test_webDataToDF1()

import pandas as pd
import numpy as np
import re

# HoTen_MSSV	ThoiGian	NoiDung		TuongTac	Nhom

data = {
	"SauDaiHoc": None,
	"ThiTracNghiem": None,
	"CoSoVatChat": None,
	"HustEnglish": None,
	"BeBoiBK": None,
	"ThiTiengAnhOnline": None,
	"PhongDaoTao": None,
	"CTSV": None,
	"DiemRenLuyen": None,
	"AllCompany": None
}

def deEmojify(text):            # loại bỏ emoji
	regex_pattern = re.compile(pattern = "["
		u"\U0001F600-\U0001F64F"
		u"\U0001F300-\U0001F5FF"
		u"\U0001F680-\U0001F6FF"
		u"\U0001F1E0-\U0001F1FF"
								"]+", flags= re.UNICODE)
	return regex_pattern.sub(r"", text)

def text_cleaner(text):         # loại bỏ dấu câu và khoảng trắng lớn
    filters = '!"#$%()*+,-./:;=?@[]^_`{|}~'    

    newString = text.lower()
    for i in filters:
        newString = newString.replace("{}".format(i), " ")
    newString = re.sub(r"'s\b", "", newString)
    newString = re.sub('\s{2,}', " ", newString)
    return newString

def clear_data(text):           # kết hợp lại và kiểm tra kí tự đầu có phải là " "
    result = deEmojify( text_cleaner(text) )
    if result[0] == " ":
        result = result[1:]
    return result


with pd.ExcelFile("crawldata.xlsx") as reader:
	for key in data:
		# bỏ dòng cuối do chỉ chứa giá trị null
		data[key] = pd.read_excel(reader, sheet_name=key)[0: -1]

		data[key]["HoTen_MSSV"] = [
            clear_data(str(name)) for name in data[key]["HoTen_MSSV"]
        ]

		data[key]["NoiDung"] = [
            clear_data(str(content)) for content in data[key]["NoiDung"]
        ]
		
# print( data["HustEnglish"]["NoiDung"] )
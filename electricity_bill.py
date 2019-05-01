import os, sys
import win32print
import win32con
import configparser
import codecs
import datetime
from dateutil.relativedelta import relativedelta

def print_file(filename):
	printer_name = "Canon LBP6030/6040/6018L"
	win32print.SetDefaultPrinter(printer_name)
	os.startfile(filename, "print")

def print_file3(str1):
	import win32ui
	import win32print
	import win32con
	#str1 = str1 + str1 + str1 + str1  # test height of text area
	hDC = win32ui.CreateDC()

	printer_name = "Canon LBP6030/6040/6018L"
	win32print.SetDefaultPrinter(printer_name)

	hDC.CreatePrinterDC(win32print.GetDefaultPrinter())
	hDC.StartDoc("Test doc")
	hDC.StartPage()
	hDC.SetMapMode(win32con.MM_TWIPS)
	# draws text within a box (assume about 1400 dots per inch for typical HP printer)
	ulc_x = 1000    # give a left margin
	ulc_y = -1000   # give a top margin
	lrc_x = 11500   # width of text area-margin, close to right edge of page
	lrc_y = -15000  # height of text area-margin, close to bottom of the page
	hDC.DrawText(str1, (ulc_x, ulc_y, lrc_x, lrc_y), win32con.DT_LEFT)
	hDC.EndPage()
	hDC.EndDoc()
def print_file2(filename):
	lines = read_file(filename)

	printer_name = "Canon LBP6030/6040/6018L"
	win32print.SetDefaultPrinter(printer_name)
	import win32ui
	# X from the left margin, Y from top margin
	# both in pixels
	X=50; Y=50
	
	hDC = win32ui.CreateDC ()
	hDC.CreatePrinterDC (printer_name)
	hDC.StartDoc ("Electricity Bill Print")
	hDC.StartPage ()
	for line in lines:
		print(line)
		hDC.TextOut(X,Y,line)
		Y += 100
		
	hDC.EndPage ()
	hDC.EndDoc ()

def read_config_ini(filename):
    config = configparser.ConfigParser()
    config.readfp(codecs.open(filename, "r", "utf8"))
    return config

def read_file(filename):
	with codecs.open(filename, "r", encoding="utf-8") as file_reader:
		lines = file_reader.readlines()

	ill_chars = ['\r','\n']
	_ = []
	for line in lines:
		for ic in ill_chars:
			line = line.replace(ic,'')
		_.append(line)
	filtered_lines = _
	return filtered_lines


def write_file(filename, strs,mode="w"):
	import codecs
	with codecs.open(filename, mode, encoding='utf-8') as file_appender:
		file_appender.writelines(strs)

def comma_seperator_number(number):
	number = float(number)
	number = str(number)

	split = number.split('.')
	split_1 = split[0]
	split_2 = split[1]

	rev_split1 = split_1[::-1]
	rev_comma = rev_split1[:3] 
	 
	if rev_split1[3:5] != '':
		rev_comma = rev_comma + "," + rev_split1[3:5]
	if rev_split1[5:7] != '':
		rev_comma = rev_comma + "," + rev_split1[5:7]
	if rev_split1[7:] != '':
		rev_comma = rev_comma + "," + rev_split1[7:]
	#comma_after = [3,5,7]
	return rev_comma[::-1]+"."+split_2

#print(comma_seperator_number(1561.96))


today = datetime.date.today()

last_date_of_prev_month = datetime.date(today.year, today.month, 1) - relativedelta(days=1)
date_ = last_date_of_prev_month.strftime('%d %b,%Y')

config = read_config_ini("config.ini")

present_electricity_reading = float(config['READING']['present_electricity_unit'])#7900#float(input("present reading:"))
past_electricity_reading = float(config['READING']['past_electricity_unit'])#float(input("past reading:"))

vat_percentage_stri = config['READING']['vat'] #%
vat_percentage_stri = int(vat_percentage_stri.split("percent")[0].replace(' ',''))

#fixed costs
service_charge = float(config['FIXED']['service_charge'])
demand_charge = float(config['FIXED']['demand_charge'])
gas_bill = float(config['FIXED']['gas_bill'])
#fixed costs

#calculation
electricity_reading = present_electricity_reading - past_electricity_reading

#check for split 3
split_1_range = 75
split_1_reading = 75
split_1_rate = 4
split_2_rate = 5.45

if electricity_reading > split_1_range:
	split_2_reading = electricity_reading - split_1_reading
else:
	split_2_reading = 0

split_1 = split_1_reading*split_1_rate
split_2 = split_2_reading*split_2_rate
total_electricity_bill = split_1 + split_2

vat_percentage = vat_percentage_stri/100
vat = total_electricity_bill*vat_percentage

total_payable = total_electricity_bill + vat + service_charge + demand_charge + gas_bill



electricity_string=f"""Date: {date_}
Flat: Shaon [Ground Floor]

{'Present Reading':<23} = {present_electricity_reading:7.2f} Unit
{'Past Reading':<23} = {past_electricity_reading:7.2f} Unit
_______________________________________
Total Electricity Usage = {electricity_reading:7.2f} Unit

Split 1 - {split_1_reading:5.2f} x {split_1_rate:5.2f} = {split_1:6,.2f} BDT
Split 2 - {split_2_reading:5.2f} x {split_2_rate:5.2f} = {split_2:6,.2f} BDT
_____________________________________
{'Total Electricity Bill':<22} = {total_electricity_bill:7,.2f} BDT
{vat_percentage_stri}{'% Vat':<21} = {vat:7.2f} BDT
{'Service Charge':<22} = {service_charge:7.2f} BDT
{'Demand Charge':<22} = {demand_charge:7.2f} BDT
{'Gas Bill':<22} = {gas_bill:7,.2f} BDT
_____________________________________
{'Total Payable':<22} = {total_payable:7,.2f} BDT
"""

#windows string newline
#electricity_string = electricity_string.replace('\n','\r\n')
filename = date_+".txt"

write_file(filename, electricity_string,mode="w")
print_file2(filename)

present_electricity_reading = 8037#7900#float(input("present reading:"))
past_electricity_reading = 7897#float(input("past reading:"))

vat_percentage_stri = 5 #%

#fixed costs
service_charge = 60
demand_charge = 15
gas_bill = 800
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


electricity_string=f"""
Present Reading - {present_electricity_reading}
Past Reading    - {past_electricity_reading}
_________________________
Total Usage     - {electricity_reading}

Split 1 - {split_1_reading}x{split_1_rate} = {split_1}
Split 2 - {split_2_reading}x{split_2_rate} = {split_2}
_________________________
Total Bill     -  {total_electricity_bill}
{vat_percentage_stri}% Vat         -   {vat}
Service Charge -   {service_charge}
Demand Charge  -   {demand_charge}
Gass Bill      -  {gas_bill}
_________________________
Total Payable  - {total_payable}
"""
print(electricity_string)
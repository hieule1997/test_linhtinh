import xlrd

workbook = xlrd.open_workbook('/home/hieu/Desktop/cautrucde/Data/READING/noicau.xlsx')
worksheet = workbook.sheet_by_index(0)
num_rows = worksheet.nrows
num_cols = worksheet.ncols
# for r in range(num_rows-1):
# 	for c in range (num_cols):
# 		if worksheet.cell_value(r+1,c) == '':
# 			continue
# 			# print("rong")

# 		else:
# 			print(worksheet.cell_value(r+1,c))

# 	print("\n")
for r in range(0,num_cols-2,2):
    for i in range(num_rows - 1):
        print(str(r) + worksheet.cell_value(i+1,r))  
        print(str(r+1) + worksheet.cell_value(i+1,r+1))
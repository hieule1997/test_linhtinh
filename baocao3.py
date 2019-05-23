import xlwt 
from xlwt import Workbook 
  
# Workbook is created 
wb = Workbook() 
  
# add_sheet is used to create sheet. 
sheet1 = wb.add_sheet('Sheet 1') 

font = xlwt.Font()  # ???????
font.name = 'Times New Roman'
font.bold = True
font.color_index = 0
style = xlwt.XFStyle()
style.font = font
alignment = xlwt.Alignment()
alignment.horz = xlwt.Alignment.HORZ_CENTER
alignment.vert = xlwt.Alignment.VERT_CENTER
alignment.wrap = 1
style.alignment = alignment
sheet1.write_merge(r1 = 4,c1 = 1,r2 =  4,c2= 12, label ="BÁO CÁO TỔNG HỢP TÀI SẢN ĐẶC BIỆT",style = style)
sheet1.write_merge(r1 = 6,c1 = 1,r2 =  8, c2= 1, label = 'Tài sản',style = style)
sheet1.write_merge(r1 = 6,c1 = 2,r2 =  8, c2= 2, label = 'Mã số',style = style)
sheet1.write_merge(r1 = 6,c1 = 3,r2 =  8, c2= 3, label = 'Số lượng TS',style = style)
sheet1.write_merge(r1 = 6,c1 = 4,r2 =  8, c2= 4, label = 'Khối lượng TS',style = style) 
sheet1.write_merge(r1 = 6,c1 = 5,r2 =  7, c2= 9, label = 'Nguyên giá',style = style) 
sheet1.write_merge(r1 = 8,c1 = 5,r2 =  8, c2= 5, label = 'Bộ cấp',style = style) 
sheet1.write_merge(r1 = 8,c1 = 6,r2 =  8, c2= 6, label = 'Địa phương',style = style) 
sheet1.write_merge(r1 = 8,c1 = 7,r2 =  8, c2= 7, label = 'Dự án',style = style)
sheet1.write_merge(r1 = 8,c1 = 8,r2 =  8, c2= 8, label = 'Nguồn khác',style = style)
sheet1.write_merge(r1 = 8,c1 = 9,r2 =  8, c2= 9,label = 'Tổng cộng',style = style)
sheet1.write_merge(r1 = 6,c1 = 10,r2 =  8, c2= 10,label = 'Hao mòn lũy kế',style = style)
sheet1.write_merge(r1 = 6,c1 = 11,r2 =  8, c2= 11, label = 'Giá trị còn lại',style = style) 
j = 0
for x in range(9,11,1):
	for i in range(1,12,1):
		sheet1.write(x,i,"x"+"i")
	j = x

sheet1.write_merge(r1 = j+1,c1 = 1,r2 =  j+1, c2= 2, label = 'Tổng cộng',style = style) 

wb.save('example3.xlsx') 
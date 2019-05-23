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
sheet1.write_merge(r1 = 4,c1 = 1,r2 =  4,c2= 9, label="BIÊN BẢN ĐÁNH GÍA LẠI TÀI SẢN PHỤC VỤ CÔNG TÁC QUẢN LÝ",style = style)
sheet1.write_merge(r1 = 6,c1 = 1,r2 =  8, c2= 1, label = 'STT',style = style)
sheet1.write_merge(r1 = 6,c1 = 2,r2 =  8, c2= 2, label = 'Tên tài sản',style = style)
sheet1.write_merge(r1 = 6,c1 = 3,r2 =  8, c2= 3, label = 'Số thẻ', style = style)
sheet1.write_merge(r1 = 6,c1 = 4,r2 =  6, c2= 6, label = 'Giá trị đang ghi sổ',style = style)
sheet1.write_merge(r1 = 7,c1 = 4,r2 =  8, c2= 4, label = 'Nguyên giá',style = style) 
sheet1.write_merge(r1 = 7,c1 = 5,r2 =  8, c2= 5, label = 'Giá trị hao mòn',style = style) 
sheet1.write_merge(r1 = 7,c1 = 6,r2 =  8, c2= 6, label = 'Giá trị còn lại',style = style) 
sheet1.write_merge(r1 = 6,c1 =7,r2 =  8, c2= 7,label = 'Giá theo đánh giá lại',style = style)
sheet1.write_merge(r1 = 6,c1 = 8,r2 =  7, c2= 9,label = 'Chênh lệnh giữa đánh giá và giá trị còn lại',style = style)
sheet1.write_merge(r1 = 8,c1 = 8,r2 =  8, c2= 8, label = 'Tăng',style = style) 
sheet1.write_merge(r1 = 8,c1 = 9,r2 =  8, c2= 9, label = 'Giảm',style = style)

for x in range(1,10,1):
	for i in range(9,11,1):
		sheet1.write(i,x,"x"+"i")
wb.save('example1.xlsx') 
import xlwt 
from xlwt import Workbook 
  

wb = Workbook() 
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
sheet1.write_merge(r1 = 4,c1 = 1,r2 =  4,c2= 12, label ="BIÊN BẢN KIỂM KÊ TÀI SẢN CHUYÊN DÙNG",style = style)
sheet1.write_merge(r1 = 6,c1 = 1,r2 =  8, c2= 1, label = 'STT',style = style)
sheet1.write_merge(r1 = 6,c1 = 2,r2 =  8, c2= 2, label = 'Mã số',style = style)
sheet1.write_merge(r1 = 6,c1 = 3,r2 =  8, c2= 3, label = 'Năm sử dụng',style = style)
sheet1.write_merge(r1 = 6,c1 = 4,r2 =  8, c2= 4, label = 'Nơi sử dụng',style = style) 
sheet1.write_merge(r1 = 6,c1 = 5,r2 =  6, c2= 7, label = 'Theo sổ kế toán',style = style) 
sheet1.write_merge(r1 = 7,c1 = 5,r2 =  8, c2= 5, label = 'Số lượng',style = style) 
sheet1.write_merge(r1 = 7,c1 = 6,r2 =  8, c2= 6, label = 'Nguyên giá',style = style) 
sheet1.write_merge(r1 = 7,c1 = 7,r2 =  8, c2= 7, label = 'Giá trị còn lại',style = style)
sheet1.write_merge(r1 = 6,c1 = 8,r2 =  6, c2= 11, label = 'Theo kiểm kê',style = style)
sheet1.write_merge(r1 = 7,c1 = 8,r2 =  8, c2= 8,label = 'Số lượng',style = style)
sheet1.write_merge(r1 = 7,c1 = 9,r2 =  8, c2= 9,label = 'Nguyên giá',style = style)
sheet1.write_merge(r1 = 7,c1 = 10,r2 =  8, c2= 10,label = 'Giá trị còn lại',style = style)
sheet1.write_merge(r1 = 7,c1 = 11,r2 =  8, c2= 11,label = 'TL còn lại (%)',style = style)
sheet1.write_merge(r1 = 6,c1 = 12,r2 =  6, c2= 14,label = 'Chênh lệch',style = style)
sheet1.write_merge(r1 = 7,c1 = 12,r2 =  8, c2= 12,label = 'Số lượng',style = style)
sheet1.write_merge(r1 = 7,c1 = 13,r2 =  8, c2= 13,label = 'Nguyên giá',style = style)
sheet1.write_merge(r1 = 7,c1 = 14,r2 =  8, c2= 14,label = 'Giá trị còn lại',style = style)
sheet1.write_merge(r1 = 6,c1 = 15,r2 =  8, c2= 15, label = 'Ghi chú',style = style) 
j = 0
for x in range(9,11,1):
	for i in range(1,16,1):
		sheet1.write(x,i,"x"+"i")
	j = x

sheet1.write_merge(r1 = j+1,c1 = 1,r2 =  j+1, c2= 2, label = 'Cộng',style = style) 

wb.save('example4.xlsx') 
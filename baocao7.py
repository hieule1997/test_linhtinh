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
sheet1.write_merge(r1 = 4,c1 = 1,r2 =  4,c2= 12, label ="SỔ TÀI SẢN CỐ ĐỊNH",style = style)
sheet1.write_merge(r1 = 6,c1 = 1,r2 =  6, c2= 7, label = 'Ghi tăng tài sản cố định',style = style)
sheet1.write_merge(r1 = 7,c1 = 1,r2 =  7, c2= 2, label = 'Chứng từ',style = style)
sheet1.write_merge(r1 = 8,c1 = 1,r2 =  9, c2= 1, label = 'Số hiệu',style = style)
sheet1.write_merge(r1 = 8,c1 = 2,r2 =  9, c2= 2, label = 'Ngày tháng',style = style) 
sheet1.write_merge(r1 = 7,c1 = 3,r2 =  9, c2= 3, label = 'Tên,đặc điểm TSCĐ',style = style) 
sheet1.write_merge(r1 = 7,c1 = 4,r2 =  9, c2= 4 ,label = 'Nước sản xuất',style = style) 
sheet1.write_merge(r1 = 7,c1 = 5,r2 =  9, c2= 5, label = 'Năm sử dụng',style = style) 
sheet1.write_merge(r1 = 7,c1 = 6,r2 =  9, c2= 6, label = 'Số hiệu TSCĐ',style = style)
sheet1.write_merge(r1 = 7,c1 = 7,r2 =  9, c2= 7, label = 'Hao mòn tài sản cố định',style = style)
sheet1.write_merge(r1 = 6,c1 = 8,r2 =  6, c2= 12, label = 'Nguyên giá TSCĐ',style = style)
sheet1.write_merge(r1 = 7,c1 = 8,r2 =  7, c2= 9,label = 'Hao mòn một năm',style = style)
sheet1.write_merge(r1 = 8,c1 = 8,r2 =  9, c2= 8,label = 'Tỷ lệ (%)',style = style)
sheet1.write_merge(r1 = 8,c1 = 9,r2 =  9, c2= 9,label = 'Số tiền',style = style)
sheet1.write_merge(r1 = 7,c1 = 10,r2 =  9, c2= 10,label = 'Số hao mòn các năm khác chuyển sang',style = style)
sheet1.write_merge(r1 = 7,c1 = 11,r2 =  9, c2= 11,label = 'Số hao mòn tròn năm',style = style)
sheet1.write_merge(r1 = 7,c1 = 12,r2 =  9, c2= 12,label = 'Lũy kế hao mòn đến khi chuyển sổ hoặc ghi giảm TSCĐ',style = style)
sheet1.write_merge(r1 = 6,c1 = 13,r2 =  6, c2= 16,label = 'Ghi giảm tài sản cố định',style = style)
sheet1.write_merge(r1 = 7,c1 = 13,r2 =  7, c2= 14,label = 'Chứng từ',style = style)
sheet1.write_merge(r1 = 8,c1 = 13,r2 =  9, c2= 13,label = 'Số hiệu',style = style)
sheet1.write_merge(r1 = 8,c1 = 14,r2 =  9, c2= 14,label = 'Ngày tháng',style = style)
sheet1.write_merge(r1 = 7,c1 = 15,r2 =  9, c2= 15,label = 'Lý do giảm',style = style)
sheet1.write_merge(r1 = 7,c1 = 16,r2 =  9, c2= 16,label = 'Giá trị còn',style = style)
j = 0
for x in range(10,12,1):
	for i in range(1,17,1):
		sheet1.write(x,i,"x"+"i")
	j = x

sheet1.write_merge(r1 = j+1,c1 = 4,r2 =  j+1, c2= 4, label = 'Cộng',style = style) 

wb.save('example7.xlsx') 
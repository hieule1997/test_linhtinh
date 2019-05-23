from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import datetime
import json
import urllib.request
from matplotlib import pyplot as plt
KEY_MAP = {0: "A", 1:"B", 2:"C", 3:"D"}


def qus(input_image=""):

	paper =cv2.imread(input_image)
	# paper = cv2.imread(input_image)
	warped = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY) # chuyeern doi mau
	# apply Otsu's thresholding method to binarize the warped
	# piece of paper
	# print(paper)
	height, width, channels = paper.shape
	# print(height)
	thresh = cv2.threshold(warped, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]   # chuyen mau ve dang den trang

	# find contours in thplt.show()e thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # Phat hien khung dap an
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	questionCnts = []

	# cnts = contours.sort_contours(cnts,
	# 	method="top-to-bottom")[0]
	cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * paper.shape[1] )
	#use cv2 to get target(MASV. MADE, CAUTRALOI)
	target = []
	
	for cnx in cnts:
		(x, y, w, h) = cv2.boundingRect(cnx)
		ar = h / float(w)
		color = (0, 255, 0)
		k = 0
		if h > height/3:
			cv2.drawContours(paper, [cnx], 0, color, 3)
			target.append(cnx)

	tar = target[0]

	color = (255, 255, 0)
	# cv2.drawContours(paper, [tar], -1, color, 3)
	peri4 = cv2.arcLength(tar, True) # chu vi hinh chu nhat tar
	approx4 = cv2.approxPolyDP(tar, 0.05 * peri4, True)
	(x, y, w4, h4) = cv2.boundingRect(tar)
	paper4 = four_point_transform(paper, approx4.reshape(4, 2))
	warped4 = cv2.cvtColor(paper4, cv2.COLOR_BGR2GRAY)
	thresh4 = cv2.threshold(warped4, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	
	output = {}
	# find contours in the thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts4 = cv2.findContours(thresh4.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts4 = cnts4[0] if imutils.is_cv2() else cnts4[1]
	tar5 = []
	for cnx1 in cnts4:
		(x,y,w,h) = cv2.boundingRect(cnx1)
		ar = h/float(w)
		color = (0,255,0)
		k = 0
		if h>height/5:
			cv2.drawContours(paper4,[cnx1],0,color,3)
			tar5.append(cnx1)
    	# (x, y, w, h) = cv2.boundingRect(cnx1)
    	# ar = h / float(w)
    	# color = (0, 255, 0)
    	# k = 0
    	# if h > height/5:
    	# 	cv2.drawContours(paper4, [cnx1], 0, color, 3)
    	# 	tar5.append(cnx1)

	tar1 = tar5[0]	
	print(tar1)
	peri5 = cv2.arcLength(tar1, True) # chu vi hinh chu nhat tar
	approx5 = cv2.approxPolyDP(tar1, 0.05 * peri5, True)
	(x, y, w4, h4) = cv2.boundingRect(tar5)
	paper5 = four_point_transform(paper4, approx5.reshape(4, 2))
	lt.imshow(paper5,'gray')
	plt.xticks([]), plt.yticks([])
	plt.show()

	questionCnts4 = []
	for cn in cnts4:
		(x, y, w, h) = cv2.boundingRect(cn)
		ar = w / float(h)
		print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
		if w >= 20 and h >= 20 and ar >= 0.8 and ar <= 1.2:
			cv2.drawContours(paper4, [cn], -1, color, 3)
			questionCnts4.append(cn)
	print(len(questionCnts4))		
	plt.imshow(paper4,'gray')
	plt.xticks([]), plt.yticks([])
	plt.show()

	questionCnts4 = contours.sort_contours(questionCnts4,method="top-to-bottom")[0]
		
	for (q, i) in enumerate(np.arange(0, len(questionCnts4), 4)):
		cnts = contours.sort_contours(questionCnts4[i:i + 4])[0]
		bubbled = None
		dict_count= {}
		list_count= []
		# loop over the sorted contours
		for (j, c) in enumerate(cnts):
			# construct a mask that reveals only the current
			# "bubble" for the question
			mask = np.zeros(thresh4.shape, dtype="uint8")
			cv2.drawContours(mask, [c], -1, 255, -1)

			mask = cv2.bitwise_and(thresh4, thresh4, mask=mask)
			total = cv2.countNonZero(mask)

			if (bubbled is None ):
				bubbled = (total, j)
			elif (bubbled[0] > 120 and total > 120):
				bubbled = (1,j)
			elif (total > bubbled[0]):
				bubbled = (total, j)
			dict_count[total] = j
			list_count.append(total)
		
		list_count.sort(reverse=True)
		print(list_count)
		if list_count[0] < list_count[1] * 1.25:
			result = {
				q+1 : None
			}
			output.update(result)

		else:
			color = (
				0, 255, 0)
			cv2.drawContours(paper4, [cnts4[k]], -1, color, 3)
			result = {
				q+1  : KEY_MAP[dict_count[list_count[0]]]
			}
			output.update(result)

	return json.dumps(output)

if __name__ == '__main__':
	print(qus("chat1.jpg"))

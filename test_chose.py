from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import datetime
import json
import urllib.request
# import matlab
from matplotlib import pyplot as plt
KEY_MAP = {0: "A", 1:"B", 2:"C", 3:"D"}
KEY_SO = {}

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image


def auto_mark(input_image=""):
	# load the image, convert it to grayscale, blur it
	# slightly, then find edges

	if input_image.startswith("http"):
		paper = url_to_image(input_image)
	else:
		paper =cv2.imread(input_image)
	# paper = cv2.imread(input_image)
	warped = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
	# apply Otsu's thresholding method to binarize the warped
	# piece of paper

	height, width, channels = paper.shape
	# print(height)
	thresh = cv2.threshold(warped, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	plt.imshow(thresh)
	plt.xticks([]), plt.yticks([])
	plt.show()
	# find contours in the thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	questionCnts = []

	# cnts = contours.sort_contours(cnts,
	# 	method="top-to-bottom")[0]
	cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * paper.shape[1] )

	#use cv2 to get target(MASV. MADE, CAUTRALOI)
	
	target = []
	# print(len(cnts))
	for cnx in cnts:
		(x, y, w, h) = cv2.boundingRect(cnx)
		ar = h / float(w)
		color = (0, 255, 0)
		k = 0
		if h > height/3:
			# print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
			cv2.drawContours(paper, [cnx], -1, color, 3)
			target.append(cnx)
	plt.imshow(paper,'gray')
	plt.xticks([]), plt.yticks([])
	plt.show()
	dict_count= {}
	list_count= []
	output = {}
	output1 = {}
	p = 0
	for tar in target:
		color = (255, 255, 0)
		# cv2.drawContours(paper, [tar], -1, color, 3)
		peri4 = cv2.arcLength(tar, True)
		approx4 = cv2.approxPolyDP(tar, 0.02 * peri4, True)
		# print (approx4)
		output = {}
		(x, y, w4, h4) = cv2.boundingRect(tar)
		# print(str(x) + " " +str(y) +" "+str(w4)+" "+str(h4))
		width_one = round(w4/ 8.5)
		paper4 = four_point_transform(paper, approx4.reshape(4, 2))

		warped4 = cv2.cvtColor(paper4, cv2.COLOR_BGR2GRAY)
		thresh4 = cv2.threshold(warped4, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		plt.imshow(thresh4,'gray')
		plt.xticks([]), plt.yticks([])
		plt.show()

		# find contours in the thresholded image, then initialize
		# the list of contours that correspond to questions
		cnts4 = cv2.findContours(thresh4.copy(), cv2.RETR_LIST,
			cv2.CHAIN_APPROX_SIMPLE)
		
		cnts4 = cnts4[0] if imutils.is_cv2() else cnts4[1]
		questionCnts4 = []
		tbwone = width_one//2
		for cn in cnts4:
			(x, y, w, h) = cv2.boundingRect(cn)
			ar = w / float(h)
			if w >= tbwone and h >= tbwone and ar >= 0.8 and ar <= 1.2 :
				color = (0, 0, 255)
				# print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
				cv2.drawContours(paper4, [cn], -1, color, 1)
				questionCnts4.append(cn)
		questionCnts4 = contours.sort_contours(questionCnts4,method="top-to-bottom")[0]
		plt.imshow(paper4,'gray')
		plt.xticks([]), plt.yticks([])
		plt.show()
		for (q, i) in enumerate(np.arange(0, len(questionCnts4), 4)):
			cnts = contours.sort_contours(questionCnts4[i:i + 4])[0]
			bubbled = None
			# questiondetail = []
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
			if list_count[0] < list_count[1] * 1.25:
				p = p + 1
				result = {
					p : 0
				}
				
				output.update(result)
			else:
				color = (0, 255, 0)
				cv2.drawContours(paper4, [cnts4[k]], -1, color, 3)
				p= p+1
				result = {
					p : KEY_MAP[dict_count[list_count[0]]]
				}
				output.update(result)

		output1.update(output)

	return json.dumps(output1)

def auto_mark1(input_image=""):
	# load the image, convert it to grayscale, blur it
	# slightly, then find edges

	if input_image.startswith("http"):
		paper = url_to_image(input_image)
	else:
		paper =cv2.imread(input_image)
	# paper = cv2.imread(input_image)
	warped = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
	# apply Otsu's thresholding method to binarize the warped
	# piece of paper

	height, width, channels = paper.shape
	# print(height)
	thresh = cv2.threshold(warped, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	# find contours in the thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	questionCnts = []

	# cnts = contours.sort_contours(cnts,
	# 	method="top-to-bottom")[0]
	cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * paper.shape[1] )

	#use cv2 to get target(MASV. MADE, CAUTRALOI)

	target = []
	# print(len(cnts))
	for cnx in cnts:
		(x, y, w, h) = cv2.boundingRect(cnx)
		ar = h / float(w)
		color = (0, 255, 0)
		k = 0
		if h > height/8:
			# print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
			cv2.drawContours(paper, [cnx], -1, color, 3)
			target.append(cnx)

	dict_count= {}
	
	output = {}
	# output1 = {}
	# p = 0
	# for tar in target:
	tar = target[2]
	color = (255, 255, 0)
	# cv2.drawContours(paper, [tar], -1, color, 3)
	peri4 = cv2.arcLength(tar, True)
	approx4 = cv2.approxPolyDP(tar, 0.02 * peri4, True)
	# print (approx4)
	output = {}
	(x, y, w4, h4) = cv2.boundingRect(tar)
	# print(str(x) + " " +str(y) +" "+str(w4)+" "+str(h4))
	width_one = round(w4/ 8.5)
	paper4 = four_point_transform(paper, approx4.reshape(4, 2))

	warped4 = cv2.cvtColor(paper4, cv2.COLOR_BGR2GRAY)
	thresh4 = cv2.threshold(warped4, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	plt.imshow(paper4,'gray')
	plt.xticks([]), plt.yticks([])
	plt.show()

	# find contours in the thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts4 = cv2.findContours(thresh4.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts4 = cnts4[0] if imutils.is_cv2() else cnts4[1]
	questionCnts4 = []
	tbwone = width_one//1 + 1
	# print(tbwone)
	for cn in cnts4:
		(x, y, w, h) = cv2.boundingRect(cn)
		ar = w / float(h)
		if w >= tbwone and h >= tbwone and ar >= 0.8 and ar <= 1.2 :
			color = (0, 0, 255)
			# print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
			cv2.drawContours(paper4, [cn], -1, color, 1)
			questionCnts4.append(cn)
	questionCnts4 = contours.sort_contours(questionCnts4,method="left-to-right")[0]
	for (q, i) in enumerate(np.arange(0, len(questionCnts4), 10)):
		cnts = contours.sort_contours(questionCnts4[i:i + 10])[0]
		bubbled = None
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
		# print(list_count)
		list_count.sort(reverse=True)

		if list_count[0] < list_count[1] * 1.25:
			# p = p + 1
			result = {
				q+1 : None
			}
			
			output.update(result)
		else:
			color = (0, 255, 0)
			cv2.drawContours(paper4, [cnts4[k]], -1, color, 3)
			# p= p+1
			result = {
				q+1 : dict_count[list_count[0]]
			}
			output.update(result)


	return json.dumps(output)

def auto_mark2(input_image=""):
	# load the image, convert it to grayscale, blur it
	# slightly, then find edges

	if input_image.startswith("http"):
		paper = url_to_image(input_image)
	else:
		paper =cv2.imread(input_image)
	# paper = cv2.imread(input_image)
	warped = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
	# apply Otsu's thresholding method to binarize the warped
	# piece of paper

	height, width, channels = paper.shape
	# print(height)
	thresh = cv2.threshold(warped, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	# find contours in the thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	questionCnts = []

	# cnts = contours.sort_contours(cnts,
	# 	method="top-to-bottom")[0]
	cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * paper.shape[1] )

	#use cv2 to get target(MASV. MADE, CAUTRALOI)

	target = []
	# print(len(cnts))
	for cnx in cnts:
		(x, y, w, h) = cv2.boundingRect(cnx)
		ar = h / float(w)
		color = (0, 255, 0)
		k = 0
		if h > height/8:
			# print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
			cv2.drawContours(paper, [cnx], -1, color, 3)
			target.append(cnx)

	dict_count= {}
	output = {}
	# output1 = {}
	# p = 0
	# for tar in target:
	tar = target[3]
	color = (255, 255, 0)
	# cv2.drawContours(paper, [tar], -1, color, 3)
	peri4 = cv2.arcLength(tar, True)
	approx4 = cv2.approxPolyDP(tar, 0.02 * peri4, True)
	# print (approx4)
	output = {}
	(x, y, w4, h4) = cv2.boundingRect(tar)
	# print(str(x) + " " +str(y) +" "+str(w4)+" "+str(h4))
	width_one = round(w4/ 8.5)
	paper4 = four_point_transform(paper, approx4.reshape(4, 2))

	warped4 = cv2.cvtColor(paper4, cv2.COLOR_BGR2GRAY)
	thresh4 = cv2.threshold(warped4, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	

	# find contours in the thresholded image, then initialize
	# the list of contours that correspond to questions
	cnts4 = cv2.findContours(thresh4.copy(), cv2.RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts4 = cnts4[0] if imutils.is_cv2() else cnts4[1]
	questionCnts4 = []
	tbwone = width_one * 2 - 2
	# print(tbwone)
	for cn in cnts4:
		(x, y, w, h) = cv2.boundingRect(cn)
		ar = w / float(h)
		if w >= tbwone and h >= tbwone and ar >= 0.8 and ar <= 1.2 :
			color = (0, 0, 255)
			print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
			cv2.drawContours(paper4, [cn], -1, color, 1)
			questionCnts4.append(cn)
	questionCnts4 = contours.sort_contours(questionCnts4,method="top-to-bottom")[0]
	#  
	plt.imshow(paper4,'gray')
	plt.xticks([]), plt.yticks([])
	plt.show()
	list_question= []
	for (q, i) in enumerate(np.arange(0, len(questionCnts4), 3)):
		cnts = contours.sort_contours(questionCnts4[i:i + 3])[0]
		bubbled = None
		list_count = []
		# loop over the sorted contours
		for (j, c) in enumerate(cnts):
			# construct a mask that reveals only the current
			# "bubble" for the question
			mask = np.zeros(thresh4.shape, dtype="uint8")
			cv2.drawContours(mask, [c], -1, 255, -1)

			mask = cv2.bitwise_and(thresh4, thresh4, mask=mask)
			print(mask.shape)
			total = cv2.countNonZero(mask)
			print(total)
			if (bubbled is None ):
				bubbled = (total, j)
			elif (bubbled[0] > 120 and total > 120):
				bubbled = (1,j)
			elif (total > bubbled[0]):
				bubbled = (total, j)
			
			list_count.append(total)
		list_question.append(list_count)
		# list_count.sort(reverse=True)
	print(list_question)
	list_1 = []
	list_2 = []
	list_3 = []
	q = 0
	j = 0
	for lis in list_question:
		i = 1
		for asr in lis:
			if i==1:
				list_1.append(asr)
				dict_count[asr] = j
				# print(dict_count)
			elif i==2:
				list_2.append(asr)
				dict_count[asr] = j
				# print(dict_count)
			elif i==3:
				list_3.append(asr)
				dict_count[asr] = j
				# print(dict_count)
			i += 1
		j += 1
	# print(dict_count)
	list_alls = []
	list_alls.append(list_1)	
	list_alls.append(list_2)	
	list_alls.append(list_3)
	for list_all in list_alls:
		list_all.sort(reverse=True)
		if list_all[0] < list_all[1] * 1.2:
			# p = p + 1
			result = {
				q+1 : None
			}
			output.update(result)

		else:
			color = (0, 255, 0)
			cv2.drawContours(paper4, [cnts4[k]], -1, color, 3)
			result = {
				q+1 : dict_count[list_all[0]]
			}
			output.update(result)
		q += 1
	
	made = ""
	made = str(output[1]) + str(output[2]) +str(output[3])


	return made

if __name__ == '__main__':
	# print(auto_mark2("SV4_loi_cau_1.jpg"))
	# print(auto_mark1("maudethi.jpg"))
	print(auto_mark("SV4_loi_cau_1.jpg"))

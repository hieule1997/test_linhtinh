from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import datetime
import json
import urllib.request
KEY_MAP = {0: 1, 1:2, 2:3, 3:4}


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
	try:
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
			if h > height/3:
				# print(str(x) + " " +str(y) +" "+str(w)+" "+str(h)+" "+str(ar))
				cv2.drawContours(paper, [cnx], -1, color, 3)
				target.append(cnx)

		tar = target[0]
		color = (255, 255, 0)
		# cv2.drawContours(paper, [tar], -1, color, 3)
		peri4 = cv2.arcLength(tar, True)
		approx4 = cv2.approxPolyDP(tar, 0.02 * peri4, True)
		# print (approx4)

		(x, y, w4, h4) = cv2.boundingRect(tar)
		width_one = round(w4/ 8.5)
		for x in range(0,3):
			for y in range(x,4):
				if approx4[x,0][0] > approx4[y,0][0]:
					sw = approx4[x,0][0]
					approx4[x,0][0] = approx4[y,0][0]
					approx4[y,0][0] = sw
					swy = approx4[x,0][1]
					approx4[x,0][1] = approx4[y,0][1]
					approx4[y,0][1] = swy
		
		if approx4[0,0][1] > approx4[1,0][1]:
			sw = approx4[0,0][0]
			approx4[0,0][0] = approx4[1,0][0]
			approx4[1,0][0] = sw
			swy = approx4[0,0][1]
			approx4[0,0][1] = approx4[1,0][1]
			approx4[1,0][1] = swy

		if approx4[2,0][1] > approx4[3,0][1]:
			sw = approx4[2,0][0]
			approx4[2,0][0] = approx4[3,0][0]
			approx4[3,0][0] = sw
			swy = approx4[2,0][1]
			approx4[2,0][1] = approx4[3,0][1]
			approx4[3,0][1] = swy

		approx4[0,0][0] = approx4[2,0][0] - width_one
		approx4[1,0][0] = approx4[3,0][0] - width_one
		approx4[0,0][1] = approx4[0,0][1] + round(h4/7)
		approx4[1,0][1] = approx4[1,0][1] + 10
		approx4[2,0][1] = approx4[2,0][1] + round(h4/7)
		approx4[3,0][1] = approx4[3,0][1] +10
		# print(approx4)
		paper4 = four_point_transform(paper, approx4.reshape(4, 2))

		warped4 = cv2.cvtColor(paper4, cv2.COLOR_BGR2GRAY)
		thresh4 = cv2.threshold(warped4, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

		output = {}

		# find contours in the thresholded image, then initialize
		# the list of contours that correspond to questions
		cnts4 = cv2.findContours(thresh4.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts4 = cnts4[0] if imutils.is_cv2() else cnts4[1]
		questionCnts4 = []
		for cn in cnts4:
			(x, y, w, h) = cv2.boundingRect(cn)
			ar = w / float(h)
			# if w >= 9 and h >= 9 and ar >= 0.85 and ar <= 1.15 and w < height/4:
			if w >= 9 and h >= 9 and h < h4/4 and w < width_one / 2:
				# color = (0, 0, 255)
				cv2.drawContours(paper4, [cn], -1, color, 3)
				questionCnts4.append(cn)

		questionCnts4 = contours.sort_contours(questionCnts4,method="top-to-bottom")[0]
		

		for (q, i) in enumerate(np.arange(0, len(questionCnts4), 4)):
			# sort the contours for the current question from
			# left to right, then initialize the index of the
			# bubbled answer

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
			# print(list_count)
			list_count.sort(reverse=True)
			if list_count[0] < list_count[1] * 1.25:
				result = {
					q+1 : None
				}
				output.update(result)
				sheet1.write(row_,q+5,str(None))

			else:
				color = (0, 255, 0)
				cv2.drawContours(paper4, [cnts4[k]], -1, color, 3)
				result = {
					q+1  : KEY_MAP[dict_count[list_count[0]]]
				}
				output.update(result)

		return json.dumps(output)
	except:
		print("Input Error! %s" %input_image)
		return None

# if __name__ == '__main__':
# 	print(Auto_Mark("image_test/1.jpg"))
# 	print(Auto_Mark("https://drive.google.com/uc?authuser=0&id=1T07yNBRQyhiWBJNZgPK7egHpqDF6ggzO&export=download"))

#opencv calibration

import numpy as np
import cv2
import glob
import os
import json

class Calibrator :

	configFilename = "config.json"
	config = {}

	#cached camera matrix
	mtx = 0
	dist = 0
	rvecs = 0
	tvecs = 0

	def __init__(self) :
		with open(self.configFilename) as jsonData :
			self.config = json.load(jsonData)

		self.InitCalibrationImages()

	def InitCalibrationImages(self) :
		# termination criteria
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

		# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
		objp = np.zeros((7*7,3), np.float32)
		objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

		# Arrays to store object points and image points from all the images.
		objpoints = [] # 3d point in real world space
		imgpoints = [] # 2d points in image plane.

		images = glob.glob(self.config["calibrationImagePath"] + "/*.png")

		print("Found {} images for processing.".format(len(images)))

		successCount = 0

		for fname in images:
			img = cv2.imread(fname)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			success, corners = cv2.findChessboardCorners(gray, (7,7), None)

			# If found, add object points, image points (after refining them)
			if success :
				successCount += 1

				objpoints.append(objp)
				corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
				imgpoints.append(corners2)


		print("Successfully found patterns for {} of {} images".format(successCount, len(images)))

		ret, self.mtx, self.dist, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None,None)
        
	def CalibrateData(self) :
		imageCount = len(glob.glob(self.config["datapath"] + "/*.tif"))
		processedCount = 0

		print("Calibrating {} TIFF images.".format(imageCount))

		for filename in os.listdir(self.config["datapath"]):
			if ".tif" in filename :
				distImage = cv2.imread(self.config["datapath"] + '/' + filename)
				h,w = distImage.shape[:2]
				newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),0,(w,h))

				# undistort
				undistortedImage = cv2.undistort(distImage, self.mtx, self.dist, None, newCameraMtx)

				#write out undistorted image
				outname = filename.replace('.', "_flattened.")
				cv2.imwrite(self.config["datapath"] + "/" + outname, undistortedImage)

				processedCount += 1

		print("Successfully calibrated {} of {} images".format(processedCount, imageCount))


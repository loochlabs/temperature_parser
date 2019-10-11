#opencv calibration

import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('../data/Lens_Calibration_Images_Formatted/*.png')

print("Found {} images for processing.".format(len(images)))

successCount = 0

for fname in images:
	img = cv2.imread(fname)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	success, corners = cv2.findChessboardCorners(gray, (7,7), None)

	# If found, add object points, image points (after refining them)
	if success :
		print("Success! Found grid lines in {}".format(fname))

		objpoints.append(objp)
		corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners2)

		# Draw and display the corners
		#img = cv2.drawChessboardCorners(img, (7,7), corners2, ret)
		#cv2.imshow('img',img)
		#cv2.imwrite(fname, img)
		#cv2.waitKey(5000)

		successCount += 1

print("Successfully found grids {} of {} images".format(successCount, len(images)))

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None,None)
        
#Undistort image
print("Beginning undistortion process.")

distImagePath = "../temp/test_csv/Ellesmere_IR_flight01_1000ft_000055.jpg"
distImage = cv2.imread(distImagePath)

h,w = distImage.shape[:2]
print("{} {}".format(h,w))

newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),0,(w,h))

#TODO Write out the new camera matrix to a txt file to reuse for future runs
#	There is no reason to run this every time once we have a correct calibration

# undistort
undistortedImage = cv2.undistort(distImage, mtx, dist, None, newCameraMtx)

# crop the image
#print(roi)
#x,y,w,h = roi
#undistortedImage = undistortedImage[y:y+h, x:x+w]

cv2.imwrite("holy_sheet_it_works.jpg", undistortedImage)

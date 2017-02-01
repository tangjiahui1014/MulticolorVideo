# 多色视频录制
# Author: Jiahui Tang

#import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2

#construct the argument parse and paese the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', required=True,
	help='path to output video file')
ap.add_argument('-p', '--picamera', type=int, default=-1,
	help='whether or not the Raspberry Pi camera should be used')
ap.add_argument('-f', '--fps', type=int, default=20,
	help='FPS of output video')
ap.add_argument('-c', '--codec', type=str, default='MJPG',
	help='codec of output video')
args = vars(ap.parse_args())

#initialize the video stream and allow the camera
#sensor to warmup
print('[INFO] warming up camera...')
vs = VideoStream(usePiCamera=args['picamera'] > 0).start()
time.sleep(2.0)

#initialize the FoueCC, video writer, dimensions of the frame, and
#zeros array
#fourcc = cv2.VideoWriter_fourcc(*args['codec'])
#fourcc = cv2.cv.CV_FOURCC(*args['codec'])
fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
writer = None
(h, w) = (None, None)
zeros = None

#loop over frames from the video stream
while True:

#grab the frame from the video stream and resize it to have a
	#maximum width of 300 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=300)

	#check if the writer is None
	if writer is None:
		#store the image dimensions, initialzie the video writer,
		#and construct the zeros array
		(h, w) = frame.shape[:2]
		writer = cv2.VideoWriter(args['output'], fourcc, args['fps'],
			(w * 2, h * 2), True)
		zeros = np.zeros((h, w), dtype='uint8')

	#break the image into its RGB components, then construct the 
	#RGB representation of each frame individually
	(R, G, B) = cv2.split(frame)
	R = cv2.merge([zeros, zeros, R])
	G = cv2.merge([zeros, G, zeros])
	B = cv2.merge([B, zeros, zeros])

	#
	#
	#
	#
	output = np.zeros((h * 2, w * 2, 3), dtype='uint8')
	output[0:h, 0:w] = frame
	output[0:h, w:w * 2] = R
	output[h:h * 2, w: w * 2] = G
	output[h:h * 2, 0: w] = B

	#write the output frame to file
	writer.write(output)

	#show the frames
	cv2.imshow('frame', frame)
	cv2.imshow('output', output)
	key = cv2.waitKey(1) & 0xFF

        #if the 'q'key was pressed, break from the loop
	if key == ord('q'):
		break

#do a bit of cleanup
print('[INFO] cleaning up...')
cv2.destroyAllWindows()
vs.stop()
writer.release()


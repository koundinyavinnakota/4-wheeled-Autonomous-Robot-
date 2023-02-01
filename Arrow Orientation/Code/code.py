
import numpy as np
import cv2
import copy
import time 
import matplotlib.pyplot as plt

#CONSTANTS
H_MAX=106
S_MAX=190
V_MAX=126

H_MIN=32
S_MIN=76
V_MIN=30
lower_green=np.array([H_MIN,S_MIN,V_MIN])
upper_green=np.array([H_MAX,S_MAX,V_MAX])


#90,160,150
#45,60,70

#32,76,30
#106,190,126
f=open('hw3data.txt','w')
def file_write(f,delta):
    f.write(f'{delta}\n')

def plot_data(y):
    y = y[1:]
    x=np.arange(0,len(y))
    print(y)
    plt.figure(1)
    plt.plot(x,y,label="Raw Data")
    plt.title("Object Tracking: Processing Time")
    plt.xlabel("Frame")
    plt.ylabel("Processing Time [ms]")
    plt.legend(loc=2)
    plt.grid()
    
    plt.figure(2)
    plt.hist(y,10)
    plt.title("Object Tracking: Processing Time")
    plt.ylabel("Frame")
    plt.xlabel("Processing Time [ms]")
    plt.show()


cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 7.0, (640,480))
y_data=[]
while(cap.isOpened()):
	ret, frame = cap.read()
	if ret==True:	

		tic=time.time()
		#frame=cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
		frame=cv2.rotate(frame, cv2.ROTATE_180)
		frame_hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)     
		mask=cv2.GaussianBlur(frame_hsv,(5,5),3)
		kernel = np.ones((7,7),np.uint8)
		#mask = cv2.inRange(frame, lower_green, upper_green)
		mask = cv2.inRange(mask, lower_green, upper_green)
		#mask = cv2.dilate(mask,kernel,iterations = 2)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
		#mask = cv2.inRange(frame_hsv, lower_green, upper_green)
		
		threshold=mask

		_,contours,_ = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)	
		#frame = cv2.drawContours(frame, contours, -1, (255,0,0), 3)
		contours=contours[0]
		area = cv2.contourArea(contours)
		if area>4000:
			
			epsilon = 0.01*cv2.arcLength(contours,True)
			approx = cv2.approxPolyDP(contours,epsilon,True)
		#print(approx)
		#print(approx[0][0])
			for pt in approx:
				cv2.circle(frame,(pt[0][0],pt[0][1]),3,(0,0,255),-1)
			x,y,w,h = cv2.boundingRect(contours)
			threshold = mask[y:y+h,x:x+w]

		
		height,width = np.shape(threshold)

		if height>width:
			histogram = np.sum(threshold,axis=1)
			maxval= max(histogram)
			maxrow= np.argmax(histogram)
			if maxrow > height/1.8:
				direction = "down"
			else:
				direction = "up"
		else:	
			histogram = np.sum(threshold,axis=0)
			maxval = max(histogram)
			maxrow= np.argmax(histogram)
			

	
			if maxrow > width/1.8:
				direction = "right"
			else:
				direction = "left"

		font=cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame,direction,(10,50),font,1,(255,0,0),3)
		#cv2.imshow('HSV IMAGE',frame_hsv)
		#cv2.waitKey(0)
		#cv2.imshow('MASK',mask)
		cv2.imshow('RGB FRAME',frame)
		out.write(frame)
		toc=time.time()
		delta=toc-tic
		#print(delta)
		y_data.append(delta)
		file_write(f,delta)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	else:
		break

# Release everything if job is finished
f.close()
cap.release()
cv2.destroyAllWindows()

#f1=open('hw3data.txt','r')
plot_data(y_data)
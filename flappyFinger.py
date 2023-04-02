import cv2
import mediapipe as mp
import time
import handTrackingModule as hmt
import random
import cvzone

score = 0
fix_fx = 500

def wall(img,lim,pos):
	cv2.line(img,(pos,0),(pos,lim-60),(0,0,255),40)
	cv2.line(img,(pos,lim+60),(pos,img.shape[0]),(0,0,255),40)
	return img

def refresh(pos,lim,fresh):
	global score
	if pos<fix_fx-20 and fresh:
		score+=1
		fresh=0
	if pos<100:
		pos = 1280
		fresh=1
		lim = random.randint(50,650)
	return [pos,lim,fresh]


def play():
	cap = cv2.VideoCapture(0)
	pTime = 0
	cTime = 0
	detector = hmt.handDetector()
	pos1 = 1280
	lim1 = 400
	pos2 = 1800
	lim2 = 500
	flag=0
	fresh1=1
	fresh2=1
	while True:
		pos1-=20
		pos2-=20
		success,img = cap.read()
		img = cv2.flip(img,1)
		img = wall(img,lim1,pos1)
		if pos2<1280:
			img = wall(img,lim2,pos2)
		img =  detector.findHands(img,draw=False)
		lmList1 = detector.findPositions(img,handNo=0,pos=8,draw=False)
		if len(lmList1):
			idd,fx,fy = lmList1
			cv2.circle(img,(fix_fx,fy),15,(0,255,0),cv2.FILLED)
			if lim1-50<fy<lim1+50 or (fix_fx>pos1+5 or fix_fx<pos1-5):
				pass
			else:
				flag=1

			if lim2-50<fy<lim2+50 or (fix_fx>pos2+5 or fix_fx<pos2-5):
				pass
			else:
				flag=1
		else:
			while len(lmList1)==0:
				success,img = cap.read()
				img = cv2.flip(img,1)
				img = wall(img,lim1,pos1)
				if pos2<1280:
					img = wall(img,lim2,pos2)
				imgPause = cv2.imread("static/paused.png",cv2.IMREAD_UNCHANGED)
				imgPause = cv2.resize(imgPause, (0, 0), fx = 0.5, fy = 0.5)
				img = cvzone.overlayPNG(img,imgPause,[300,150])
				cv2.imshow("Image",img)
				img =  detector.findHands(img,draw=False)
				lmList1 = detector.findPositions(img,handNo=0,pos=8,draw=False)
				cv2.waitKey(1)
			idd,fx,fy = lmList1
			cv2.circle(img,(fix_fx,fy),15,(0,255,0),cv2.FILLED)
			if lim1-50<fy<lim1+50 or (fix_fx>pos1+5 or fix_fx<pos1-5):
				pass
			else:
				flag=1
		cTime = time.time()
		fps = 1/(cTime-pTime)
		pTime = cTime
		cv2.putText(img,"Score: "+str(score),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
		pos1,lim1,fresh1 = refresh(pos1,lim1,fresh1)
		pos2,lim2,fresh2 = refresh(pos2,lim2,fresh2)
		cv2.imshow("Image",img)
		if flag==1:
			imgGraphics = cv2.imread("static/gameover.png",cv2.IMREAD_UNCHANGED)
			img = cvzone.overlayPNG(img,imgGraphics,[150,150])
			cv2.imshow("Image",img)
			cv2.waitKey(3000)
			break
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

play()
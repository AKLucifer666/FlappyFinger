import cv2
import mediapipe as mp
import time

class handDetector():
	def __init__(self,mode=False,maxHands = 2,model_complexity=1,detectionCon=0.5,trackCon=0.5):
		self.mode = mode
		self.maxHands = maxHands
		self.detectionCon = detectionCon
		self.trackCon = trackCon
		self.model_complexity = model_complexity

		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.model_complexity, self.detectionCon, self.trackCon)
		self.mpDraw = mp.solutions.drawing_utils

	def findHands(self, img, draw=True):
		imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)
		#print(results.multi_hand_landmarks)
		if self.results.multi_hand_landmarks:
			for handLms in self.results.multi_hand_landmarks:
				if draw:
					 self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

		return img

	def findPositions(self, img, handNo=0, pos=0, draw=True):
		lmList = []
		if self.results.multi_hand_landmarks:
			try:
				myHand = self.results.multi_hand_landmarks[handNo]
				for idd, lm in enumerate(myHand.landmark):
					h,w,c = img.shape
					cx, cy = int(lm.x*w),int(lm.y*h)
					if idd==pos:
						lmList = [idd, cx,cy]
					if draw:
						cv2.circle(img,(cx,cy),15,(0,0,255),cv2.FILLED)
			except:
				return lmList

		return lmList



def main():
	cap = cv2.VideoCapture(0)
	pTime = 0
	cTime = 0
	detector = handDetector()
	while True:
		success,img = cap.read()
		img =  detector.findHands(img)
		lmList = detector.findPositions(img)
		if len(lmList)!=0: 
			print(lmList[1])
		cTime = time.time()
		fps = 1/(cTime-pTime)
		pTime = cTime

		cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
		cv2.imshow("Image",img)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break



if __name__ == "__main__":
	main()
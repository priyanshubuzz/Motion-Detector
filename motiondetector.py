import cv2
import pandas
from datetime import datetime

video = cv2.VideoCapture(0)

first_frame = None
status_list = []
times = []

while True:
    frame = video.read()[1]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21),0)

    status = 0 
    
    if first_frame is None:
        first_frame = gray
        status_list.append(status) #since at starting we're capturing bg without moving object
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
    contours = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    for contour in contours:
        if cv2.contourArea(contour) > 10000:
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 4)
            status = 1

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-2] == 0 and status_list[-1] == 1:
        times.append(datetime.now())
    elif status_list[-2] == 1 and status_list[-1] == 0:
        times.append(datetime.now())

    cv2.imshow("Motion Detector", frame)
    # cv2.imshow("Delta Frame", delta_frame)
    # cv2.imshow("Thresh Frame", thresh_frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        if status==1:
            times.append(datetime.now())
        break  
    
cv2.destroyAllWindows()
video.release()

df = pandas.DataFrame(columns= ["Start", "End"])

for i in range(0,len(times),2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")
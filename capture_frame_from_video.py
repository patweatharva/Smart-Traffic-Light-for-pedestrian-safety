import cv2
 
# Opens the inbuilt camera of laptop to capture video.


#cap = cv2.VideoCapture("Path_to_video")
cap = cv2.VideoCapture(0)
i = 0

 
while(cap.isOpened()):
    ret, frame = cap.read()
     
    # This condition prevents from infinite looping
    # incase video ends.
    if ret == False:
        break
     
    # Save Frame by Frame into disk using imwrite method
    if cv2.waitKey(0) & 0xFF == ord('x'):
        cv2.imwrite('Frame'+str(i)+'.jpg', frame)
        i += 1
 
cap.release()
cv2.destroyAllWindows()
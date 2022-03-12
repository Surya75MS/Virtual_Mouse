import cv2 as c
import autopy
import time
import numpy as npy
import HandTrackingModule as htm

(width_cam, height_cam) = (650, 750)
(width_scr, height_scr) = autopy.screen.size()
smoothening = 7
PreviousTime = 0
(prev_locX, prev_locY) = (0, 0)
(cur_locX, cur_locY) = (0, 0)
(StartX, StartY) = (200, 150)
(EndX, EndY) = (400, 350)

vid = c.VideoCapture(0)

# Not working
vid.set(3, width_cam)  # ID for width_cam is 3
vid.set(4, height_cam)  # ID for height_cam is 4
# Not working

detector = htm.handDetector(maxHands=1)

while True:
    # 1. Find hand landmarks.
    success, frame = vid.read()
    frame = detector.findHands(frame)
    lmList, bbox = detector.findPosition(frame)

    # 2. To get coordinates of middle_finger_MCP(metacarpophalangeal joint)
    if (len(lmList) != 0):
        x1, y1 = lmList[9][1:]

        # 3. Check which fingers are up.
        fingers = detector.fingersUp()
        c.rectangle(frame, (StartX, StartY), (EndX, EndY), (0, 255, 255), 2)

        # 4. All fingers up. Moving mode
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:

            # 5. Convert co-ordinates so that small dimensions of webcam will be converted to dimensions equal to screen.
            x3 = npy.interp(x1, (StartX, EndX), (0, width_scr))
            y3 = npy.interp(y1, (StartY, EndY), (0, height_scr))

            # 6. Smoothen values
            cur_locX = prev_locX + (x3-prev_locX) / smoothening
            cur_locY = prev_locY + (y3-prev_locY) / smoothening

            # 7. Move mouse
            autopy.mouse.move(width_scr-cur_locX, cur_locY)
            c.circle(frame, (x1, y1), 15, (255, 0, 0), c.FILLED)
            prev_locX, prev_locY = cur_locX, cur_locY
            
        # 8. Check if in clicking mode if both middle and index fingers are up.

            # 9. Find distance b/w fingers
            length, frame, lineInfo = detector.findDistance(8, 12, frame)
            print(length)

            # 10. Scrolling if distance is shoxrt
            if length < 20:
                c.circle(frame, (lineInfo[4], lineInfo[5]),15, (255, 255, 0), c.FILLED)
                autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
                # c.putText(frame,"Scrolling",(200,44),c.CALIB_CB_LARGER, 1, (0,0,0), 5)
                time.sleep(0.35)

        if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
            autopy.mouse.click(autopy.mouse.Button.LEFT)
            # c.putText(frame,"Left click",(200,44),c.CALIB_CB_LARGER, 1, (0,0,0), 5)
            time.sleep(0.2)
        elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
            # c.putText(frame,"Right click",(200,44),c.CALIB_CB_LARGER, 1, (0,0,0), 5)
            time.sleep(0.2)

    # 11. Frame rate
    currentTime = time.time()
    fps = 1/(currentTime-PreviousTime)
    PreviousTime = currentTime
    c.putText(frame, str(int(fps)), (15, 47),
              c.FONT_HERSHEY_TRIPLEX, 3, (0, 255, 255), 5)

    # 12. Display
    c.imshow("Image", frame)
    c.waitKey(1)

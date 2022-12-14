import cv2
import mediapipe as mp

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

# Initialising default webcam
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()  # Initialises a hand object
mpDraw = mp.solutions.drawing_utils # Initialising drawing module to draw landmarks

while True:

    success, img = cap.read()  # Reading each frame and storing in img
    img = cv2.flip(img, 1)
    h, w, c = img.shape  # Gives height width and color channel of image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV takes image in BGR format, so first we convert it to RGB
    # format
    results = hands.process(imgRGB)  # Process the image and identify the hands

    # multi_hand_landmarks gives all the landmarks
    if results.multi_hand_landmarks:  # If any hand is detected
        for handLms in results.multi_hand_landmarks:  # Iterate over all the landmarks of the hand in frame
            lm_list = []
            for lm in handLms.landmark:
                lm_list.append(lm)

            if lm_list[8].y < lm_list[7].y and lm_list[12].y < lm_list[11].y and lm_list[16].y < lm_list[15].y and \
                    lm_list[20].y < lm_list[19].y and lm_list[4].y < lm_list[3].y and lm_list[12].y < lm_list[9].y < \
                    lm_list[0].y:
                cv2.putText(img, 'STOP', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            finger_fold_status = []
            if lm_list[0].x < lm_list[9].x:  # If hand is Left Hand
                for tip in finger_tips:
                    x, y = int(lm_list[tip].x*w), int(lm_list[tip].y*h)
                    print('LEFT HAND')
                    # cv2.circle(img, (x, y), 15, (0, 0, 255), cv2.FILLED)

                    if lm_list[tip].x < lm_list[tip-3].x:
                        finger_fold_status.append(True)
                        # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    else:
                        finger_fold_status.append(False)
            else:  # Hand is Right
                for tip in finger_tips:
                    x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                    print('RIGHT HAND')
                    # cv2.circle(img, (x, y), 15, (0, 0, 255), cv2.FILLED)

                    if lm_list[tip].x > lm_list[tip - 3].x:
                        finger_fold_status.append(True)
                        # cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    else:
                        finger_fold_status.append(False)
            # print(finger_fold_status)

            if all(finger_fold_status):
                if lm_list[thumb_tip].y < lm_list[thumb_tip-1].y < lm_list[thumb_tip-2].y:
                    print("THUMBS UP")
                    cv2.putText(img, "THUMBS UP", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                if lm_list[thumb_tip].y > lm_list[thumb_tip-1].y > lm_list[thumb_tip-2].y:
                    print("THUMBS DOWN")
                    cv2.putText(img, "THUMBS DOWN", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            # HAND_CONNECTIONS connects or draws the lines
            # draw_landmarks draws all 21 points in a hand using img and landmarks (handLms)

    cv2.imshow("Image", img)  # Shows the camera input. We can give any name instead of 'Image'
    cv2.waitKey(1)  # To hold the output window

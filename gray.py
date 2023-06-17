import cv2

image = cv2.imread('hukei.png')
image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

cv2.imshow("hukei_gray", image_gray)
cv2.imwrite("./hukei_gray.png", image_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
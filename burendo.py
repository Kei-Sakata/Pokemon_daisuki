import cv2

img1 = cv2.imread('hukei.png')
img2 = cv2.imread('hito.png')

img2 = cv2.resize(img2, img1.shape[1::-1])

alpha = cv2.addWeighted(img1, 0.4, img2, 0.8, 0)
cv2.imwrite('./hukei_alpha.png', alpha)
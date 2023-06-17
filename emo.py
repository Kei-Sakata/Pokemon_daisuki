import cv2
import numpy as np
from scipy.interpolate import splrep, splev
 
def peripheral_light_correct(img, gain_params):
    h, w = img.shape[:2]
    size = max([h, w])  
 
    x = np.linspace(-w / size, w / size, w)
    y = np.linspace(-h / size, h / size, h)  
    xx, yy = np.meshgrid(x, y)
    r = np.sqrt(xx ** 2 + yy ** 2)
 
    gainmap = gain_params * r + 1
 
    return np.clip(img * gainmap, 0., 255)
 

def main():
    img = cv2.imread("hukei.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

 
    h, w = gray.shape
    gauss = np.random.normal(0, 10, (h, w))
    gauss = gauss.reshape(h, w)
    gray = np.clip(gray + gauss, 0, 255).astype(np.uint8)
 
    xs = [0, 0.25, 0.5, 0.75, 1]
    ys = [0, 0.15, 0.5, 0.85, 0.99]
    gray = gray / 255
    tck = splrep(xs, ys)  
    gray = splev(gray, tck)*255  
 
    gray = peripheral_light_correct(gray, -0.4).astype(np.uint8)
 
    img_hsv = np.zeros_like(img)
    img_hsv[:, :, 0] = np.full_like(img_hsv[:, :, 0], 15, dtype=np.uint8)
    img_hsv[:, :, 1] = np.full_like(img_hsv[:, :, 1], 153, dtype=np.uint8)
    img_hsv[:, :, 2] = gray
    img = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
 
    cv2.imwrite("./hukei_emo.png", img)
 
 
if __name__ == '__main__':
    main()
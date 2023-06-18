import cv2
import numpy as np
def masuku(pokemon,haikei):    
    img = cv2.imread(pokemon)
    bg_img = cv2.imread(haikei)
    fg_img = cv2.resize(img, (int(bg_img.shape[1]/3), int(bg_img.shape[1]/3)))
    
    # 前景画像をHSV色空間に変換
    # fg_hsv = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)
    
    
    x, y = 200, 100
    
    # 合成する領域
    w = min(fg_img.shape[1], bg_img.shape[1] - x)
    h = min(fg_img.shape[0], bg_img.shape[0] - y)
    
    
    # fg_gray = cv2.cvtColor(fg_img,cv2.COLOR_BGR2GRAY)
    # ret, dst = cv2.threshold(fg_gray, 0, 255, cv2.THRESH_OTSU)
    # cv2.imwrite("./Result_mizyu_bin.jpg", dst)
    bin_img1 = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)
    bin_img = cv2.inRange(bin_img1, (0, 2, 0), (255, 255, 255))
    
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=lambda x: cv2.contourArea(x))
    
    mask = np.zeros_like(bin_img)
    cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
    
    bg_roi = bg_img[y : y + h, x : x + w]
    
    mask_indices = np.where(mask[:h, :w] == 255)
    
    bg_roi_hsv = cv2.cvtColor(bg_roi, cv2.COLOR_BGR2HSV)
    bg_roi_s = np.mean(bg_roi_hsv[np.where(mask[:h, :w] == 255)][:, 1])
    bg_roi_v = np.mean(bg_roi_hsv[np.where(mask[:h, :w] == 255)][:, 2])
    # 前面画像の平均彩度と平均明度
    fg_hsv = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)
    fg_roi_s = np.mean(fg_hsv[np.where(mask[:h, :w] == 255)][:, 1])
    fg_roi_v = np.mean(fg_hsv[np.where(mask[:h, :w] == 255)][:, 2])
    
    # 背景画像の明度と彩度に前面画像の明度と彩度からの変化量を加える
    if fg_roi_v - bg_roi_v <= 0:
        fg_hsv[:, :, 1] = np.clip(fg_hsv[:, :, 1] + (bg_roi_s - fg_roi_s), 0, 255).astype(np.uint8)
    elif fg_roi_v - bg_roi_v > 0:
        fg_hsv[:, :, 2] = np.clip(fg_hsv[:, :, 2] + (bg_roi_v - fg_roi_v), 0, 255).astype(np.uint8)
    
    
    
    # 背景画像の平均の彩度と明度
    # bg_roi_hsv = cv2.cvtColor(bg_roi, cv2.COLOR_BGR2HSV)
    # fg_roi_hsv = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)
    # bg_roi_s = bg_roi_hsv[np.where(mask[:h, :w] == 255)][:,1]
    # bg_roi_v = bg_roi_hsv[np.where(mask[:h, :w] == 255)][:,2]
    # # 前面画像の平均の彩度と明度
    # fg_roi_hsv = cv2.cvtColor(fg_img, cv2.COLOR_BGR2HSV)
    # fg_roi_s = fg_roi_hsv[np.where(mask[:h, :w] == 255)][:,1]
    # fg_roi_v = fg_roi_hsv[np.where(mask[:h, :w] == 255)][:,2]
    # fg_roi_hsv[np.where(mask[:h, :w] == 255)][:,1]= bg_roi_s
    # fg_roi_hsv[np.where(mask[:h, :w] == 255)][:,2] = bg_roi_v
    # fg_hsv[..., 1][mask_indices] = bg_roi_s
    # fg_hsv[..., 2][mask_indices] = bg_roi_v
    rgb = cv2.cvtColor(fg_hsv, cv2.COLOR_HSV2BGR)
    
    # 合成する
    fg_roi = rgb[:h, :w]
    bg_roi[np.where(mask[:h, :w] == 255)] = fg_roi[np.where(mask[:h, :w] == 255)]
    
    return bg_img
    # newbg_img = bg_img
    
    # bg_img = cv2.imread("./kusamura.jpg")
    
    # alpha = cv2.addWeighted(bg_img, 0.4, newbg_img, 0.7, 20)
    # cv2.imwrite("./Result_alpha.jpg", alpha)
    

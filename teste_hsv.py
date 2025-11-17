import cv2

img = cv2.imread("mapas/forest1.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        print("HSV:", pixel)

cv2.imshow("imagem", img)
cv2.setMouseCallback("imagem", click)

cv2.waitKey(0)
cv2.destroyAllWindows()

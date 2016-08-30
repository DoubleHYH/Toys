import cv2

imageName = 'big.jpg'

def get_char(gray_number):
	length = len(list(r"$@&%B#=-. "))
	unit = (256.0 + 1)/length
	return list(r"$@&%B#=-. ")[int(gray_number/unit)]

image = cv2.resize(cv2.imread(imageName,cv2.IMREAD_GRAYSCALE),(110,85))
txt = ''
for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		txt += get_char(image[i,j])
	txt += '\n'
f = open('output.txt','w')
f.write(txt)

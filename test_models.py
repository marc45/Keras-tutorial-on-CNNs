import cv2
import numpy as np

from keras.models import model_from_json
from keras.datasets import cifar10

from vgg_cifar10 import load_cifar10_data
from vgg_face_detection import load_celeba


model_selection = raw_input('Choose simple/vgg_class/vgg_regr: ')

if model_selection == 'simple':
	STAMP = 'simple_cnn'
	(x_train, y_train), (x_val, y_val) = cifar10.load_data()
	print(x_val.shape[0], 'test samples')

elif model_selection == 'vgg_class':
	STAMP = 'vgg_cifar10'
	x_train, y_train, x_val, y_val = load_cifar10_data()

elif model_selection == 'vgg_regr':
	STAMP = 'face_detection'
	x_train, y_train, x_val, y_val = load_celeba(num_batches=1)

else:
	print('Model should be one of simple/vgg_class/vgg_regr')


x_val_orig = x_val
x_val = x_val.astype('float32')
x_val /= 255

json_file = open('model/' + STAMP + '.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights('model/' + STAMP + '.h5')
print("Loaded model from disk")


for c,(img, x_img, lab) in enumerate(zip(x_val_orig, x_val, y_val)):
	x_img = x_img.reshape(1,x_img.shape[0],x_img.shape[1],x_img.shape[2])
	pred = model.predict(x_img)
	if model_selection == 'simple':
		pred = np.argmax(pred)
		img = cv2.resize(img, (150,150))
		print('Predicted class: %d' % pred)
		print('Original class: %d' % lab)
		cv2.imshow('image',img)
		k = cv2.waitKey(0)
		if k == ord('q'):
			cv2.destroyAllWindows()
			break
		

	elif model_selection == 'vgg_class':
		pred = np.argmax(pred)
		lab = np.argmax(lab)
		img = cv2.resize(img, (150,150))
		print('Predicted class: %d' % pred)
		print('Original class: %d' % lab)
		cv2.imshow('image',img)
		k = cv2.waitKey(0)
		if k == ord('q'):
			cv2.destroyAllWindows()
			break
		

	else:
		x_1,y_1,width,height = pred[0].astype(int)
		predicted_roi = img[y_1:y_1+height,x_1:x_1+width,:]
		cv2.rectangle(img,(x_1,y_1),(x_1+width,y_1+height),(0,255,0),3)
		cv2.imshow('image',img)
		k = cv2.waitKey(0)
		if k == ord('q'):
			cv2.destroyAllWindows()
			break
		
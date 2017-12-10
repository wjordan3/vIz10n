from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np

img_width, img_height = 150, 150


test_model = load_model('multi_class_third_try_full_model.h5')

img = load_img('/Users/wjordan/Downloads/Pandora_V1/Baroque/6496.jpg',False,target_size=(img_width,img_height))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)
"to match rescale"
x = x/255
preds = test_model.predict_classes(x)
prob = test_model.predict_proba(x)
#print(preds, prob)
print(classes[preds], prob)

img = load_img('/Users/wjordan/Downloads/Pandora_V1/Baroque/37.jpg',False,target_size=(img_width,img_height))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)
"to match rescale"
x = x/255
preds = test_model.predict_classes(x)
prob = test_model.predict_proba(x)
#print(preds, prob)
print(classes[preds], prob)

img = load_img('/Users/wjordan/Downloads/Pandora_V1/Cubism/Pablo Ruiz Picasso (387)456.jpg',False,target_size=(img_width,img_height))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)
"to match rescale"
x = x/255
preds = test_model.predict_classes(x)
prob = test_model.predict_proba(x)
#print(preds, prob)
print(classes[preds], prob)

img = load_img('/Users/wjordan/Downloads/Pandora_V1/Romanticism/2319.jpg',False,target_size=(img_width,img_height))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)
"to match rescale"
x = x/255
preds = test_model.predict_classes(x)
prob = test_model.predict_proba(x)
#print(preds, prob)
print(classes[preds], prob)

img = load_img('/Users/wjordan/Downloads/Pandora_V1/realism/McCarthy/Brian McCarthy 1960 - Irish Realist painter - Tutt\'Art@ (14).jpg',False,target_size=(img_width,img_height))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)
"to match rescale"
x = x/255
preds = test_model.predict_classes(x)
prob = test_model.predict_proba(x)
#print(preds, prob)
print(classes[preds], prob)

img = load_img('/Users/wjordan/Downloads/Pandora_V1/Fauvism/Valtat/Louis Valtat_3.jpg',False,target_size=(img_width,img_height))
x = img_to_array(img)
x = np.expand_dims(x, axis=0)
"to match rescale"
x = x/255
preds = test_model.predict_classes(x)
prob = test_model.predict_proba(x)
#print(preds, prob)
print(classes[preds], prob)



classes = np.array(['baroque','cubism','romanticism'])


def predict_style(image_path):
	img = load_img(image_path,False,target_size=(img_width,img_height))
	x = img_to_array(img)
	x = np.expand_dims(x, axis=0)
	"to match rescale"
	x = x/255
	preds = test_model.predict_classes(x)
	prob = test_model.predict_proba(x)
	return print(classes[preds], prob)
 





predict_style('/Users/wjordan/Downloads/Pandora_V1/Baroque/6496.jpg')

predict_style('/Users/wjordan/Downloads/Pandora_V1/Baroque/37.jpg')

predict_style('/Users/wjordan/Downloads/Pandora_V1/Cubism/Pablo Ruiz Picasso (387)456.jpg')

predict_style('/Users/wjordan/Downloads/Pandora_V1/Romanticism/2319.jpg')

predict_style('/Users/wjordan/Downloads/Pandora_V1/realism/McCarthy/Brian McCarthy 1960 - Irish Realist painter - Tutt\'Art@ (14).jpg')

predict_style('/Users/wjordan/Downloads/Pandora_V1/Fauvism/Valtat/Louis Valtat_3.jpg')







test_datagen = ImageDataGenerator(rescale=1. / 255)


validate_generator = test_datagen.flow_from_directory(
    'preview',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

predict = test_model.predict_generator(validate_generator, use_multiprocessing=True)
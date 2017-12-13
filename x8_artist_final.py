from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint
from keras.callbacks import ReduceLROnPlateau
from keras.models import Model
from keras import applications
from keras import regularizers


img_width, img_height = 224, 224
number_of_categories= 28
train_data_dir = 'artist/data/train'
validation_data_dir = 'artist/data/validation'
nb_train_samples = 100*number_of_categories
nb_validation_samples = 20*number_of_categories
#rounds of training
epochs = 75
batch_size = 10
#number of images for each pass through the network
#smaller requires less memory and is faster but less accurate for calculating gradient


train_datagen = ImageDataGenerator(
    #Will return int in python2 if not specificed with "."
    rescale=1. / 255,
    zoom_range=0.2,
    width_shift_range=0.2,
    height_shift_range=0.2,
    rotation_range=90,
    horizontal_flip=True,
    vertical_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

#generator for retrieving and creating training images with random transformations
train_generator = train_datagen.flow_from_directory(
	train_data_dir,
	target_size=(img_width, img_height),
	batch_size=batch_size,
)

#generator for retrieving validation images
validation_generator = test_datagen.flow_from_directory(
	validation_data_dir,
	target_size=(img_width, img_height),
	batch_size=batch_size,
)
#load VGG16 internal model
vgg_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(img_width,img_height,3))

model = Sequential()

#add layers from VGG16
for l in vgg_model.layers:
    model.add(l)

#creating top layers to stack onto VGG16
top_model = Sequential()
top_model.add(Flatten(input_shape=model.output_shape[1:]))
top_model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.01), name='final_layer'))
top_model.add(Dropout(0.5))
top_model.add(Dense(number_of_categories, activation='softmax'))

#add top layers to model
model.add(top_model)

#Freeze VGG16 layers
for i in model.layers[:-4]:
    i.trainable = False

#configure model for training 
model.compile(optimizer='sgd',
loss='categorical_crossentropy',
metrics=['accuracy'])

#generates log files
tensorboard=TensorBoard(log_dir='./artistFinal_logs', histogram_freq=0, batch_size=batch_size, write_graph=True, write_grads=True, write_images=True, embeddings_freq=0, embeddings_layer_names='final_layer', embeddings_metadata='./artistFinal_metadata')

#ensure the best model is saved based on maximum validation accuracy attained during training rounds
best_model_checkpoint = ModelCheckpoint(filepath='artist_final_best_model.h5', monitor='val_acc', verbose=0, save_best_only=True, save_weights_only=False, mode='auto', period=1)

#if the validation_loss stalls after 5 epochs then the learning rate will be lowered
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

history_tl = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    class_weight='auto',
    callbacks=[tensorboard, best_model_checkpoint, reduce_lr],
    use_multiprocessing = True)


model.save('artist_model_final.h5')


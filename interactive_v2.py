from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import cv2

# Predicts the class (style or artist) of the inputted image using the inputted model
# Arguments are filename, test_model

#Will not need this
#filename = sys.argv[1]
#test_model = load_model(sys.argv[2])
print("Initializing")

artist_model = load_model('artist_final_best_model.h5')

style_model = load_model('style_final_best_model.h5')

img_width, img_height = 224, 224

style_classes = np.array(['early renaissance', 'high renaissance','rococo','impressionism','baroque','realism',\
    'neoclassicism', 'medieval', 'northern renaissance', 'post-impressionism', 'mannerism','romanticism'])

style_classes.sort()

artist_classes = np.array(['john everett millais', 'frederic leighton', 'anthony van dyck', 'godfrey kneller', 'john opie',\
    'carel victor morlais weight','joshua reynolds','marianne north','john duncan fergusson', 'henry raeburn',\
    'thomas gainsborough','thomas lawrence', 'william etty', 'joseph mallord william turner', 'peter lely', 'kyffin williams',\
    'laurence stephen lowry', 'alfred james munnings', 'walter richard sickert','william orpen','frank brangwyn',\
    'duncan grant','henry scott tuke','john lavery','peter paul rubens','george frederic watts', 'john constable','augustus edwin john'])

artist_classes.sort()

print("Hello, welcome to the painting image classifier")

active_model = None

def select_model():
    print("select 1 for style classification")
    print("select 2 for artist classification")
    response = input("Which classifier would you like to use:")


    if response == '1':
        return response
    elif response == '2':
        return response
    else:
        print("Please choose an applicable option!")
        select_model()

def select_image():
    response = input("What is the file path to the image you would like to classify:")

    if response == '':
        print('Error! No image inputted.')
        select_image()
    elif response.find('.jpg') == -1:
        print('Error! The file must be a jpeg.')
        select_image()
    else:
        return response



user_model = select_model()

user_image = select_image()

if user_model == '1':
    active_model = style_model
elif user_model == '2':
    active_model = artist_model


#everything above is not complete
#################################################################################

def predict_style(image_path, number_to_return=1):
    try:
        img = load_img(image_path,False,target_size=(img_width,img_height))
    except:
        return "Issue with file_path unable to predict", "Issue with file_path unable to predict"
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    #to match rescaled images used for training
    x = x/255
    #flatten ensures array of probabilities is 1 dimensional
    prob = style_model.predict_proba(x).flatten()
    #indices containing desired number of predictions
    indices = np.argpartition(prob, -number_to_return)[-number_to_return:]
    #[::-1] is to flip array as predictions are for least to greatest
    indices = indices[np.argsort(prob[indices])][::-1]
    if number_to_return > 1:
        return tuple( style_classes[indices]), tuple( prob[indices])
    else:
        return str(style_classes[indices].tolist()[0]), str(prob[indices].tolist()[0])

"""
no_errors = True
if filename == '':
    print('Error! No image inputted.')
    no_errors = False
elif filename.find('.jpg') != -1:
    print('Error! The file must be a jpeg.')
    no_errors = False
elif test_model == '':
    print('Error! No model inputted.')
    no_errors = False
elif test_model.find('.h5') != -1:
    print('Error! Invalid keras model.')
    no_errors = False
if no_errors:
"""


#just for testing purposes assign appropriate replace filename with user_image once complete
filename = user_image.strip(' ')
class_prediction, class_probabilities = predict_style(filename, 3)
img = cv2.imread(filename)
text1 = str(class_prediction) + ": "
text2 = str(class_probabilities)
#putText(image, text, position, font, font size, font color, font thickness)
cv2.putText(img, text1, (10,35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
cv2.putText(img, text2, (10,85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
cv2.imshow("Predictions", img)
cv2.waitKey()

#there is some sort of bug in cv2 that I have yet to figure out but image displays at least, just does not close
cv2.destroyWindow("testing")
cv2.waitKey(-1)
cv2.imshow("testing", img)
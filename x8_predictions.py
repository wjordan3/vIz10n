from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import sqlite3
from collections import defaultdict
import pandas as pd


img_width, img_height = 224, 224

artist_model = load_model('keras/artist_final_best_model.h5')

style_model = load_model('keras/style_final_best_model.h5')

style_classes = np.array(['early renaissance', 'high renaissance','rococo','impressionism','baroque','realism',\
    'neoclassicism', 'medieval', 'northern renaissance', 'post-impressionism', 'mannerism','romanticism'])

style_classes.sort()

artist_classes = np.array(['john everett millais', 'frederic leighton', 'anthony van dyck', 'godfrey kneller', 'john opie',\
    'carel victor morlais weight','joshua reynolds','marianne north','john duncan fergusson', 'henry raeburn',\
    'thomas gainsborough','thomas lawrence', 'william etty', 'joseph mallord william turner', 'peter lely', 'kyffin williams',\
    'laurence stephen lowry', 'alfred james munnings', 'walter richard sickert','william orpen','frank brangwyn',\
    'duncan grant','henry scott tuke','john lavery','peter paul rubens','george frederic watts', 'john constable','augustus edwin john'])

artist_classes.sort()


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

#a,b = predict_style('/Users/wjordan/Downloads/Pandora_V1/Baroque/37.jpg')
#predict_artist('/Users/wjordan/Downloads/Pandora_V1/Baroque/37.jpg')

def predict_artist(image_path, number_to_return=1):
	try:
		img = load_img(image_path,False,target_size=(img_width,img_height))
	except:
		return "Issue with file_path unable to predict", "Issue with file_path unable to predict"
	x = img_to_array(img)
	x = np.expand_dims(x, axis=0)
	#to match rescaled images used for training
	x = x/255
	#flatten ensures array of probabilities is 1 dimensional
	prob = artist_model.predict_proba(x).flatten()
	#indices containing desired number of predictions
	indices = np.argpartition(prob, -number_to_return)[-number_to_return:]
	#[::-1] is to flip array as predictions are for least to greatest
	indices = indices[np.argsort(prob[indices])][::-1]
	if number_to_return > 1:
		return tuple( artist_classes[indices]), tuple( prob[indices])
	else:
		return str(artist_classes[indices].tolist()[0]), str(prob[indices].tolist()[0])

conn = sqlite3.connect('artwork.db')
c = conn.cursor()
#select all images from database
c.execute('''
		SELECT style, image_filename, artist_name
		FROM fact_table f
		JOIN styles s ON f.style_id = s.id
		JOIN paintings p ON f.painting_id = p.id
		JOIN artists a ON f.artist_id = a.id
		WHERE style IN (
		    SELECT style
		    FROM fact_table f
		    JOIN styles s ON f.style_id = s.id
		    JOIN paintings p ON f.painting_id = p.id
		    GROUP BY style)
        ''')

style_file_names = list(c.fetchall())

dataFrame_storage = defaultdict(list)

for record in style_file_names:
	style = record[0]
	image_path = record[1]
	artist = record[2]

	predicted_style_classes, predicted_style_probabilities = predict_style(image_path, 3)
	#top_style_class = predicted_style_classes[0]
	#top_style_probability = predicted_style_probabilities[0]

	predicted_artist_classes, predicted_artist_probabilities = predict_artist(image_path, 3)
	#top_artist_class = predicted_artist_class[0]
	#top_artist_probability = predicted_artist_probabilities[0]

	dataFrame_storage['style'].append(style)
	dataFrame_storage['image_filename'].append(image_path)
	dataFrame_storage['artist_name'].append(artist)

	dataFrame_storage['predicted_styles'].append(predicted_style_classes)
	dataFrame_storage['predicted_style_probabilities'].append(predicted_style_probabilities)

	dataFrame_storage['predicted_artists'].append(predicted_artist_classes)
	dataFrame_storage['predicted_artist_probabilities'].append(predicted_artist_probabilities)


file_to_save = pd.DataFrame(dataFrame_storage)

file_to_save.to_csv('database_predictions.csv', encoding='utf-8', index=False)


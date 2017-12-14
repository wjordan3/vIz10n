from collections import defaultdict
import sqlite3
import os
import sys
import random
import shutil

#args = sys.argv[1:]
#file_directory = str(args[0])

#run this in python3
def make_directory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def create_image_copy(file_names , target_directory, style, train_number=530, test_number=160):
	#file_names = os.listdir(directory)
	target_directory = target_directory + '/'

	if len(file_names) < train_number + test_number:
		return 'Not enough images,: ' + style
	#randomize images
	random.shuffle(file_names)
	file_names = file_names[:train_number+test_number]
	for i in range(train_number+test_number):
		#file = directory + '/' + file_names[i]
		file = file_names[i]
		if i >= train_number:
			make_directory(target_directory + 'data/validation/' + style)
			shutil.copyfile(file, os.path.join(target_directory + 'data/validation/' + style, os.path.basename(file)))
		else:
			make_directory(target_directory + 'data/train/' + style)
			shutil.copyfile(file, os.path.join(target_directory + 'data/train/' + style, os.path.basename(file)))

#if len(args) < 1:
#	print("must provide folder name")
#	exit()

conn = sqlite3.connect('artwork.db')
c = conn.cursor()
c.execute('''
		SELECT style, image_filename
		FROM fact_table f
		JOIN styles s ON f.style_id = s.id
		JOIN paintings p ON f.painting_id = p.id
		WHERE style IN (
		    SELECT style
		    FROM fact_table f
		    JOIN styles s ON f.style_id = s.id
		    JOIN paintings p ON f.painting_id = p.id
		    WHERE style IS NOT ''
		    GROUP BY style
		    HAVING count(image_filename) >= 690) 
        ''')
style_file_names = set(c.fetchall())

dict_style_file_names = defaultdict(list)

for item in style_file_names:
    #dict_style_file_names[item[0]].append(file_directory+ '/'+ item[1])
    dict_style_file_names[item[0].encode('utf-8').strip()].append(item[1].encode('utf-8').strip())

for key in dict_style_file_names.keys():
	create_image_copy(dict_style_file_names[key], 'keras/style', key)


c.execute('''
		SELECT artist_name, image_filename
		FROM fact_table f
		JOIN artists a ON f.artist_id = a.id
		JOIN paintings p ON f.painting_id = p.id
		WHERE artist_name IN (
		    SELECT artist_name
		    FROM fact_table f
		        JOIN artists a ON f.artist_id = a.id
		        JOIN paintings p ON f.painting_id = p.id
		    GROUP BY artist_name
		    HAVING count(image_filename) >= 120
		    )
         ''')

artist_file_names = set(c.fetchall())

dict_artist_file_names = defaultdict(list)

for item in artist_file_names:
    dict_artist_file_names[item[0].encode('utf-8').strip()].append(item[1].encode('utf-8').strip())

for key in dict_artist_file_names.keys():
	create_image_copy(dict_artist_file_names[key], 'keras/artist', key, train_number=100, test_number=20)


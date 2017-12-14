import pandas as pd
import sqlite3
import csv


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    del df['style']
    del df['artist_name']

    return df


if __name__ == '__main__':

    # This code loads the predicted styles and artists from a CSV file (generated in Keras),
    # and returns a CSV, with each element of the tuple having its own column

    import os
    from urllib.parse import urljoin

    abs_path = urljoin(os.getcwd(), 'Project/data')

    elems = []

    with open(os.path.join(abs_path, 'database_predictions.csv'), newline='', encoding='utf-8') as csvfile:
        isHeader = True
        reader = csv.reader(csvfile)
        for row in reader:
            artist_name = row[0]
            image_filename = row[1]
            predicted_artist_probabilities = row[2].strip('(').strip(')').split(',')
            predicted_artists = row[3].strip('(').strip(')').split(',')
            predicted_style_probabilities = row[4].strip('(').strip(')').split(',')
            predicted_styles = row[5].strip('(').strip(')').split(',')
            style = row[6]
            newElem = [artist_name, image_filename] + predicted_artist_probabilities + predicted_artists + predicted_style_probabilities + predicted_styles + [style]
            if isHeader:
                isHeader = False
            else:
                elems.append(newElem)

    columns = ['artist_name',
               'image_filename',
               'pred_prob_a1',
               'pred_prob_a2',
               'pred_prob_a3',
               'pred_artist1',
               'pred_artist2',
               'pred_artist3',
               'pred_prob_s1',
               'pred_prob_s2',
               'pred_prob_s3',
               'pred_style1',
               'pred_style2',
               'pred_style3',
               'style']

    df = pd.DataFrame(elems, columns=columns)

    cleaned = clean_data(df)

    print(cleaned)

    cleaned.to_csv(os.path.join(abs_path, 'pred_cleaned.csv'), index=False, encoding='utf-8')



import re
import numpy as np
import pandas as pd


def clean_image_address(df: pd.DataFrame) -> pd.DataFrame:

    print(len(df))
    df.drop_duplicates(['image_filename'], keep='first', inplace=True)
    print(len(df))
    pattern = re.compile('.html')


    for index, row in df.iterrows():
        if re.search(pattern,row['image_filename']):
            df.drop(index,inplace=True)
        else:
            df.at[index,'image_filename'] = 'wgaScraping/'+row[0]

    df.loc[11903:11928, 'artist_name'] = 'joshua reynolds'
    df = df.reset_index(drop=True)
    #print(df.loc[df['image_filename'] == 'hunt_y_lady183c.jpg'])
    df['source']='Web Gallery of Art'
    print(df)

    return df



if __name__ == '__main__':
    import os
    from urllib.parse import urljoin

    abs_path = urljoin(os.getcwd(), 'Project/data')
    columns = ['image_filename', 'painting_name', 'artist_name', 'artist_years', 'style', 'artist_school', 'misc',
               'file_info', 'web_url', 'release_year','source']
    df = pd.read_csv(os.path.join(abs_path, 'collection1.csv'), names = columns, encoding='utf-8')
    cleaned = clean_image_address(df)
    cleaned.to_csv(os.path.join(abs_path, 'wga_cleaned.csv'), index=False, encoding='utf-8')



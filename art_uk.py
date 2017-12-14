import re
import numpy as np
import pandas as pd


def clean_image_address(df: pd.DataFrame) -> pd.DataFrame:
    print(len(df))
    #print(df.shape)
    #print(df['image_filename'].value_counts())
    df.drop_duplicates(['image_filename'], keep='first', inplace=True)
    #print(df.shape)
    df = df.reset_index(drop=True)
    df.dropna(axis=0, how='all')
    df['source']='Art UK'
    print(len(df))
    return df


if __name__ == '__main__':
    import os
    from urllib.parse import urljoin

    abs_path = urljoin(os.getcwd(), 'Project/data')
    columns = ['image_filename', 'painting_name', 'artist_name', 'artist_years', 'style', 'artist_school', 'misc',
               'file_info', 'web_url', 'release_year', 'source']
    df = pd.read_csv(os.path.join(abs_path, 'artuk2.csv'), names = columns, encoding='utf-8')
    cleaned = clean_image_address(df)
    cleaned.to_csv(os.path.join(abs_path, 'artuk2_cleaned.csv'), index=False, encoding='utf-8')



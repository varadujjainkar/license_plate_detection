# split_dataset.py
import pandas as pd
from sklearn.model_selection import train_test_split
import os
# Split dataset
def split_dataset(csv_path, output_dir):
    df = pd.read_csv(csv_path)
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

    train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
    val_df.to_csv(os.path.join(output_dir, 'val.csv'), index=False)

split_dataset('data/annotations.csv', 'data/')

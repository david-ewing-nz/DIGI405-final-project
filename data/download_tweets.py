from datasets import load_dataset
import pandas as pd
import os

ds = load_dataset('cardiffnlp/tweet_eval', 'sentiment')
print(ds)

label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}

output_dir = r'D:\github\DIGI405\final-project\data'

for split in ds.keys():
    df = ds[split].to_pandas()
    df['label_name'] = df['label'].map(label_map)
    print(f'\n{split}: {len(df)} rows')
    print(df['label_name'].value_counts())

# Save CSVs
for split in ds.keys():
    df = ds[split].to_pandas()
    df['label_name'] = df['label'].map(label_map)
    file_path = os.path.join(output_dir, f'tweets_{split}.csv')
    df.to_csv(file_path, index=False)
    print(f'Saved tweets_{split}.csv')

print('\nSample tweets:')
train_df = ds['train'].to_pandas()
train_df['label_name'] = train_df['label'].map(label_map)
print(train_df.sample(10, random_state=82171165)[['text','label_name']].to_string())

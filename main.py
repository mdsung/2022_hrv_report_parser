from dataclasses import fields
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from src.parser import FrequencyDomain, General, Nonlinear, Parser, TimeDomain


def get_number_from_file(filename):
    return filename.split('-')[0]

def get_time_from_file(filename):
    if '-1' in filename:
        return "induction"
    elif '-2' in filename:
        return 'operation'
    elif '-3' in filename:
        return 'emergence'
    
def create_dataframe(filename, general:General, timedomain:TimeDomain, frequencydomain:FrequencyDomain, nonlinear:Nonlinear):
    results = {'file': filename, 'no': get_number_from_file(filename.stem), 'time': get_time_from_file(filename.stem)}
    for field in fields(general):
        results[field.name] = getattr(general, field.name)
    for field in fields(timedomain):
        results[field.name] = getattr(timedomain, field.name)
    for field in fields(frequencydomain):
        results[field.name] = getattr(frequencydomain, field.name)
    for field in fields(nonlinear):
        results[field.name] = getattr(nonlinear, field.name)
    return results

def main():
    results =[]
    for file in tqdm(Path('data/raw').glob('*.html')):
        parser = Parser(file)
        results.append(create_dataframe(file, *parser.process()))
    
    pd.DataFrame(results).to_csv('data/processed.csv')
    
if __name__ == '__main__':
    main()

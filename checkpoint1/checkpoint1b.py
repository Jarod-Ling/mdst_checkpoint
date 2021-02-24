"""
Checkpoint 1b

*First complete the steps in checkpoint1a.pdf

Here you will create a script to preprocess the data given in starbucks.csv. You may want to use
a jupyter notebook or python terminal to develop your code and test each function as you go... 
you can import this file and its functions directly:

    - jupyter notebook: include the lines `%autoreload 2` and `import preprocess`
                        then just call preprocess.remove_percents(df) to test
                        
    - python terminal: run `from importlib import reload` and `import preprocess`
                       each time you modify this file, run `reload(preprocess)`

Once you are finished with this program, you should run `python preprocess.py` from the terminal.
This should load the data, perform preprocessing, and save the output to the data folder.

""" 
import pandas as pd
import numpy as np

def fix_str(x):
    s = ''
    if type(x) == str:
        x = x.lower()
        for i in x:
            if ((i.isalpha()) or (i.isspace())):
                s += i
    return s

def standard(x):
    s = ''
    x = x.lower()
    for i in x:
      if i =='(':
        break
      s += i
    return s

def remove_percents(df, col):
    #slice the string of each member in col up to the last character, which will be the % symbol
    df[col] = df[col].apply(lambda x: int(float(x[:-1])) if type(x) == str else x)
    return df

def fill_zero_iron(df):
    df['Iron (% DV)'] =  df['Iron (% DV)'].fillna(0)
    return df

def fix_caffeine(df):
    #df['Caffeine (mg)'] = df['Caffeine (mg)'].astype(int,errors='ignore')
    df['Caffeine (mg)'] =  df['Caffeine (mg)'].fillna("varies")
    df['Caffeine (mg)'] = df['Caffeine (mg)'].apply(lambda x: np.NaN if x.lower() == 'varies' else x)
    med = df['Caffeine (mg)'].median(skipna = True)
    df['Caffeine (mg)'] =  df['Caffeine (mg)'].fillna(med)

    return df

    #df.loc[df['Caffeine (mg)'].notna()] = df.loc[df['Caffeine (mg)'].notna()].replace('varies', np.NaN)
#def fix_caffeine(df):
   # med = df['Caffeine (mg)'].median()
    #df['Caffeine (mg)'] =  df['Caffeine (mg)'].fillna(med)
    #df['Caffeine (mg)'] =  df['Caffeine (mg)'].apply(lambda x: "k" if type(x) == str else x) 
    #return df

def standardize_names(df):
    # map standard function that takes in original iterable list of df.columns as parameter
    # now standard function will convert the names and return the new name
    # map will return new name for each column, now we convert it into a list of strings
    # Usage: map(function, iterable that is passed in as parameter for the function)
    df.columns = list(map(standard, df.columns))
    return df

def fix_strings(df, col):
    df[col] = df[col].apply(fix_str)
    return df


def main():
    
    # first, read in the raw data
    df = pd.read_csv('../data/starbucks.csv')
    
    # the columns below represent percent daily value and are stored as strings with a percent sign, e.g. '0%'
    # complete the remove_percents function to remove the percent symbol and convert the columns to a numeric type
    pct_DV = ['Vitamin A (% DV)', 'Vitamin C (% DV)', 'Calcium (% DV)', 'Iron (% DV)']
    for col in pct_DV:
        df = remove_percents(df, col)
    
    # the column 'Iron (% DV)' has missing values when the drink has no iron
    # complete the fill_zero_iron function to fix this
    df = fill_zero_iron(df)

    # the column 'Caffeine (mg)' has some missing values and some 'varies' values
    # complete the fix_caffeine function to deal with these values
    # note: you may choose to fill in the values with the mean/median, or drop those values, etc.
    df = fix_caffeine(df)
    
    # the columns below are string columns... starbucks being starbucks there are some fancy characters and symbols in their names
    # complete the fix_strings function to convert these strings to lowercase and remove non-alphabet characters
    names = ['Beverage_category', 'Beverage']
    for col in names:
        df = fix_strings(df, col)
    
    # the column names in this data are clear but inconsistent
    # complete the standardize_names function to convert all column names to lower case and remove the units (in parentheses)
    df = standardize_names(df)
    
    # now that the data is all clean, save your output to the `data` folder as 'starbucks_clean.csv'
    # you will use this file in checkpoint 2
    
    df.to_csv('../data/starbucks_clean.csv')
    

if __name__ == "__main__":
    main()

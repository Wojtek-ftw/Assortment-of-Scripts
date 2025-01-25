"""
file: secret_message.py
author: Wojciech Zacherek
1) Inputs arguments from user using the argparse library. This lib adds a help menu, description of arguments, and other safeguards to the UI side of things.
2) Download the table. I originally used the requests API and searched manually. Eventually, I got to the table aspect and recalled that pandas had a html import function, so I switched over.
3) Processing the table. Mainly involved selecting the first table that pandas generates in a list.
4) Populate spaces. The provided table assumes spaces as necessary, so I had to manually fill in the spaces.
5) Output. Displays text to screen, with optional html output.
Example usage: python secret_message.py --url https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub --output visualized.html
"""
from typing import List, Optional
import pandas as pd
import argparse

def download(url) -> pd.DataFrame:
    table = pd.read_html(url,  encoding='UTF-8')
    return table

def processing_table(table: pd.DataFrame) -> pd.DataFrame:
    table = table[0]
    table = pd.DataFrame(table.values[1:],columns=table.values[0])    
    return table

def populate_spaces(table: pd.DataFrame) -> pd.DataFrame:
    table['x-coordinate'] = table['x-coordinate'].astype(int)
    table['y-coordinate'] = table['y-coordinate'].astype(int)
    x_min = table['x-coordinate'].min()
    x_max = table['x-coordinate'].max()
    y_min = table['y-coordinate'].min()
    y_max = table['y-coordinate'].max()

    full_table = pd.DataFrame(' ', index=range(y_min, y_max + 1), columns=range(x_min, x_max + 1))
    for _, row in table.iterrows():
        full_table.at[row['y-coordinate'], row['x-coordinate']] = row['Character']
    return full_table

def generate_output(full_table: pd.DataFrame, output: Optional[str] = None):
    if output: full_table.to_html(output)
    for _, row in full_table.iterrows():
        print(repr(''.join(row.values)))

def arguments(cli_args: Optional[List] = None):
    ap = argparse.ArgumentParser(
        prog="Secret Message Decoder",
        description="Decodes a secret message from a given google docs URL"
    )
    ap.add_argument("--url", action='store',required=True, help="URL to be read from.")
    ap.add_argument("--output", action='store', default=None,required=False, help="Filepath to output generated text to html.")

    if cli_args: args = ap.parse_args(cli_args)
    else: args = ap.parse_args()
    return args

def main(cli_args: Optional[List] = None):
    args = arguments(cli_args)
    table = download(args.url)
    table = processing_table(table)
    table = populate_spaces(table)
    generate_output(table, args.output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import csv
import requests
import argparse
import time
import sys
from tqdm import tqdm


if __name__ == '__main__':
    # Read args, open file handles and iterators
    parser = argparse.ArgumentParser(description='Pull bulk prices from Scryfall.')
    parser.add_argument('-i', '--input-file', type=str, default='cards.csv',
                        help='Path to csv containing list of cards.')
    parser.add_argument('-o', '--output-file', type=str, default='cards_priced.csv',
                        help='Path to csv containing list of cards.')
    args = parser.parse_args()

    input_file = open(args.input_file, 'r')
    output_file = open(args.output_file, 'w')

    cards_reader = csv.reader(input_file, delimiter=',', quotechar='"')
    cards_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    # Count rows for progress bar
    n_cards = sum(1 for line in open(args.input_file, 'r')) - 1  
    
    # Copy header and add price column
    header = next(cards_reader)
    cards_writer.writerow(header + ['price'])

    with tqdm(total=n_cards) as pbar:
        for card in cards_reader:
            # Fetch price for data rows
            payload = {"exact": card[0]}

            # Look for set
            if not card[1]:
                payload.update({"set": card[1]})

            r = requests.get('https://api.scryfall.com/cards/named', params=payload).json()
            pbar.update(1)

            if r['object'] == 'error':
                tqdm.write('Card "{}" not found!'.format(card[0]), file=sys.stderr)
                continue

            if card[2] and (str.lower(card[2]) in ['t', 'true', '1']):
                # Foil price
                cards_writer.writerow(card + [r['prices']['usd_foil']])
            else:
                # Regular price
                cards_writer.writerow(card + [r['prices']['usd']])

            time.sleep(0.1)  # 10 RPS, per https://scryfall.com/docs/api

    input_file.close()
    output_file.close()

#!/usr/bin/env python3

import csv
import requests
import os
import argparse
import time


if __name__ == '__main__':
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

    header = True
    for card in cards_reader:
        # Write out header for first row
        if header:
            cards_writer.writerow(card + ['price'])
            header = False
        
        # Fetch price for data rows
        else:
            payload = {"exact": card[0]}
            # Look for set
            if not card[1]:
                payload.update({"set": card[1]})

            r = requests.get('https://api.scryfall.com/cards/named', params=payload).json()
            if not card[2] and (str.lower(card[2]) == "t" or str.lower(card[2]) == "true"):
                # Foil price
                cards_writer.writerow(card + [r['prices']['usd_foil']])
            else:
                # Regular price
                cards_writer.writerow(card + [r['prices']['usd']])

            time.sleep(0.1)  # 10 RPS, per https://scryfall.com/docs/api

    input_file.close()
    output_file.close()

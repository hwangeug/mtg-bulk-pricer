# Magic: the Gathering Bulk Pricing Script

Gets prices for a CSV list of Magic: the Gathering cards.  CSV must contain the following columns, in order, as the first three columns:

- Exact card name
- Set (if empty, the first Scryfall result will be used)
- Indicator whether it is foil ("t", "true", and 1 all indicate that the card is foil, any other value including empty means not foil)

Any additional columns may be added after these three.  The script will append a column labeled `price`.

Usage:

`./pricer.py -i cards.csv -o cards_priced.csv`

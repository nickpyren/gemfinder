from argparse import ArgumentParser
from csv import reader

from models.gem import Gem

# Arguments
arg_parser = ArgumentParser()
arg_parser.add_argument("-s", "--source_file", required=False, dest="source_file", help="A file containing a database of gems and their sources.", default="./poe-gem-vendor-list-3.13.csv")
arg_parser.add_argument("-i", "--input_file", required=True, dest="input_file", help="A file containing a list of gems to look for.")
args = arg_parser.parse_args()

# Build list of gems
def get_gem_from_csv_line(csv_line) -> Gem:
    return Gem(
        name=csv_line[0],
        source=f"{csv_line[1]} - {csv_line[9]}"
    )
with open(args.source_file) as source_file:
    csv_lines = reader(source_file)
    gem_list = list(map(get_gem_from_csv_line, csv_lines))
gem_dictionary = { gem.name.lower(): gem for gem in gem_list }

# Look through list of gems for provided gems and assemble the ones we want
desired_gems = []
with open(args.input_file) as input_file:
    for line in input_file:
        lower_case_line = line.strip().lower()
        if lower_case_line in gem_dictionary:
            gem = gem_dictionary[lower_case_line]
            desired_gems.append(gem)

# sort the list by act and print
sort_key_function = lambda gem: gem.source
desired_gems.sort(key=sort_key_function)
for gem in desired_gems:
    print(f"{gem.name} - {gem.source}")

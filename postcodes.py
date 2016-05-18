from argparse import ArgumentParser
from location import *
import csv

def parse_args():
    """ Read arguments from command line."""

    parser = ArgumentParser(
        description="Adding postcodes."
    )
    parser.add_argument(
        '--input_file',
        type=str,
        help='Old results without postcodes.'
    )
    parser.add_argument(
        '--output_file',
        type=str,
        help='Output file with new results including postcodes.'
    )
    return parser.parse_args()

def read_postcodes():
    sla = list(csv.reader(open("./data/sla.csv"), delimiter='\t'))
    sla_postcodes = {}
    
    for s in sla:
        if s[1] in sla_postcodes:
            sla_postcodes[s[1]].append(s[0])
        else:
            sla_postcodes[s[1]] = [s[0]]
            
    return sla_postcodes

def write_result(args, postcodes):
    violence = list(csv.reader(open(args.input_file)))
    
    with open(args.output_file, 'w') as result_file:
        result_file.write("SLA,Tweets per 1000 Population,Score,Score (Log Scale),Postcodes\n")
        
        for i, v in enumerate(violence):
            if i != 0:
                result_file.write("{0},{1},{2},{3},{4}\n".format(v[0], v[1], v[2], v[3], postcodes[v[0]]))

def main():
    args = parse_args()
    postcodes = read_postcodes()
    write_result(args, postcodes)
    
if __name__ == '__main__':
    main()

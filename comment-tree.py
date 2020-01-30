#!/usr/bin/python3

import argparse
import json
import sys
import select


def parse_args():
    '''
    Parse command line arguments.

    Returns:
        argparse.Namespace: Command line arguments
    '''

    parser = argparse.ArgumentParser(
        description='Get comments for you JSON file')

    parser.add_argument('--file', type=str,
                        help='input JSON filename')

    return parser.parse_args()


def get_json_data(filename):
    '''
    Get JSON data from any stdin source.

    Can either provide data via pipe:
    $ cat ./test/test.json | ./comment-tree.py
    or via command line argument:
    $ ./comment-tree.py --file ./test/test.json

    We check if there is stdin data by using select. That, unfortunately, only
    works on *nix machines and looks very ugly.

    Args:
        filename (str): Name of a JSON file.

    Returns:
        dict: A JSON file represented in a Python dictionary.
    '''
    if filename:
        with open(filename) as json_file:
            try:
                json_data = json.load(json_file)
                return json_data
            except:
                print(f"Could not read any JSON data from '{filename}'!")
                return None

    elif select.select([sys.stdin, ], [], [], 0.0)[0]:
        try:
            json_data = json.load(sys.stdin)
            return json_data
        except:
            print('Could not read any JSON data from stdin!')
            return None

    else:
        print(f"No input data was provided! Check '{sys.argv[0]} --help'")
        return None


def main():
    args = parse_args()

    json_data = get_json_data(args.file)
    if not json_data:
        exit(-1)


if __name__ == "__main__":
    main()

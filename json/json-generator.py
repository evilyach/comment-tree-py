#!/usr/bin/python3

import argparse
import json
import random


def generate_list(count):
    ''' Generate a list which contains needed info '''

    obj = []

    for _ in range(count):
        obj.append({
            'id': random.randint(1, 100),
            'replies': generate_list(random.randint(0, 2))
        })

    return obj


def generate_json():
    ''' Generate JSON for testing Comment Tree app '''

    return {
        'id': random.randint(1, 100),
        'replies': generate_list(random.randint(1, 2))
    }


def parse_args():
    ''' Parse command line arguments '''

    parser = argparse.ArgumentParser(
        description='Generate a JSON file to test Comment Tree App on')

    parser.add_argument('--filename', type=str,
                        help='JSON file name')

    return parser.parse_args()


def main():
    ''' Entry point of an app '''

    args = parse_args()

    if args.filename:
        with open(args.filename if args.filename else 'test.json', "w") as json_file:
            json.dump(generate_json(), json_file, indent=2)
    else:
        print(json.dumps(generate_json(), indent=2))


if __name__ == "__main__":
    main()

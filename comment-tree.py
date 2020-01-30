#!/usr/bin/python3

import argparse
import json
import sys
import select
import requests


class CommentTree:
    ''' Class to add comments to an existing JSON file. '''

    def __init__(self, filename):
        '''
        Object constructor.

        Args:
            filename (str): Name of a JSON file.

        Attributes:
            filename (str): Name of a JSON file.
            json_data (dict): A JSON file represented in a Python dictionary.
            bodies (list): List of bodies lists [id, body].
        '''

        self.filename = filename
        self.json_data = self.get_json_data(self.filename)

        self.bodies = []
        self.get_comment_bodies(self.json_data)

    def __repr__(self):
        ''' Returns representation of a Comment Tree '''

        return json.dumps(self.json_data)

    def __str__(self):
        ''' Returns string representation of a Comment Tree '''

        return json.dumps(self.json_data)

    def get_json_data(self, filename):
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

    def get_comment_bodies(self, data):
        '''
        Get a list of comment bodies.

        It works by iterating through the JSON tree and retrieving data using
        JSON placeholder API.

        Args:
            data (dict): A JSON represented in a Python dictionary.
        '''

        for key, value in data.items():
            if key == 'replies':
                for element in value:
                    self.get_comment_bodies(element)
            if key == 'id':
                req = requests.get(
                    f'https://jsonplaceholder.typicode.com/posts/{value}')
                self.bodies.append([value, req.json()['body']])


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


def main():
    ''' Entry point of an app '''

    args = parse_args()

    comment_tree = CommentTree(args.file)
    print(comment_tree)


if __name__ == "__main__":
    main()

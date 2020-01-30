#!/usr/bin/python3

import argparse
import json
import sys
import select
import grequests
import copy


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
            bodies (list): A list of comment bodies.
        '''

        self.filename = filename
        self.json_data = self.get_json_data(self.filename)
        self.bodies = {}
        self.add_comments(self.json_data)

    def __str__(self):
        ''' Returns string representation of a Comment Tree '''

        return json.dumps(self.json_data, indent=4)

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

        # This select is the only way I found to check if stdin is empty or not
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

    def async_requests(self, urls):
        '''
        Send GET-requests to a list of URLs asynchronously.

        Args:
            urls (list): a list of URLs to send requests to.
        '''

        rs = (grequests.get(url) for url in urls)
        requests = grequests.map(rs)

        for response in requests:
            self.bodies[response.json()['id']] = response.json()['body']

    def add_comments(self, data):
        '''
        Add comment bodies to a JSON dict.

        It works by iterating through the JSON tree and retrieving data using
        JSON placeholder API.

        Args:
            data (dict): A JSON represented in a Python dictionary.
        '''

        # A list of URLs to request from
        urls = []

        # The first run is to get the indeces for URLs
        for key, value in data.items():
            if key == 'id':
                urls.append(
                    f'https://jsonplaceholder.typicode.com/posts/{value}')

            if key == 'replies':
                for element in value:
                    self.add_comments(element)

        self.async_requests(urls)

        # The second run is to add comment bodies
        for key, value in data.copy().items():
            if key == 'id':
                data['body'] = self.bodies[value]

            if key == 'replies':
                for element in value:
                    self.add_comments(element)


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
    parser.add_argument('--save', type=str,
                        help='output JSON filename')

    return parser.parse_args()


def main():
    ''' Entry point of an app '''

    args = parse_args()

    comment_tree = CommentTree(args.file)

    if (args.save):
        with open(args.save, "w+") as json_file:
            json_file.write(str(comment_tree))
    else:
        print(comment_tree)


if __name__ == "__main__":
    main()

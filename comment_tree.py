#!/usr/bin/python3

import argparse
import json
import sys
import select
import aiohttp
import asyncio
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
            bodies (dict): A dictionary of comment bodies.
            urls (list<str>): A list of URLs
        '''

        self.filename = filename

        self.json_data = self.get_json_data(self.filename)

        if self.json_data is None:
            return

        self.bodies = {}
        self.urls = []

        self.process(self.json_data)

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

    def get_urls(self, data):
        '''
        Iterate through a JSON tree and get id values to form a URLs list.

        Args:
            data (dict): a JSON tree to get id values from.
        '''

        for key, value in data.items():
            if key == 'id':
                self.urls.append(
                    f'https://jsonplaceholder.typicode.com/posts/{value}')

            if key == 'replies':
                for element in value:
                    self.get_urls(element)

    def add_comments(self, data):
        '''
        Iterate through a JSON tree and put comment bodies into it.

        Args:
            data (dict): a JSON tree to put comment bodies into.
        '''

        for key, value in data.copy().items():
            if key == 'id':
                if self.bodies[value]:
                    data['body'] = self.bodies[value]

            if key == 'replies':
                for element in value:
                    self.add_comments(element)

    async def fetch(self, url, session):
        '''
        Fetch data from URL inside a session.

        This function only uses 'id' and 'body' fields.

        Args:
            url (str): a URL to fetch data from.
            session (aiohttp.client.ClientSession): a client session.
        '''
        async with session.get(url) as response:
            data = await response.json()
            if data:
                self.bodies[data['id']] = data['body']
            else:
                self.bodies[data['id']] = None

    async def bound_fetch(self, semaphore, url, session):
        '''
        Invokes a fetch guarded with a semaphore.

        Args:
            semaphore (asyncio.locks.Semaphore): a semaphore guard.
            url (str): a URL to fetch data from.
            session (aiohttp.client.ClientSession): a client session.
        '''

        async with semaphore:
            await self.fetch(url, session)

    async def run(self):
        ''' Builds a session which invokes asyncronous calls to fetch data. '''

        semaphore_count = 1000

        tasks = []
        semaphore = asyncio.Semaphore(semaphore_count)

        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                task = asyncio.ensure_future(
                    self.bound_fetch(semaphore, url, session))
                tasks.append(task)

            await asyncio.gather(*tasks)

    def process(self, data):
        '''
        Add comment bodies to a JSON dict.

        It works by iterating through the JSON tree and retrieving data using
        JSON placeholder API.

        Args:
            data (dict): A JSON represented in a Python dictionary.
        '''

        # The first run is to get the indeces for URLs
        self.get_urls(self.json_data)

        # Fetch URLs asynchronously
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run())
        loop.run_until_complete(future)

        # The second run is to add comment bodies
        self.add_comments(self.json_data)


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

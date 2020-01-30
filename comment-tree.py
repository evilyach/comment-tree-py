#!/usr/bin/python3

import argparse


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
    args = parse_args()


if __name__ == "__main__":
    main()

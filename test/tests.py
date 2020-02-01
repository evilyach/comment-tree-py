#!/usr/bin/python3

import unittest
import time
import os


class CommentTreePyTest(unittest.TestCase):
    ''' Comment Tree app tests '''

    def test_original_json(self):
        ''' Test the program with original input '''

        out_filename = 'test_original.json'

        try:
            command = f'./../comment-tree.py --file ./../json/samples/test.json --save {out_filename}'
            result = os.system(command)
            print(result)

            self.assertEqual(result, 0)
        finally:
            if os.path.exists(out_filename):
                os.remove(out_filename)

    def test_big_json(self):
        ''' Test the program with big input '''

        out_filename = 'test_big.json'

        try:
            command = f'./../comment-tree.py --file ./../json/samples/big.json --save {out_filename}'
            result = os.system(command)
            print(result)

            self.assertEqual(result, 0)
        finally:
            if os.path.exists(out_filename):
                os.remove(out_filename)

    def test_random_json(self):
        ''' Test the program with randomly generated input '''

        in_filename = 'test_random_input.json'
        out_filename = 'test_random_output.json'

        try:
            json_generate_command = f'./../json/json-generator.py --filename {in_filename}'
            os.system(json_generate_command)

            with open(in_filename) as f:
                print(f'\nTest JSON file is {len(f.readlines())} lines long')

            convert_command = f'./../comment-tree.py --file {in_filename} --save {out_filename}'

            start_time = time.time()
            result = os.system(convert_command)
            end_time = time.time() - start_time

            print(f'It took {end_time}s')

            self.assertEqual(result, 0)
        finally:
            if os.path.exists(in_filename):
                os.remove(in_filename)
            if os.path.exists(out_filename):
                os.remove(out_filename)

    def stress_test_original_json(self):
        ''' Test the original JSON file for some time '''

        total = 100
        successful = 0
        failed = 0

        for i in range(1, total + 1):
            command = f'./../comment-tree.py --file ./../json/samples/test.json > /dev/null 2>&1'
            result = os.system(command)

            if result == 0:
                print(f'{i}: successful')
                successful += 1
            else:
                print(f'{i}: failed')
                failed += 1

            self.assertEqual(result, 0)

        print(f'Successful runs: {successful} out of {total}')
        print(f'Failed runs: {failed} out of {total}')


if __name__ == "__main__":
    unittest.main()

# Comment Tree Py

## About
**Comment Tree Py** CLI app to add comments to a JSON concurrently using jsonplaceholder.typicode.com API.

## Command Line Interface
### Install:
```bash
$ git clone https://github.com/evilyach/comment-tree-py
```

### Run:
You can either pipe your file directly:
```bash
$ cat ./test/test.json | ./comment-tree.py
```
or via command line argument:
```bash
$ ./comment-tree.py --file ./test/test.json
```

### JSON generator:
You can generate a random JSON file that fits the use of this program by using **json-generator**:
```bash
$ ./json/json-generator.py
```
It will generate very random JSON file or you can pipe the output directrly into **comment-tree**:
```bash
$ ./json/json-generator.py | ./comment-tree.py --save my-new-file.json
```

### Tests:
**Warning**: you need to be in ./test directory!

You can run all the tests by typing:
```bash
$ ./tests.py
```

You can run each of them individually:
* **Test Original JSON**  
You can run this test agains the original JSON given in a task.
```bash
$ ./tests.py CommentTreePyTest.test_original_json
```
* **Test Big JSON**  
Big JSON is around 10000 lines long.
```bash
$ ./tests.py CommentTreePyTest.test_big_json
```
* **Test Random JSON**  
Generate a random JSON and test the program with it.
```bash
$ ./tests.py CommentTreePyTest.test_random_json
```
* **Stress Test Original JSON**  
Run the original test 100 times. Could be more, but don't want to try to DoS the service.
```bash
$ ./tests.py CommentTreePyTest.stress_test_original_json
```

## Example
For example, we have a test JSON file:
```json
{
  "id": 1,
  "replies": [
    {
      "id": 2,
      "replies": []
    },
    {
      "id": 3,
      "replies": [
        {
          "id": 4,
          "replies": []
        },
        {
          "id": 5,
          "replies": []
        }
      ]
    }
  ]
}
```

When we run:
```bash
$ cat ./test/test.json | ./comment-tree.py --save ./output.json
```

The program creates a new file called 'output.json'. It looks like this, with newly added comments:
```json
{
    "id": 1,
    "replies": [
        {
            "id": 2,
            "replies": [],
            "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
        },
        {
            "id": 3,
            "replies": [
                {
                    "id": 4,
                    "replies": [],
                    "body": "ullam et saepe reiciendis voluptatem adipisci\nsit amet autem assumenda provident rerum culpa\nquis hic commodi nesciunt rem tenetur doloremque ipsam iure\nquis sunt voluptatem rerum illo velit"
                },
                {
                    "id": 5,
                    "replies": [],
                    "body": "repudiandae veniam quaerat sunt sed\nalias aut fugiat sit autem sed est\nvoluptatem omnis possimus esse voluptatibus quis\nest aut tenetur dolor neque"
                }
            ],
            "body": "et iusto sed quo iure\nvoluptatem occaecati omnis eligendi aut ad\nvoluptatem doloribus vel accusantium quis pariatur\nmolestiae porro eius odio et labore et velit aut"
        }
    ],
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

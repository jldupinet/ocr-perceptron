# Perceptron for digit recognition

This project uses a perceptron network for digits recognition. It uses the data in `training_data.csv` to train each perceptron and then set ups a web server to listen for `POST /recognize` requests at port `:8000`.

Because single layer perceptrons are binary classifiers, the script creates and trains one perceptron for each class that needs to be recognized at startup. When it needs to recognize a character, it sends the data to each perceptron and returns the one that gets fired.

You can easily edit the data in `training_data.csv` in Excel or Numbers to add or change the recognized digits.

An example of the data contained in the training set:

| Uno | 0 | 1 | 1 | 0 | 0 |
|     | 0 | 0 | 1 | 0 | 0 |
|     | 0 | 0 | 1 | 0 | 0 |
|     | 0 | 0 | 1 | 0 | 0 |
|     | 0 | 0 | 1 | 0 | 0 |
|     | 0 | 0 | 1 | 0 | 0 |
|     | 1 | 1 | 1 | 1 | 1 |

* The first column of a class is the class name or tag
* The rest of the info is a matrix of 5x7 representing the character to be recognized
* The script supports char matrices of any size but all characters must be of the same size


## Requirements
This project depends on:
* Tornado

## Running
Run with:

```
python perceptron.py
```

And open `number_recognizer.html` with your browser



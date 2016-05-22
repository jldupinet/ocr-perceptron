import tornado.ioloop
import tornado.web
import csv
import json

# Perceptron Config TODO: obtain config from file
threshold = 0.5
learning_rate = 0.1
trained_perceptrons = {}

# Helper method to find if a csv row is empty
def is_row_empty(row):
    for i in row:
        if i != '':
            return False
    return True

# Reads a csv file and returns a dict with the class name as the key and the values
# as a 1-dimension vector (list)
# The csv has the following structure:
# 'class_name', input_1, input_2, ..., input_n
#           '', input_1, input_2, ..., input_n
def process_data(file = 'numbers.csv'):
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        data = {}
        currentClass = ''
        for row in reader:
            if is_row_empty(row):
                pass
            else:
                if row[0] != '': #new class
                    currentClass = row[0]
                    data[currentClass] = []
                elements = map(lambda x: int(x), row[1:])    
                data[currentClass].extend(elements)
    return data

# Returns the dot product between a collection of values and their weights
def dot_product(values, weights):
    return sum(value * weight for value, weight in zip(values, weights))

# Trains the perceptron using the given training_set
# The training set must be a list of tuples containing (example, desired_output)
def train(training_set):
    weights = [0] * len(training_set[0][0])
    while True:
        error_count = 0
        for input_vector, desired_output in training_set:
            # print(weights)
            result = dot_product(input_vector, weights) > threshold
            error = desired_output - result
            if error != 0:
                error_count += 1
                for index, value in enumerate(input_vector):
                    weights[index] += learning_rate * error * value
        if error_count == 0:
            break
    return weights

# Creates the training set for the given tag
# Returns a list of tuples (one tuple of (sensor_data, desired_output) for each class)
def create_training_set(tag, training_data):
    training_set = []
    for key, data in training_data.iteritems():
        training_set.append((tuple(data),1 if key == tag else 0))
    return training_set

def classify(sensor_data, perceptrons):
    for key, value in perceptrons.iteritems():
        if recognize(sensor_data, value):
            return key
    return 'Not Found!'

def recognize(sensor_data, weights):
    return dot_product(sensor_data, weights) > threshold

def create_perceptrons():
    data = process_data()
    # trained_perceptrons = {}
    # train a perceptron for each class in data
    for tag in data.iterkeys():
        trained_perceptrons[tag] = train(create_training_set(tag, data))
    # classify(data['Tres'], trained_perceptrons)

# create_perceptrons()
class MainHandler(tornado.web.RequestHandler):
    def post(self):
        sensor_data = json.loads(self.request.body)['sensor']
        result = {'result':classify(sensor_data, trained_perceptrons)}
        self.write(result)

def make_app():
    return tornado.web.Application([
        (r"/recognize", MainHandler),
    ])

if __name__ == "__main__":
    create_perceptrons()
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
        

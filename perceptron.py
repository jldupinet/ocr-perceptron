import tornado.ioloop
import tornado.web
import csv
import json

# Perceptron Config TODO: obtain config from file
threshold = 0.5
learning_rate = 0.1
trained_perceptrons = {}
verbose = True

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
def process_data(file = 'training_data.csv'):
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

# Runs recognize() on every trained perceptron and returns the first tag that results True
def classify(sensor_data, perceptrons):
    ratings = []
    for key, value in perceptrons.iteritems():
        verbose("Trying {0}".format(key))
        ratings.append((key,recognize(sensor_data,value)))
    verbose("-"*10)
    return max(ratings, key = lambda i: i[1])[0]

# Tries to recognize sensor_data through a single perceptron. It uses the threshold parameter
# to determine when it gets fired
def recognize(sensor_data, weights):
    result = dot_product(sensor_data, weights)
    verbose("output: {0} threshold: {1}".format(result, threshold))
    return result 


# Creates and begins perceptron training
def create_perceptrons():
    data = process_data()
    for tag in data.iterkeys():
        trained_perceptrons[tag] = train(create_training_set(tag, data))

def verbose(s):
    if verbose:
        print s

def init():
    print "***Starting server***"
    print "Training perceptrons..."
    create_perceptrons()
    print "Perceptrons trained!"


# Small server to listen for /recognize requests at port :8000

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
    init()
    app = make_app()
    app.listen(8000)
    print "Listening to port :8000"
    tornado.ioloop.IOLoop.current().start()
        

import random

import numpy as np
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_first_derivative(x):
    return math.exp(-x)/(1+math.exp(-x))**2

hidden = [float]*4
input = [float]*2

#first 8, input -> hidden
#last 4, hidden -> output
weights = [random.uniform(0,1)] * 12

input[0] = 0
input[1] = 0
output = 0


def net(A,B):
    global output
    for x in range(4):

        hidden[x]= A * weights[x] + B * weights[x+len(hidden)]
        output += sigmoid(hidden[x]*weights[x+(len(hidden)*2)-1])
        #print "hidden ",x," weights ",x+len(hidden)*2-1
    """
    hidden[0] = A * weights[0] + B * weights[4]
    hidden[1] = A * weights[1] + B * weights[5]
    hidden[2] = A * weights[2] + B * weights[6]
    hidden[3] = A * weights[3] + B * weights[7]
    """

    #output = sigmoid(hidden[0]) * weights[7] + sigmoid(hidden[1]) * weights[8] + sigmoid(hidden[2]) * weights[9] + sigmoid(hidden[3]) * weights[10]
    return sigmoid(output)

def trainNet(target):

    global input
    global hidden
    global weights
    output = 0

    for x in range(4):
        #print "hidden ",x," weighhts ",(x+len(hidden))
        hidden[x] = input[0] * weights[x] + input[1] * weights[x + len(hidden)]
        output += sigmoid(hidden[x]*weights[x+(len(hidden)*2)-1])
        #print "hidden ", x, " weights ", x + len(hidden) * 2 - 1

    calculated = sigmoid(output)
    error = target - calculated
    deltaOutputSum = sigmoid_first_derivative(output) * error

    hiddenCount = len(hidden)

    for x in range(4):
        weights[x+hiddenCount] = weights[x+hiddenCount] + sigmoid(hidden[x]*deltaOutputSum)
        deltaHiddenSum = deltaOutputSum* weights[x+hiddenCount] * sigmoid_first_derivative(hidden[x])
        print "weights ",x+hiddenCount
        inputValue = 0
        if(x >= 3):
            inputValue = input[1]
        else:
            inputValue = input[0]

        weights[x] = weights[x] + deltaHiddenSum * inputValue

    print calculated


def trainNetBadCode(target):

    global input
    global hidden
    global weights
    output = 0

    hidden[0] = input[0] * weights[0] + input[1] * weights[4]
    hidden[1] = input[0] * weights[1] + input[1] * weights[5]
    hidden[2] = input[0] * weights[2] + input[1] * weights[6]
    hidden[3] = input[0] * weights[3] + input[1] * weights[7]

    output = sigmoid(hidden[0])*weights[7]+sigmoid(hidden[1])*weights[8]+sigmoid(hidden[2])*weights[9]+sigmoid(hidden[3])*weights[10]
    calculated = sigmoid(output)
    error = target - calculated
    deltaOutputSum = sigmoid_first_derivative(output)*error

    weights[7] = weights[7] + sigmoid(hidden[0])*deltaOutputSum
    weights[8] = weights[8] + sigmoid(hidden[1])*deltaOutputSum
    weights[9] = weights[9] + sigmoid(hidden[2])*deltaOutputSum
    weights[10] = weights[10] + sigmoid(hidden[3])*deltaOutputSum

    #print "new weights ",weights[6],weights[7],weights[8]

    deltaHiddenSum1 = deltaOutputSum*weights[7]*sigmoid_first_derivative(hidden[0])
    deltaHiddenSum2 = deltaOutputSum*weights[8]*sigmoid_first_derivative(hidden[1])
    deltaHiddenSum3 = deltaOutputSum*weights[9]*sigmoid_first_derivative(hidden[2])
    deltaHiddenSum4 = deltaOutputSum*weights[10]*sigmoid_first_derivative(hidden[3])

    weights[0] = weights[0] + deltaHiddenSum1 * input[0]
    weights[1] = weights[1] + deltaHiddenSum2 * input[0]
    weights[2] = weights[2] + deltaHiddenSum3 * input[0]
    weights[3] = weights[3] + deltaHiddenSum4 * input[0]

    weights[4] = weights[4] + deltaHiddenSum1 * input[1]
    weights[5] = weights[5] + deltaHiddenSum2 * input[1]
    weights[6] = weights[6] + deltaHiddenSum3 * input[1]
    weights[7] = weights[7] + deltaHiddenSum4 * input[1]

    print calculated

def trainNet2Hidden(target):
    global input
    global hidden
    global weights

    hidden[0] = input[0] * weights[0] + input[1] * weights[2]
    hidden[1] = input[0] * weights[1] + input[1] * weights[3]

    output = sigmoid(hidden[0]) * weights[4] + sigmoid(hidden[1]) * weights[5]
    calculated = sigmoid(output)
    error = target - calculated
    deltaOutputSum = sigmoid_first_derivative(output) * error

    weights[4] = weights[4] + sigmoid(hidden[0]) * deltaOutputSum
    weights[5] = weights[5] + sigmoid(hidden[1]) * deltaOutputSum

    # print "new weights ",weights[6],weights[7],weights[8]

    deltaHiddenSum1 = deltaOutputSum * weights[4] * sigmoid_first_derivative(hidden[0])
    deltaHiddenSum2 = deltaOutputSum * weights[5] * sigmoid_first_derivative(hidden[1])

    weights[0] = weights[0] + deltaHiddenSum1 * input[0]
    weights[1] = weights[1] + deltaHiddenSum2 * input[0]
    weights[2] = weights[2] + deltaHiddenSum1 * input[1]
    weights[3] = weights[3] + deltaHiddenSum2 * input[1]

    print calculated

if __name__ == '__main__':


    #training 'logical AND'
    for x in range(5):

        input[0] = 1
        input[1] = 1
        #trainNet2Hidden(1)
        trainNet(0)

        input[0] = 0
        input[1] = 1
        #trainNet2Hidden(1)
        trainNet(1)

        input[0] = 1
        input[1] = 0
        #trainNet2Hidden(1)
        trainNet(1)

        input[0] = 0
        input[1] = 0
        #trainNet2Hidden(0)
        trainNet(0)

        print "================"

    print "== DEBUG =="
    print len(hidden), len(weights)
    print "== Test =="
    print "0 0 ",net(0,0)
    print "0 1 ",net(0,1)
    print "1 0 ",net(1,0)
    print "1 1 ",net(1,1)

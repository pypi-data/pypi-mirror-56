# Python 3
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

class Model:
  def __init__(self, x, y, number_of_hidden_layers=2, number_of_hidden_nodes=30, quiet=False):
    self.x = x
    self.y = y
    self.number_of_hidden_layers = number_of_hidden_layers
    self.number_of_hidden_nodes = number_of_hidden_nodes
    self.input_layer_activation_function = "tanh"
    self.hidden_layer_activation_function = "tanh"
    self.output_layer_activation_function = "tanh"

    #making a random, reproducible seed
    np.random.seed(1)

    input_shape = self.x[0].shape[0]
    output_shape = self.y[0].shape[0]

    number_of_hidden_nodes = self.number_of_hidden_nodes
    number_of_hidden_layers = self.number_of_hidden_layers

    #init the full lists of hidden plus 2 for input and output
    #weights
    self.W = [None] * (number_of_hidden_layers + 2)
    #activations
    self.A = [None] * (number_of_hidden_layers + 2)
    #deltas
    self.D = [None] * (number_of_hidden_layers + 2)

    input_layer_weights = 2 * np.random.random((input_shape,number_of_hidden_nodes)) - 1
    self.W[0] = (input_layer_weights)

    #middle
    for i in range(number_of_hidden_layers):
      i += 1
      hidden_layer_weights = 2 * np.random.random((number_of_hidden_nodes,number_of_hidden_nodes)) - 1
      self.W[i] = (hidden_layer_weights)

    #output
    output_layer_weights = 2 * np.random.random((number_of_hidden_nodes,output_shape)) - 1
    self.W[len(self.W)-1] = (output_layer_weights)

    if quiet == False:
      #show the architecture:
      print ("Network Architecture:")
      print ("----------------------------------------------------------------------------")
      total = 0
      for count, i in enumerate(self.W):
        total += (i.shape[0] * i.shape[1])
        if count == 0:
          print("Input Layer Number of Weights: " + str(i.shape[0] * i.shape[1]))
        elif count == (len(self.W)-1):
          print("Output Layer Number of Weights: " + str(i.shape[0] * i.shape[1]))
        else:
          print("Hidden Layer " + str(count) + " Number of Weights: " + str(i.shape[0] * i.shape[1]))
      print ("----------------------------------------------------------------------------")
      print("Total Number of Weights: ", total)
      print()

  #nonlin func
  def nonlin(self, x, deriv, function):
    if function == "tanh":
      t= 2 / (1 + np.exp(-2 * x)) -1
      if (deriv==True):
          dt=1-t**2
          return dt
      return t

    elif function == "sigmoid":
      if (deriv==True):
          return (x * (1-x))
      return 1/(1 + np.exp(-x))

    elif function == "leaky_relu":
      if (deriv==True):
          dx = np.ones_like(x)
          dx[x < 0] = 0.01
          return dx
      return np.where(x > 0, x, x * 0.01)

  def predict(self, x):
    #forward pass
    input_layer_activation = self.nonlin(np.dot(x, self.W[0]), False, self.input_layer_activation_function)
    self.A[0] = (input_layer_activation)

    for i in range(self.number_of_hidden_layers):
      i += 1
      hidden_layer_activation = self.nonlin(np.dot(self.A[i-1], self.W[i]), False, self.hidden_layer_activation_function)

    output_layer_activation = self.nonlin(np.dot(hidden_layer_activation, self.W[len(self.W)-1]), False,  self.output_layer_activation_function)
    print()
    print("Prediction:")
    return output_layer_activation


  #training
  def train(self, loss_function, epochs, alpha=0.001):
    for j in range(epochs):

        #forward pass
        input_layer_activation = self.nonlin(np.dot(self.x, self.W[0]), False, self.input_layer_activation_function)
        self.A[0] = (input_layer_activation)

        for i in range(self.number_of_hidden_layers):
          i += 1
          hidden_layer_activation = self.nonlin(np.dot(self.A[i-1], self.W[i]), False, self.hidden_layer_activation_function)
          self.A[i] = (hidden_layer_activation)

        output_layer_activation = self.nonlin(np.dot(hidden_layer_activation, self.W[len(self.W)-1]), False,  self.output_layer_activation_function)
        self.A[len(self.A)-1] = (output_layer_activation)

        #choose error in compile
        #so output_layer_activation is the prediction!!!
        if loss_function == "mse":
          error = (self.y - output_layer_activation) **2
        if loss_function == "mae":
          error = np.abs(self.y - output_layer_activation)
        if loss_function == "cce":
          output_layer_activation = np.clip(output_layer_activation, 1e-12, 1. - 1e-12)
          total_number = output_layer_activation.shape[0]
          error = -np.sum(self.y*np.log(output_layer_activation+1e-9))/total_number
        else:
          error = self.y - output_layer_activation

        #print every n steps
        divis = epochs//10
        if (j % divis) == 0:
            print ('Epoch: ' + str(j+1) + ' ERROR: ' + str(np.mean(np.abs(error))))

        #backwards pass
        output_delta = error * self.nonlin(output_layer_activation, True, self.output_layer_activation_function)
        self.D[0] = output_delta

        #setting working vars
        working_delta = output_delta
        past_layer_weights = self.W[len(self.W)-1]

        for i in range(self.number_of_hidden_layers):
          working_index = i+1

          hidden_layer_activation_error = working_delta.dot(past_layer_weights.T)

          hidden_layer_activation_delta = hidden_layer_activation_error * self.nonlin(self.A[len(self.A)-working_index-1], True, self.hidden_layer_activation_function)

          self.D[working_index] = hidden_layer_activation_delta

          working_delta = hidden_layer_activation_delta
          past_layer_weights = self.W[len(self.W)-(working_index+1)]

        input_layer_activation_error = self.D[working_index].dot(self.W[working_index].T)

        input_layer_activation_delta = input_layer_activation_error * self.nonlin(input_layer_activation, True, self.input_layer_activation_function)
        self.D[working_index+1] = input_layer_activation_delta

        #update weights
        internal_alpha = alpha
        self.W[len(self.W)-1] += input_layer_activation.T.dot(self.D[0]) * internal_alpha

        for i,z in enumerate(range(self.number_of_hidden_layers,0,-1)):
          i += 1
          self.W[z] += self.A[i].T.dot(self.D[i]) * internal_alpha

        self.W[0] += self.x.T.dot(self.D[len(self.D)-1]) * internal_alpha

    #ending print out
    print()
    print("Done.")
    if (np.abs((np.mean(np.abs(error)))-1)*100) >100:
      print("Bad Training Session! Adjust Parameters.")
    print("Final Accuracy: " + str(np.abs((np.mean(np.abs(error)))-1)*100) + "%")

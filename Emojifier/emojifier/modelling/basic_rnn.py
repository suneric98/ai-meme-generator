import numpy as np
import torch
import torch.nn as nn
from torch.nn import init
import torch.optim as optim
import math
import random
import os
from pathlib import Path 
import time
from tqdm import tqdm

class RNN(nn.Module):
	def __init__(self, input_dim, h, output_dim = 2): # Add relevant parameters
		super(RNN, self).__init__()
		self.rnn = nn.RNN(input_dim, h)
		self.finalLayer = nn.Linear(h, output_dim)
		self.input_dim = input_dim
		self.hidden_dim = h
		self.output_dim =  output_dim
		self.softmax = nn.LogSoftmax()
		self.loss = nn.NLLLoss()

	def compute_Loss(self, predicted_vector, gold_label):
		return self.loss(predicted_vector, gold_label)	

	def forward(self, inputs):
		#begin code
		k = torch.sqrt(torch.Tensor([self.input_dim]))[0]
		init_hidden = - k + torch.rand(1,1,self.hidden_dim) * 2 * k
		# ebmedded = self.embedding(inputs)
		out, hidden = self.rnn(inputs, init_hidden)
		hidden = hidden.contiguous().view(-1,self.hidden_dim)
		# Remember to include the predicted unnormalized scores which should be normalized into a (log) probability distribution
		predicted_vector = self.softmax(self.finalLayer(hidden))
		return predicted_vector
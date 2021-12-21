import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.metrics import mean_squared_error
from torch.nn import functional as F

def data_window(data, sequence_length, output_var_dim, leeway):
    x = []
    y = []
    for i in range(len(data)-sequence_length-1-leeway):
        temp_x = data[i:(i+sequence_length)]
        temp_var = np.sign(data[(i+sequence_length+leeway),output_var_dim] - data[(i+sequence_length-1),output_var_dim])
        temp_y = np.array([0,1]).reshape(1,-1) if temp_var>0 else np.array([1,0]).reshape(1,-1)
        x.append(temp_x)
        y.append(temp_y)
    return np.array(x), np.array(y).reshape(-1,2)

def load_data(ticker, data_mode, test_ratio, sequence_length, leeway):
    chain_data = pd.read_pickle('../ethChainData/processed_data/'+ ticker + '_' + data_mode + '_stat_pandas_1m.pickle')
    if ticker == 'LINK' and data_mode == 'eth':
        price_data = pd.read_pickle('../priceData/data/coinbase_pandas_LINK-USD_1m_2021-11-30 16:35:00_2021-12-11 19:52:00_list.pickle')
    elif ticker == 'SHIB' and data_mode == 'eth':
        price_data = pd.read_pickle('../priceData/data/coinbase_pandas_SHIB-USD_1m_2021-11-30 17:47:00_2021-12-11 21:10:00_list.pickle')
    elif ticker == 'MKR' and data_mode == 'eth':
        price_data = pd.read_pickle('../priceData/data/coinbase_pandas_MKR-USD_1m_2021-11-30 20:40:00_2021-12-11 23:56:00_list.pickle')
    else:
        print("Price data not available, please download")
        sys.exit(1)
    data = pd.merge(chain_data, price_data, on='time')
    dataset = data.iloc[:,1:17].values
    scaler = MinMaxScaler()
    training_data = scaler.fit_transform(dataset)
    output_var_dim = 15 # close price
    x, y = data_window(training_data, sequence_length, output_var_dim, leeway)
    train_size = int(len(y)*(1-test_ratio))
    test_size = len(y) - train_size

    train_x = Variable(torch.tensor(x[:train_size])).float()
    train_y = Variable(torch.tensor(y[:train_size])).float()
    print(train_y.shape)

    test_x = Variable(torch.tensor(x[train_size:])).float()
    test_y = Variable(torch.tensor(y[train_size:])).float()

    output_scaler = MinMaxScaler()
    output_training_data = output_scaler.fit_transform(dataset[:,output_var_dim].reshape(-1,1))

    return data, train_x, train_y, test_x, test_y, scaler, output_scaler

# Here we define our model as a class
class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, -1, :])
        return out


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: LSTMpredictor.py symbol-name data-mode num-epochs")
        sys.exit(1)

    ticker = sys.argv[1]
    data_mode = sys.argv[2]
    test_ratio = 0.33
    sequence_length = 50
    leeway = 0

    data, train_x, train_y, test_x, test_y, scaler, output_scaler = load_data(ticker, data_mode, test_ratio, sequence_length, leeway)

    input_dim = 16
    hidden_dim = 64
    num_layers = 3
    output_dim = 2

    model = LSTM(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, num_layers=num_layers)

    loss_fn = torch.nn.MSELoss()

    optimiser = torch.optim.Adam(model.parameters(), lr=0.01)
    print(model)

    # Train
    num_epochs = int(sys.argv[3])
    loss_hist = np.zeros(num_epochs)

    # Number of steps to unroll
    seq_dim =sequence_length-1

    for t in range(num_epochs):

        train_y_pred = model(train_x)

        loss = loss_fn(train_y_pred, train_y)
        if t % 10 == 0 and t !=0:
            print("Epoch ", t, "MSE: ", loss.item())
        loss_hist[t] = loss.item()

        # Zero out gradient, else they will accumulate between epochs
        optimiser.zero_grad()

        # Backward pass
        loss.backward()

        # Update parameters
        optimiser.step()

    plt.plot(loss_hist, label="Training loss")
    plt.legend()
    plt.show()

    # make predictions
    test_y_pred = model(test_x)

    # calculate accuracy

    train_y_val = F.log_softmax(train_y, dim=1).argmax(dim=1)
    train_preds = F.log_softmax(train_y_pred, dim=1).argmax(dim=1)
    train_total = train_y_pred.size(0)
    train_correct = (train_preds == train_y_val).sum().item()
    train_acc = train_correct / train_total

    test_y_val = F.log_softmax(test_y, dim=1).argmax(dim=1)
    test_preds = F.log_softmax(test_y_pred, dim=1).argmax(dim=1)
    test_total = test_y_pred.size(0)
    test_correct = (test_preds == test_y_val).sum().item()
    test_acc = test_correct / test_total


    print('Train accuracy: %.2f ' % (train_acc))
    print('Test accuracy: %.2f ' % (test_acc))

    torch.save(model, 'saved_models/lstm_classifier_'+ ticker + '_' + data_mode + '_' + str(num_epochs) + 'saved.pth')


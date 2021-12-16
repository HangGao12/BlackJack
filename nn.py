import torch as tr
import matplotlib.pyplot as pt
import exist_data as ed

w = tr.randn(2, requires_grad=True)
b = tr.randn(1, requires_grad=True)


def sigmoid(a):
    return (tr.exp(-a) + 1) ** (-1)


def net(x):
    return sigmoid((w * x).sum() + b)


def loss(x, target):
    y = net(x)
    return tr.sum((y - target) ** 2)  # --------------


η = 0.000000005  # learning rate eta


class Linear:
    def __init__(self, in_features, out_features):
        self.weight = tr.randn(in_features, out_features, requires_grad=True)
        self.bias = tr.randn(1, out_features, requires_grad=True)

    def parameters(self):
        return [self.weight, self.bias]

    def __call__(self, x):
        return tr.mm(x, self.weight) + self.bias


class Linear(tr.nn.Module):
    def __init__(self, in_features, out_features):
        super(Linear, self).__init__()
        self.weight = tr.randn(in_features, out_features, requires_grad=True)
        self.bias = tr.randn(1, out_features, requires_grad=True)

    def parameters(self):
        return [self.weight, self.bias]

    def forward(self, x):
        return tr.mm(x, self.weight) + self.bias


# MSE loss (sum instead of defaulting to mean)
loss = tr.nn.MSELoss(reduction='sum')

HEARTS, CLUBS, SPADES, DIAMONDS = 0, 1, 2, 3


def state_tensor(cards):
    # cards == [..., (suit, number), ...]
    state = tr.zeros((4, 13))
    for (suit, number) in cards:
        state[suit, number - 1] = 1.
    state = state.reshape(4 * 13)  # unwrap into a long vector
    return state


data = ed.data_collected()
data1 = ed.data_collected1()

inputs = tr.stack([state_tensor(hand) for (hand, _) in data])
targets = tr.tensor([score for (_, score) in data]).reshape(-1, 1)
inputs1 = tr.stack([state_tensor(hand) for (hand, _) in data1])
targets1 = tr.tensor([score for (_, score) in data1]).reshape(-1, 1)
cardnet = tr.nn.Sequential(
    tr.nn.Linear(inputs.shape[1], inputs.shape[0]),
    tr.nn.Sigmoid(),
    tr.nn.Linear(targets.shape[0], targets.shape[1])
)

# Stochastic gradient descent optimizer
sgd = tr.optim.SGD(cardnet.parameters(), lr=η)

# Track the change in loss during training
learning_curve = []
learning_curve1 = []
# exammples: c = float(cardnet(state_tensor([(HEARTS, 10), (CLUBS, 8)]))) -----------------------------------

# 如何获得utility: outputs = cardnet(inputs) inputs = state_tensor(hand) hand为手里的牌，一个list ----------------------------------

# Repeatedly take steps in the gradient direction
for step in range(500):

    # Accumulate loss and its gradient over all examples
    outputs = cardnet(inputs)

    batch_loss = loss(outputs, targets)

    if batch_loss < 0.000001: break

    batch_loss.backward()

    # Save loss history
    #learning_curve.append(batch_loss.item())
#------------------
    with tr.no_grad():
        outputs1 = cardnet(inputs1)

        batch_loss1 = loss(outputs1, targets1)

        if batch_loss1 < 0.000001: break

        #batch_loss1.backward()

        # Save loss history
        #learning_curve1.append(batch_loss1.item())
#--------
    # Take gradient descent step
    sgd.step()

    # zero out gradients for torch before next step
    sgd.zero_grad()

    # print progress updates
    if step % 100 == 0: print("%d: %f, %f" % (step, batch_loss, batch_loss1))
    learning_curve.append(batch_loss.item())
    learning_curve1.append(batch_loss1.item())

pt.plot(learning_curve, 'b-')
pt.plot(learning_curve1, 'r-')
pt.xlabel("Gradient descent steps")
pt.ylabel("Batch Loss")
pt.legend(["Train", "Test"])
pt.show()

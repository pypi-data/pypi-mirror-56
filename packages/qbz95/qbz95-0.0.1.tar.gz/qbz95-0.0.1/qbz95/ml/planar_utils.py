import matplotlib.pyplot as plt
import numpy as np
import sklearn
import sklearn.datasets
import sklearn.linear_model
import sklearn.model_selection
import h5py
import scipy.io


# def plot_decision_boundary(model, X, y):
#     # Set min and max values and give it some padding
#     x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
#     y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
#     h = 0.01
#     # Generate a grid of points with distance h between them
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
#     # Predict the function value for the whole grid
#     Z = model(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     # Plot the contour and training examples
#     plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
#     plt.ylabel('x2')
#     plt.xlabel('x1')
#     plt.scatter(X[0, :], X[1, :], c=y[0, :], cmap=plt.cm.Spectral)


# def plot_decision_boundary(model, X, y):
#     # Set min and max values and give it some padding
#     x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
#     y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
#     h = 0.01
#     # Generate a grid of points with distance h between them
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
#     # Predict the function value for the whole grid
#     Z = model(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     # Plot the contour and training examples
#     plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
#     plt.ylabel('x2')
#     plt.xlabel('x1')
#     plt.scatter(X[0, :], X[1, :], c=y[0, :], cmap=plt.cm.Spectral)
#     plt.show()

# Helper function to plot a decision boundary.
# If you don't fully understand this function don't worry, it just generates the contour plot below.
# def plot_decision_boundary(pred_func, X, y):
#     # Set min and max values and give it some padding
#     x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
#     y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
#     h = 0.01
#     # Generate a grid of points with distance h between them
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
#     # Predict the function value for the whole gid
#     Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#     # Plot the contour and training examples
#     plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
#     plt.scatter(X[:, 0], X[:, 1], c=y[0, :], cmap=plt.cm.Spectral)

def map_feature(X, degree=2):
    '''
    generate the composition of features of X.
    :param X:
    :param degree:
    :return:
    '''
    assert(X.shape[0]<=2)
    if X.shape[0]==2:
        x1 = X[0,:]
        x2 = X[1,:]
        m = np.sum(np.array([i+1 for i in range(1, degree+1)]))
        out = np.zeros((m, X.shape[1]))
        k = 0
        for i in range(1, degree+1):
            for j in range(0, i+1):
                out[k, :] = np.multiply(np.power(x1, i-j), np.power(x2, j))
                k = k + 1
        return out
    else:
        x1 = X[0, :]
        out = np.zeros((degree, X.shape[1]))
        for i in range(0, degree):
            out[i, :] = np.power(x1, i+1)
        return out


def plot_decision_boundary(model, X, y):
    # Set min and max values and give it some padding
    x_min, x_max = X[0, :].min() - 1, X[0, :].max() + 1
    y_min, y_max = X[1, :].min() - 1, X[1, :].max() + 1
    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the function value for the whole grid
    Z = model(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.scatter(X[0, :], X[1, :], c=y[0, :], cmap=plt.cm.Spectral)
    plt.show()


# map_feature
def plot_decision_boundary_map_feature(predictor, X, y, title="decision boundary", degree=2 ):
    plt.title(title)
    axes = plt.gca()
    min = X.min(axis=1)
    max = X.max(axis=1)
    range = max - min
    min = min - 0.1 * range
    max = max + 0.1 * range
    axes.set_xlim((min[0], max[0]))
    axes.set_ylim((min[1], max[1]))
    plot_decision_boundary(lambda x: predictor.predict(map_feature(x.T, degree)), X, y)


def load_sin_line_dataset(data_path="../../data/sin_line.txt", delimiter="\t", random_state=3, test_size=0.25):
    '''
     ex1data2.txt contains a training set of housing prices in Portland, Oregon.
     The first column is the size of the house (in square feet), the second column
     is the number of bedrooms, and the third column is the price of the house.
    :param data_path:
    :param delimiter:
    :return:
    '''
    data = np.loadtxt(data_path, delimiter=delimiter)
    X = data[:, :-1]
    y = data[:, -1:]
    train_X, test_X, train_y, test_y = sklearn.model_selection.train_test_split(
        X, y, test_size=test_size, random_state=random_state)
    return train_X.T, train_y.T, test_X.T, test_y.T


def load_flat_dataset(data_path="../../data/ex1data1.txt", delimiter=","):
    '''
     ex1data2.txt contains a training set of housing prices in Portland, Oregon.
     The first column is the size of the house (in square feet), the second column
     is the number of bedrooms, and the third column is the price of the house.
    :param data_path:
    :param delimiter:
    :return:
    '''
    data = np.loadtxt(data_path, delimiter=delimiter)
    X = data[:, :-1]
    y = data[:, -1:]
    return X.T, y.T


def load_regression_dataset(n_samples=400, n_features=1, bias=1, noise=5, random_state=3, test_size=0.25):
    X, y = sklearn.datasets.make_regression(n_samples=n_samples, n_features=n_features, n_targets=1, bias=bias,
                                            coef=False, noise=noise, random_state=random_state)
    train_X, test_X, train_y, test_y = sklearn.model_selection.train_test_split(
        X, y, test_size = test_size, random_state = random_state)
    return train_X, train_y, test_X, test_y


def load_regression_dataset_coef(n_samples=400, n_features=1, bias=1, noise=5, random_state=3, test_size=0.25, b=5):
    X, y, w = sklearn.datasets.make_regression(n_samples=n_samples, n_features=n_features, n_targets=1, bias=bias,
                                            coef=True, noise=noise, random_state=random_state)
    train_X, test_X, train_y, test_y = sklearn.model_selection.train_test_split(
        X, y, test_size = test_size, random_state = random_state)
    return train_X, train_y+b, test_X, test_y+b, w, b


def load_happy_dataset(train_data_path='../../data/train_happy.h5', test_data_path='../../data/test_happy.h5'):
    train_dataset = h5py.File(train_data_path, "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:])  # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])  # your train set labels

    test_dataset = h5py.File(test_data_path, "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])  # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])  # your test set labels

    classes = np.array(test_dataset["list_classes"][:])  # the list of classes

    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


def load_boston_dataset(test_size=0.25, random_state=3):
    '''
    -Origin
        The origin of the boston housing data is Natural.
    -Usage
        This dataset may be used for Assessment.
    -Number of Cases
        The dataset contains a total of 506 cases.
    -Order
        The order of the cases is mysterious.
    -Variables
        There are 14 attributes in each case of the dataset. They are:
            CRIM - per capita crime rate by town
            ZN - proportion of residential land zoned for lots over 25,000 sq.ft.
            INDUS - proportion of non-retail business acres per town.
            CHAS - Charles River dummy variable (1 if tract bounds river; 0 otherwise)
            NOX - nitric oxides concentration (parts per 10 million)
            RM - average number of rooms per dwelling
            AGE - proportion of owner-occupied units built prior to 1940
            DIS - weighted distances to five Boston employment centres
            RAD - index of accessibility to radial highways
            TAX - full-value property-tax rate per $10,000
            PTRATIO - pupil-teacher ratio by town
            B - 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
            LSTAT - % lower status of the population
            MEDV - Median value of owner-occupied homes in $1000's
    :return:
    '''
    boston = sklearn.datasets.load_boston()
    train_X, test_X, train_y, test_y = sklearn.model_selection.train_test_split(
        boston.data, boston.target, test_size = test_size, random_state = random_state)
    return train_X, train_y, test_X, test_y


def load_planar_dataset():
    np.random.seed(1)
    m = 400  # number of examples
    N = int(m / 2)  # number of points per class
    D = 2  # dimensionality
    X = np.zeros((m, D))  # data matrix where each row is a single example
    Y = np.zeros((m, 1), dtype='uint8')  # labels vector (0 for red, 1 for blue)
    a = 4  # maximum ray of the flower

    for j in range(2):
        ix = range(N * j, N * (j + 1))
        t = np.linspace(j * 3.12, (j + 1) * 3.12, N) + np.random.randn(N) * 0.2  # theta
        r = a * np.sin(4 * t) + np.random.randn(N) * 0.2  # radius
        X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
        Y[ix] = j

    X = X.T
    Y = Y.T

    return X, Y


def load_petal_dataset(num_example=400, random_state=3):
    np.random.seed(1)
    m = num_example  # number of examples
    N = int(m / 2)  # number of points per class
    D = 2  # dimensionality
    X = np.zeros((m, D))  # data matrix where each row is a single example
    Y = np.zeros((m, 1), dtype='uint8')  # labels vector (0 for red, 1 for blue)
    a = 4  # maximum ray of the flower

    for j in range(2):
        ix = range(N * j, N * (j + 1))
        t = np.linspace(j * 3.12, (j + 1) * 3.12, N) + np.random.randn(N) * 0.2  # theta
        r =  np.sin(4 * t) + np.random.randn(N) * 0.2 /a # radius
        X[ix] = np.c_[r * np.sin(t), r * np.cos(t)]
        Y[ix] = j


    train_X, test_X, train_y, test_y = sklearn.model_selection.train_test_split(
        X, Y, test_size=0.25, random_state=random_state)

    return train_X.T, train_y.T, test_X.T, test_y.T


def load_extra_datasets():
    N = 200
    noisy_circles = sklearn.datasets.make_circles(n_samples=N, factor=.5, noise=.3)
    noisy_moons = sklearn.datasets.make_moons(n_samples=N, noise=.2)
    blobs = sklearn.datasets.make_blobs(n_samples=N, random_state=5, n_features=2, centers=6)
    gaussian_quantiles = sklearn.datasets.make_gaussian_quantiles(mean=None, cov=0.5, n_samples=N, n_features=2,
                                                                  n_classes=2, shuffle=True, random_state=None)
    no_structure = np.random.rand(N, 2), np.random.rand(N, 2)

    return noisy_circles, noisy_moons, blobs, gaussian_quantiles, no_structure


def load_dataset():
    np.random.seed(1)
    train_X, train_Y = sklearn.datasets.make_circles(n_samples=300, noise=.05)
    np.random.seed(2)
    test_X, test_Y = sklearn.datasets.make_circles(n_samples=100, noise=.05)
    # Visualize the data
    plt.scatter(train_X[:, 0], train_X[:, 1], c=train_Y, s=40, cmap=plt.cm.Spectral);
    train_X = train_X.T
    train_Y = train_Y.reshape((1, train_Y.shape[0]))
    test_X = test_X.T
    test_Y = test_Y.reshape((1, test_Y.shape[0]))
    return train_X, train_Y, test_X, test_Y


def load_circle_dataset(n_train=300, seed_train=1, noise_train=0.05, n_test=100, seed_test=2, noise_test=0.05):
    np.random.seed(seed_train)
    train_X, train_Y = sklearn.datasets.make_circles(n_samples=n_train, noise=noise_train)
    np.random.seed(seed_test)
    test_X, test_Y = sklearn.datasets.make_circles(n_samples=n_test, noise=noise_test)
    train_X = train_X.T
    train_Y = train_Y.reshape((1, train_Y.shape[0]))
    test_X = test_X.T
    test_Y = test_Y.reshape((1, test_Y.shape[0]))
    return train_X, train_Y, test_X, test_Y


def load_image_data(train_data_path='../../data/train_catvnoncat.h5', test_data_path='../../data/test_catvnoncat.h5'):

    print('load ' + train_data_path)
    train_dataset = h5py.File(train_data_path, "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:])  # your train set features
    train_set_y_orig = np.array(train_dataset["train_set_y"][:])  # your train set labels

    print('load ' + test_data_path)
    test_dataset = h5py.File(test_data_path, "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:])  # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:])  # your test set labels

    classes = np.array(test_dataset["list_classes"][:])  # the list of classes

    train_set_y_orig = train_set_y_orig.reshape((train_set_y_orig.shape[0], 1))
    test_set_y_orig = test_set_y_orig.reshape((test_set_y_orig.shape[0], 1))

    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes


def initialize_image_data(X, y=None):
    m = X.shape[0]
    X = X.reshape((m, -1)).T
    if y is not None: y = y.T
    return X/255.0, y


def load_moon_dataset():
    np.random.seed(3)
    train_X, train_Y = sklearn.datasets.make_moons(n_samples=300, noise=.2)  # 300 #0.2
    # Visualize the data

    train_X = train_X.T
    train_Y = train_Y.reshape((1, train_Y.shape[0]))

    return train_X, train_Y


def load_football_dataset(file_path='../../data/football.mat'):
    data = scipy.io.loadmat(file_path)
    train_X = data['X'].T
    train_Y = data['y'].T
    test_X = data['Xval'].T
    test_Y = data['yval'].T

    return train_X, train_Y, test_X, test_Y


if __name__ == "__main__":
    # load_image_data()
    # load_football_dataset()
    # load_image_data()
    # train_X, train_y, test_X, test_y = load_boston_dataset()
    # print(train_X.shape)
    # print(train_y.shape)
    # print(test_X.shape)
    # print(test_y.shape)
    train_X, train_y, test_X, test_y = load_regression_dataset()
    print(train_X.shape)
    print(train_y.shape)
    print(test_X.shape)
    print(test_y.shape)
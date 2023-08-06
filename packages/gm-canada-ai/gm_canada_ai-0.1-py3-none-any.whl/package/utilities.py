import numpy as np
import itertools
import matplotlib.pyplot as plt
import keras
from nltk import word_tokenize
from keras.layers import Dense, Conv2D, Flatten, concatenate, Dropout, \
    Activation, MaxPooling2D
from keras.utils import to_categorical


def build_CNN2D_v2(input_, filter_sizes, filters=32, embed_size=50,
                   seq_length=440):
    out_ = []
    for sz in filter_sizes:
        x = Conv2D(filters=filters,
                   kernel_size=(sz, embed_size),
                   padding='valid',
                   activation='selu',
                   strides=1)(input_)
        x = MaxPooling2D(pool_size=(seq_length - sz + 1, 1), strides=(1, 1),
                         padding='valid')(x)
        x = Flatten()(x)
        out_.append(x)

    outputs = concatenate(out_)
    return outputs


def build_CNN2D_DNN(input_, filter_sizes, filters=32, embed_size=50,
                    seq_length=440, fc_units=128, fc_drop_out=0.5):
    out_ = []
    for sz in filter_sizes:
        x = Conv2D(filters=filters,
                   kernel_size=(sz, embed_size),
                   padding='valid',
                   activation='selu',
                   strides=1)(input_)
        x = MaxPooling2D(pool_size=(seq_length - sz + 1, 1), strides=(1, 1),
                         padding='valid')(x)
        x = Flatten()(x)
        x = Dense(fc_units)(x)
        x = Dropout(fc_drop_out)(x)
        out_.append(x)
    outputs = concatenate(out_)
    return outputs


def build_DNN(input_, units, num_layers, drop_out):
    x = input_

    for layer in range(num_layers):
        x = Dense(units)(x)
        x = Dropout(drop_out)(x)
        # x = BatchNormalization()(x)
        x = Activation('relu')(x)

    return x


def top_k_accuracy(y_true, y_pred, k):
    num_data = y_true.shape[0]
    correct = 0
    for i in range(num_data):
        actual = np.argmax(y_true[i, :])
        pred = y_pred[i, :].argsort()[-k:][::-1]
        if actual in pred:
            correct += 1

    return correct / num_data * 100


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def plot_matrix(cm, upper_thresholds, lower_thresholds,
                title='matrix', x_label='x', y_label='y',
                cmap=plt.cm.Blues):
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks_upper = np.arange(len(upper_thresholds))
    tick_marks_lower = np.arange(len(lower_thresholds))
    plt.yticks(tick_marks_upper, upper_thresholds.round(2), rotation=45)
    plt.xticks(tick_marks_lower, lower_thresholds.round(2), rotation=45)
    thresh = cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel(y_label)
    plt.xlabel(x_label)


def remove_redundancy(words):
    words = word_tokenize(words)
    prev_word = 'x'
    for i, word in enumerate(words):
        if word == prev_word:
            words.pop(i)

        prev_word = word

    return " ".join(words)


def get_dup(ticket_ids, dups, dup_set, dup_ticket_id,
            count_not_in_ticket_list):
    for ticket_id, dup in zip(ticket_ids, dups):

        if dup != 0:
            dup = int(dup.split(":")[0][1:])

            if dup in ticket_ids:
                # comp_1 = components[ticket_ids == ticket_id]
                # comp_2 = components[ticket_ids == dup]
                # if comp_1 == comp_2:
                pair_temp = tuple(sorted((ticket_id, dup), reverse=True))
                dup_set.add(pair_temp)
                dup_ticket_id.add(dup)
                dup_ticket_id.add(ticket_id)

            else:
                count_not_in_ticket_list += 1

    return dup_set, dup_ticket_id, count_not_in_ticket_list


class DataGenerator(keras.utils.Sequence):
    def __init__(self, path_data, pairs, batch_size=32, dim=300, max_len=20,
                 shuffle=True):
        self.dim = dim
        self.path_data = path_data
        self.batch_size = batch_size
        self.labels = np.array(pairs['label'].values)
        self.ticket_pairs = pairs['pair_ids'].values
        self.max_len = max_len
        self.shuffle = shuffle
        self.on_epoch_end()
        # self.indexes = None

    def __len__(self):
        # return int(np.floor(len(self.ticket_pairs) / self.batch_size))
        return int(np.ceil(len(self.ticket_pairs) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[
                  index * self.batch_size:(index + 1) * self.batch_size]
        ticket_pairs_list = list(self.ticket_pairs)
        file_id_temp = [ticket_pairs_list[k] for k in indexes]
        label_temp = [self.labels[k] for k in indexes]
        x, y = self.__data_generation(file_id_temp, label_temp)
        return x, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.ticket_pairs))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, file_id_temp, label_temp):
        x = []
        ticket_temp = dict()
        ticket_temp[0] = [i[0] for i in file_id_temp]
        ticket_temp[1] = [i[1] for i in file_id_temp]

        for k in range(2):
            x_temp = np.empty((self.batch_size, self.max_len, self.dim))
            for i, ID in enumerate(ticket_temp[k]):
                with open(
                        self.path_data + 'Description/'
                        + str(ID) + '.npy', "rb"
                ) as f_temp:
                    x_temp[i, ] = np.load(f_temp)

            x.append(x_temp)

        y = np.zeros((self.batch_size, 1), dtype=int)

        for i, label in enumerate(label_temp):
            y[i] = label
        return x, to_categorical(y, num_classes=2)


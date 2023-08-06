import numpy as np
import keras


class DataGenerator(keras.utils.Sequence):
    """
    Generate data for keras training
    """
    def __init__(self, pairs, tickets,
                 batch_size=32, max_len=300, dim=300, n_classes=2, shuffle=True):
        """
        initialization
        :param pairs: data frame of ticket pairs
        :param batch_size: batch size
        :param max_len: maximun len of sentences
        :param dim: embedding dimension
        :param n_classes: number of classes
        :param shuffle: shuffle the data or not
        """
        self.max_len = max_len
        self.tickets = tickets
        self.dim = dim
        self.batch_size = batch_size
        self.pairs = pairs
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.indices = np.arange(len(self.pairs.index))
        self.on_epoch_end()

    def __len__(self):
        """
        :return: number of batches per epoch
        """
        return int(np.floor(len(self.pairs.index) / self.batch_size))

    def __getitem__(self, index):
        """
        generate one batch of data
        :param index:
        :return:
        """

        # Generate indices of the batch
        indices = self.indices[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        pair_id_temp = [self.pairs['pair_ids'][k] for k in indices]
        label_temp = [self.pairs['label'][k] for k in indices]

        # Generate data
        x, y = self.__data_generation(pair_id_temp, label_temp)

        return x, y

    def on_epoch_end(self):
        """
        Updates indexes after each epoch
        """
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __data_generation(self, pair_id_temp, label_temp):
        """

        :param ticket_id_temp:
        :return:
        """
        # Initialization
        x_temp = [np.zeros((self.batch_size, self.max_len, self.dim, 1)),
                  np.zeros((self.batch_size, self.max_len, self.dim, 1))]
        y_temp = np.zeros(self.batch_size, dtype=int)

        # Generate data
        for i, ids in enumerate(pair_id_temp):
            # # Store ticket embedding
            temp = np.copy(self.tickets['Description_Summary'].loc[self.tickets['Id'] == ids[0]].values[0])
            x_temp[0][i, :temp.shape[0], :, 0] = temp

            temp = np.copy(self.tickets['Description_Summary'].loc[self.tickets['Id'] == ids[1]].values[0])
            x_temp[1][i, :temp.shape[0], :, 0] = temp

            # # Store class
            y_temp[i] = label_temp[i]

        return x_temp, y_temp  # keras.utils.to_categorical(y_temp, num_classes=self.n_classes)

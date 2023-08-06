import keras
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Input, Dense
from keras.models import Model
from keras import regularizers
import tensorflow as tf
from sklearn import svm
import numpy as np
import pandas as pd
import os
import parameters as p
import preprocessing as pre
import tools
import random
from matplotlib import pyplot as plt


class Autoencoder:
    """ This class includes Autoencoder methods """

    def __init__(self, data = p.sample_data, new_input=p.sample_data[1,:], encoder_layers=p.encoder_layers,
                 decoder_layers=p.decoder_layers, lam=p.lam, lr=p.lr, epoch=p.epoch, batch=p.batch, optimizer_model=p.optimizer_model, verbose=p.verbose,
                 overwrite=p.overwrite, cpu_num=p.cpu_num, training_percent = p.train_percent_autoencoder,
                 fusion=p.fusion, name = 'default', element = 1):
        """
        Constructor of Autoencoder class.

        Parameters
        ----------
            data : numpy.ndarray
                2D array of Input data. Each row is a vector to be compressed.
            new_input: numpy.ndarray
                new input file to use for prediction of output
            encoder_layers: list
                Encoder layers of autoencoder, the last item is the latent (compressed) dimension
            decoder_layers: list
                Decoder layers of the autoencoder model
            lam: float
                Lambda coefficient of L2 regulizor in keras
            lr: float
                Learning rate
            epoch: int
                Epoch number of autoencoder model showing how many times back propagation will happen in the whole
                network
            batch: int
                Batch number showing how many inputs pass in each iteration. This value detemines how much RAM is used
            optimizer_model: str
                The model of optimization in the autoencoder
            verbose: bool
                Whether the loss convergence values are shown in terminal (True) or not (False)
            overwrite: bool
                Determines whether the new training data will be overwritten on the old one (True) or not (False)
            cpu_num: int
                Number of CPU used in training of the autoencoder
            training_percent: float
                Percentage of total data used for training autoencoder between 0 % and 100 %
            name : str
                name of the autoencoder.
            element: int
                Number of considered element (It's not total number of elements). Starts from 1.

        """
        self.data = data
        self.new_input = new_input
        self.encoder_layers = encoder_layers
        self.decoder_layers = decoder_layers
        self.lam = lam
        self.lr = lr
        self.epoch = epoch
        self.batch = batch
        self.optimizer_model = optimizer_model
        self.verbose = verbose
        self.overwrite = overwrite
        self.cpu_num = cpu_num
        self.training_percent = training_percent
        self.name = name
        self.fusion = fusion
        self.element = element

    def set_best_params(self):
        self.encoder_layers, self.decoder_layers, self.lam, self.lr, self.training_percent = p.best_params

    def build_layers(self):
        """
        Build encoder and decoder layers of the autoencoder model

        Returns
        -------
            input_var: tensorflow place holder
                input
            encoded: keras layers
                encoder layers
            decoded: keras layers
                decoder layers
        """
        input_dim = len(self.data[0, :])
        input_var = Input(shape=(input_dim,))
        # Encoder layers
        encoded = Dense(self.encoder_layers[0], kernel_regularizer=regularizers.l2(self.lam),
                        activation=tf.nn.relu)(input_var)
        if len(self.encoder_layers) > 2:
            for i in (self.encoder_layers[1:-1]):
                encoded = Dense(i, kernel_regularizer=regularizers.l2(self.lam),
                                activation=tf.nn.sigmoid)(encoded)
        encoded = Dense(self.encoder_layers[-1], kernel_regularizer=regularizers.l2(self.lam),
                        activation=tf.nn.relu)(encoded)
        # Decoder layers
        decoded = Dense(self.decoder_layers[0], kernel_regularizer=regularizers.l2(self.lam),
                        activation=tf.nn.relu)(encoded)
        if len(self.decoder_layers) > 2:
            for j in (self.decoder_layers[1:-1]):
                decoded = Dense(j, kernel_regularizer=regularizers.l2(self.lam),
                                activation=tf.nn.sigmoid)(decoded)
        decoded = Dense(input_dim, kernel_regularizer=regularizers.l2(self.lam),
                        activation=tf.nn.relu)(decoded)
        return input_var, encoded, decoded


    def build_models(self):
        """
        builds autoencoder and encoder models

        Returns
        -------
        autoencoder: keras model
            autoencoder model
        encoder: keras model
            encoder model
        """
        input_var, encoded, decoded = self.build_layers()
        autoencoder = Model(input_var, decoded)
        encoder = Model(input_var, encoded)
        #   Set learning rate of keras
        if self.optimizer_model == 'adam':
            keras.optimizers.Adam(lr=self.lr)
        elif self.optimizer_model == 'SGD':
            keras.optimizers.SGD(lr=self.lr, nesterov=True)
        autoencoder.compile(optimizer=self
                            .optimizer_model, loss='mean_squared_error', metrics=['accuracy'])
        return autoencoder, encoder

    def train(self):
        """
        Trains the autoencoder model.

        parameters
        ----------

        Returns
        -------
            saves the best weights found in output directory 'weights'
        """

        # saves the best weight data found in output directory
        if os.path.isfile(p.weights_file_address + 'weight_{}'.format(self.name)):
            if self.overwrite:
                os.remove(p.weights_file_address + 'weight_{}'.format(self.name))
        checkpoint = ModelCheckpoint(p.weights_file_address + 'weight_{}'.format(self.name), monitor='val_acc',
                                     verbose=0, save_best_only=False, mode='max')
        #   Reads the data
        d = pre.Data()
        d.name = self.name
        d.data = self.data
        d.training_percentage = self.training_percent
        #   Normalizes the data
        d.normalize()
        autoencoder, encoder = self.build_models()
        data_train, data_test = d.train_test()
        if p.early_stopping:
            es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)
            call_back_list = [es, checkpoint]
        else:
            call_back_list = [checkpoint]
        autoencoder.fit(data_train, data_train, epochs=self.epoch, batch_size=self.batch, shuffle=True,
                        callbacks=call_back_list, validation_data=(data_test, data_test), verbose=self.verbose)
        return

    def predict(self):
        """
        Gives reconstructed and compressed (latent) data

        Returns
        -------
        reconstructed: numpy.ndarray
            reconstructed data
        compressed: numpy.ndarray
            compressed data
        """
        self.new_input = self.data[self.element - 1, :]
        inputs = np.array([self.new_input])
        autoencoder, encoder = self.build_models()
        autoencoder.load_weights(p.weights_file_address + 'weight_{}'.format(self.name))
        reconstructed = autoencoder.predict(inputs)
        reconstructed = pre.Data(reconstructed)
        reconstructed.denormalize()
        compressed = encoder.predict(inputs)
        compressed = pre.Data(compressed)
        compressed.denormalize()
        return reconstructed.data, compressed.data

    def error(self):
        """
        Returns autoencoder error.
        [(output - input)/input] * 100  %

        Returns
        -------
            error: float
                Autoencoder mean squared error between original and recontrcuted arrays
        """
        self.new_input = self.data[self.element - 1,:]
        inputs = np.array([self.new_input])
        autoencoder, encoder = self.build_models()
        autoencoder.load_weights(p.weights_file_address + 'weight_{}'.format(self.name))

        original = pre.Data(self.new_input)
        original.name = self.name

        if p.normalize:
            original.normalize()
            initial = original.data
        else:
            initial = original.data

        reconstructed = autoencoder.predict(inputs)
        reconstructed = pre.Data(reconstructed)
        reconstructed.name = self.name
        reconstructed.data_backup = self.data

        if p.normalize:
            new = reconstructed.data[0]
        else:
            reconstructed.denormalize()
            new = reconstructed.data[0]

        err = round((np.square(initial - new)).mean(axis=0) * 100, 2)

        return err

    def compare_plot(self):
        """ plots the original and reconstructed """
        self.new_input = self.data[self.element - 1, :]
        inputs = np.array([self.new_input])
        autoencoder, encoder = self.build_models()
        autoencoder.load_weights(p.weights_file_address + 'weight_{}'.format(self.name))

        original = pre.Data(self.new_input)
        original.name = self.name
        original.normalize()

        reconstructed = autoencoder.predict(inputs)
        reconstructed = pre.Data(reconstructed)
        reconstructed.data_backup = self.data
        reconstructed.name = self.name
        reconstructed.normalize()

        x = range(len(original.data))

        plt.plot(x, original.data, label='CFD')
        plt.plot(x, reconstructed.data[0], '--', label='Autoencoder')
        plt.xlabel('Time step since beginning of solidification')
        plt.ylabel('Normalized fusion value')
        plt.legend()
        plt.savefig(p.output_dir + 'fusion_training_{}.png'.format(original.name), dpi=600)
        plt.show()
        return


class Svm:
    """ Classifier Class"""

    def __init__(self, gamma = p.gamma, c = p.c, data = [], labels=[], new_inputs = []):
        """
        Constructor of Classifier class.

        Parameters
        ----------
        gamma  : float
            C-support nonlinear SVM Parameter (Gamma)
        c : float
            C-support nonlinear SVM Parameter (C)

        -------------------------------------
        label_1 || data_11 data_12 ... data_1n
        label_2 || data_21 data_22 ... data_2n
        .   .   ||
        .   .   ||
        label_n || data_n1 data_n2 ... data_nn
        -------------------------------------
        data: np array
            the data portion of the above table

        labels: list
            list of labels equal to the labels column shown in the above table
        new_inputs: 2D np array
            new data to be classified. Note that is the input is 1D such as [a, b, c], it should be
            defined as 2D by using [[a, b, c]] in order to pass it to SVM.
            For multiple inputs [[a, b, c], [d, e, f]]
        """
        self.gamma = gamma
        self.c = c
        self.data = data
        self.labels = labels
        self.new_inputs = new_inputs

    def classify(self):
        """
        This module uses support vector machine (SVM) to classify the data

        Returns
        -------
        predicted_labels: list
            List of label predictions
        svm_err : float
            SVM average error (%)
        """
        # Import input data and labels (created by the autoencoder)

        # data_tmp = self.data
        # data_tmp = self.data[:, 1:]
        # labels = self.data[:, 0]

        # Prepare testing and training datasets

        percent_training = int(len(self.labels) * (p.train_percent_svm / 100))

        data_train = self.data[:percent_training]
        label_train = self.labels[:percent_training]
        data_test = self.data[percent_training:]
        label_test = self.labels[percent_training:]

        # SVM training function
        def classifier():
            """ Classify only one entry"""
            model = svm.SVC(gamma=self.gamma, C=self.c)
            model.fit(data_train, label_train)
            predicted_labels = model.predict(self.new_inputs)
            return predicted_labels

        def error():
            """ Test accuracy of svm"""
            """ Classify only one entry"""
            model = svm.SVC(gamma=self.gamma, C=self.c)
            model.fit(data_train, label_train)
            predicted_labels = model.predict(data_test)
            # Classification error calculation
            misclassified = np.count_nonzero(label_test - predicted_labels)
            svm_err = (misclassified / len(self.data)) * 100
            svm_err = round(svm_err, 2)
            return svm_err

        # Make predictions based on the testing latent vectors
        predicted_labels = classifier()
        return predicted_labels, error()


class RandomManipulations:
    """ Generates random parameters user by autoencoder and SVM models """

    def __init__(self, fluent_pkl_file=[], params_file=p.params_file):
        """
        Constructor of RandomManipulations class.

        Parameters:
        -----------
        fluent_pkl_file: str
            full address of fluent pickle file to be parsed and imported
        params_file: str
            full address of file with parameters generated by genetic algorithm
        """
        self.fluent_pkl_file = fluent_pkl_file
        self.params_file = params_file

    '''
    def autoencoder_layers(self):
        """
        Returns randomly generated encoder and decoder layers.

        Returns:
        -------
        encoder_layers: list
            list of encoder layers
        decoder_layers: list
            list of decoder layers
        """
        encoder_layer_num = random.randrange(, self.encoder_num_range[1])
        encoder_layers = []
        decoder_layer_num = random.randrange(self.decoder_num_range[0], self.decoder_num_range[1])
        decoder_layers = []
        for e in range(encoder_layer_num):
            encoder_layers.append(random.randrange(self.encoder_values_range[0], self.encoder_values_range[1]))
        #   Adding latent vector to encoder layers but latent dimension is constant so It's added separately
        encoder_layers.append(p.latent_dim)
        for d in range(decoder_layer_num):
            decoder_layers.append(random.randrange(self.decoder_values_range[0], self.decoder_values_range[1]))

        return encoder_layers, decoder_layers
    '''

    def find_best(self):
        """
        finds best parameters among randomly selected ones based on the file :random_autoencoder_params_error.txt
        in 'output' directory.

        Returns
        -------
        (list, list, float, float, float)
            encoder_layers (list):
                list of encoder layers
            decoder_layers (list):
                list of decoder layers
            lam (float):
                lambda coefficient of L2 regulizer in keras
            lr  (float):
                learning rate of training in keras
            train_percent (float):
                percentage of the whole data assgined for training
        """
        tool = tools.DataManipulations()
        file = pd.read_csv(self.params_file, sep='\t')
        # file = pd.read_csv(p.output_dir + 'random_autoencoder_params_error.txt', sep='\t')
        file.columns = ['encoder', 'decoder', 'lam', 'lr', 'training_percent', 'error']
        idx_min = file['error'].idxmin()
        row_with_min_err = file.iloc[idx_min].values
        encoder_layers = tool.str_to_float_bracket(row_with_min_err[0])
        decoder_layers = tool.str_to_float_bracket(row_with_min_err[1])
        lam, lr, train_percent = row_with_min_err[2:-1]
        return encoder_layers, decoder_layers, float(lam), float(lr), float(train_percent)

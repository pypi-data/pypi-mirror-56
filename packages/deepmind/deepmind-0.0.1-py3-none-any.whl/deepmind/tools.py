"""
This module includes tool methods used for autoencoder modeling.
"""
import pandas as pd
import parameters as p


class DataManipulations:
    """ Data manipulation class """
    def __init__(self, file=p.cfd_content_file_sample):
        """
        Constructor of data manipulation class.

        Parameters
        ----------
            file: str
                Full address of Pickle file including FLUENT results to be parsed
        """
        self.file = file

    def parse(self):
        """
        Reads the file written by fluent and gives back them as a format readable by the autoencoder model

        Returns
        -------
            data: numpy.ndarray
                The parsed form of FLUENT Temperature vectors ready to be imported by the autoencoder and SVM
        """
        #   Preparing data
        file = pd.read_pickle(self.file)
        #   Transpose the data so each row shows a vector for training
        file = file.T
        #   Drop null values
        file = file.dropna()
        #   Transpose and convert to numpy array
        data = file.values
        return data

    def str_to_float_bracket(self, string):
        """
        converts string of list to list of floats:
        Parameters:
            string (str): "[a, b, c, d]"
        Return:
            (list): [a, b, c, d]
        """
        list = []
        splitted = string.strip('[]').split(',')

        for i in splitted:
            try:
                list.append(float(i))
            except:
                pass

        list_new = []
        for i in range(len(list)):
            list_new.append(int(list[i]))

        return list_new
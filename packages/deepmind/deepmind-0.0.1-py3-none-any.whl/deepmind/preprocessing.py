"""
This module containts the followings:
- Data manipulation methods.
- Initializer which checks necessar files and folders before running the main module
"""

import parameters as p
import pandas as pd
import numpy as np


class Initialize:
    """ Initializes file and folders necessary """
    def __init__(self):
        pass


class Data:
    """
    This class provides data manipulation methods.
    """

    def __init__(self, data=p.sample_data, training_percentage=p.train_percent_autoencoder,
                 address=p.cfd_content_file_sample, measurements_file=p.measurements_file, dp_file=p.dp_file,
                 fusion=p.fusion, name='dafault'):
        """
        Constructor of Data class.

        Parameters:
        -----------
        data : numpy.ndarray
            input data
        fusion: list
            [a, b]: [1, 0] means only temperature is considered and [0, 1] shown only ice fraction is important.
            and the combination of these two parameters shows a fusion of temperature and ice fraction weights.
        name : str
            a name for data for plotting and so on.
        """
        self.data_backup = data
        self.data = data
        self.training_percentage = training_percentage
        self.address = address
        self.measurements_file = measurements_file
        self.dp_file = dp_file
        self.fusion = fusion
        self.name = name

    def normalize(self):
        """
        Normalizes numpy arrays

        Parameters
        ----------
        data : numpy.ndarray
            Input data to be normalized

        Returns
        ------
        numpy.ndarray
            The normalized numpy array of data.
        """
        min_data = np.min(self.data)
        max_data = np.max(self.data)
        self.data = (self.data - min_data) / (max_data - min_data)
        return self.data

    def denormalize(self):
        """
        De-Normalizes numpy arrays

        Parameters
        ----------
        data : numpy.ndarray
            Input data to be De-Normalized

        Returns
        ------
        numpy.ndarray
            The Original data (De-normalized of the normalized data).
        """
        dataset = self.data
        min_var = np.min(self.data_backup)
        max_var = np.max(self.data_backup)
        self.data = self.data * (max_var - min_var) + min_var
        return self.data

    def train_test(self):
        """
        train_test (data)


        Generates training and testing datasets from the input data.
                |label 1, a1, a2, ... , an|\n
                |label 2, b1, b2, ... , bn|\n
                |label 3, c1, c2, ... , cn|\n
                |label N, d1, d2, ... , dn|\n


        Parameters
        ----------
        data : numpy.ndarray
               2D array of Input data.


        Returns
        -------
        tuple
            training dataset (2D numpy.ndarray), testing dataset (2D numpy.ndarray)


        Example
        -------
        data:
            [[1, 2, 4, 5],\n
            [0, 4, 7, 9],\n
            [1, 2, 3, 4],\n
            [1, 9, 6, 4],\n
            [0, 7, 4, 8]]

        returns:
             [[1 2 4 5]\n
             [0 4 7 9]\n
             [1 2 3 4]\n
             [1 9 6 4]]\n
             [[0 7 4 8]]\n
        """
        percent_index = int((len(self.data[:, 0])) * (self.training_percentage / 100))
        data_train = self.data[:percent_index, :]
        data_test = self.data[percent_index:, :]
        return data_train, data_test

    def import_fluent(self):
        """
        Parses cfd results to rows of (temperature vectors, ice vectors). Each row shows temperature or ice fraction
        vectors for one element.

        Returns:
        ------
            (temperature_db, ice_db): tuple
        """
        #   Read cfd content file
        cfd_content = pd.read_pickle(self.address)

        #   Number of ts and number of elements
        cfd_content_1 = cfd_content[cfd_content['element'] == 1]
        number_of_ts = len(cfd_content_1['temperature'].values)
        number_of_elements = int(max(cfd_content['element']))
        temperature_db = np.zeros((number_of_elements, number_of_ts))
        ice_db = np.zeros((number_of_elements, number_of_ts))
        for element in range(max(cfd_content['element'])):
            cfd_content_element = cfd_content[cfd_content['element'] == element + 1]
            temperature = cfd_content_element['temperature'].values
            temperature_db[element, :] = temperature
            ice = cfd_content_element['ice'].values
            ice_db[element, :] = ice

        return temperature_db, ice_db

    def import_fluent_fusion(self):
        """
        Parses cfd results to rows of (temperature vectors, ice vectors). Each row shows temperature or ice fraction
        vectors for one element.

        Returns:
        ------
            (temperature_db, ice_db): tuple
        """
        #   Read cfd content file
        cfd_content = pd.read_pickle(self.address)

        #   Number of ts and number of elements
        cfd_content_1 = cfd_content[cfd_content['element'] == 1]
        number_of_ts = len(cfd_content_1['temperature'].values)
        number_of_elements = int(max(cfd_content['element']))
        temperature_db = np.zeros((number_of_elements, number_of_ts))
        ice_db = np.zeros((number_of_elements, number_of_ts))
        for element in range(max(cfd_content['element'])):
            cfd_content_element = cfd_content[cfd_content['element'] == element + 1]
            temperature = cfd_content_element['temperature'].values
            temperature_db[element, :] = temperature
            ice = cfd_content_element['ice'].values
            ice_db[element, :] = ice

        temp_norm = Data()
        temp_norm.data = temperature_db
        temp_norm.normalize()
        temp_norm = temp_norm.data

        self.data = self.fusion * temp_norm + self.fusion * ice_db
        return self.data

    def import_experiment(self):
        """
        Parses and imports experimental measurements


        Returns
        -------
        measurements_modified: pandas.DataFrame
            Dataframe inlcuding points where SEM images are taken and average size of pores

        Example
        -------
                    dp    r     z      size
                0    1  0.0   2.5  0.174058
                ..  ..  ...   ...       ...
                79  80  5.0   7.5  0.102814
        """
        #   Reads the file inlcuding sheets names
        file = self.measurements_file
        df = pd.ExcelFile(file)
        sheet_names = df.sheet_names
        measurements = []
        for sheet_name in sheet_names:
            number_of_wells = sheet_name.split('w')[0].split(' ')[0]
            solution_height = sheet_name.split('_')[1].split('mm')[0]
            section_height = sheet_name.split('_')[2].split('mm')[0]
            content = df.parse(sheet_name)
            #   Average pore size
            aps = content['Average Pore Size (mm)']
            center = np.average(aps[:5])
            left = np.average(aps[5:10])
            right = np.average(aps[10:15])
            measurements.append([number_of_wells, solution_height, section_height, \
                                 center, left, right])
        measurements = pd.DataFrame(measurements)
        measurements.columns = ['number_of_wells', 'solution_height', 'section_height', \
                                'center', 'left', 'right']
        measurements['side'] = (measurements['left'] + measurements['right']) / 2
        measurements = measurements.drop(columns=['number_of_wells', 'solution_height', 'left', 'right'])
        measurements = measurements.rename(columns={'section_height': 'z'})
        dps = pd.read_csv(self.dp_file)['dp'].values
        measurements['dp'] = dps
        measurements_center = measurements[['dp', 'z', 'center']]
        measurements_side = measurements[['dp', 'z', 'side']]
        measurements_center['r'] = 0
        measurements_side['r'] = 0.005
        measurements_center = measurements_center.rename(columns={'center': 'size'})
        measurements_side = measurements_side.rename(columns={'side': 'size'})
        measurements_modified = pd.concat([measurements_center, measurements_side], ignore_index=True)
        measurements_modified = measurements_modified.sort_values('dp').reset_index(drop=True)
        measurements_modified = measurements_modified[['dp', 'r', 'z', 'size']]
        measurements_modified['r'] = 1000 * measurements_modified['r']
        measurements_modified.to_pickle(p.output_dir + 'measurements.pkl')
        self.data = measurements_modified


class classification:
    '''
    This class, classifies measurement file base on pore sizes and number of classes needed.
    '''
    def __init__(self, data = [], number_of_classes = []):
        """
        parameters
        ---------
        num_of_classes: int
            number of classes desired to pore sizes

        """
        self.num_of_classes = number_of_classes
        self.data = data


    def size_ranges(self):
        '''
        Gives size ranges based on min and max pore size and number of classes to be defined

        return
        ---------
            returns a list of lists where each inside list is a sub_range for each pore size class
        '''
        global measurements
        # measurements = pd.read_pickle(p.output_dir + 'measurements.pkl')
        measurements = self.data
        size_values = measurements['size'].values
        size_range = np.linspace(min(size_values), max(size_values), self.num_of_classes + 1, endpoint=True)
        size_ranges = []
        for i in range(len(size_range) -1):
            size_ranges.append([size_range[i], size_range[i+1]])
        return size_ranges

    def size_classes(self):
        '''
        Gives size ranges based on min and max pore size and number of classes to be defined

        parameters
        ---------
        num_of_classes: int
            number of classes desired to pore sizes

        return
        ---------
            returns a list of lists where each inside list is a sub_range for each pore size class
        '''
        size_ranges_list = self.size_ranges()
        size_classes = []
        ranges = []
        for i in range(len(measurements)):
            line = measurements.iloc[i].values
            size = line[3]
            for j in range(0, len(size_ranges_list)):
                size_range_min = size_ranges_list[j][0]
                size_range_max = size_ranges_list[j][1]
                if ((size >= size_range_min) and (size < size_range_max)) or (size == size_range_max):
                    size_classes.append(j)
                    ranges.append(size_ranges_list[j])
        return size_classes, ranges

    def assign_classes(self):
        '''
        Gives size ranges based on min and max pore size and number of classes to be defined

        parameters
        ---------
        num_of_classes: int
            number of classes desired to pore sizes

        return
        ---------
            returns a list of lists where each inside list is a sub_range for each pore size class
        '''
        classes, ranges = self.size_classes()
        measurements['size classes'] = classes
        measurements['size range'] = ranges
        measurements.to_pickle(p.output_dir + 'measurements_classified.pkl')
        self.data = measurements
        return measurements
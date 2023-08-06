"""
This module includes methods for CFD results analysis:
- Read temperature and ice fraction during solidification
- Find element_number numbers corresponding to a location
"""

import parameters as p
import pandas as pd
import numpy as np
import os
import tqdm


class ReadResults:
    """
    This class handles cfd reults maniputation including parsing data and reading variables.
    """
    def __init__(self, dp=p.dp, element_number=p.index):
        """
        Constructor of Cfd class.

        Parameters
        ----------
        dp: int
            design point number
        element_number: int
            element element_number number
        """
        self.dp = dp
        self.element_number = element_number

    def read_to_numeric(self):
        """
        This function reads the pickle file containing CFD results for 'dp' and convert str values to numeric values.

        Return
        ------
        pandas.DataFrame
            cfd content of design point = dp as DataFrame of numeric values.
        """
        file = pd.read_pickle(p.cfd_content + 'contents_{}_freezing.pkl'.format(int(self.dp)))
        file = pd.read_pickle(p.sample_file_ice)
        columns = file.columns
        for column in columns:
            file[column] = pd.to_numeric(file[column])
        return file

    @property
    def num_of_el(self):
        """
        This function returns number of elements in the cfd object.

        Returns
        -------
        int
            number of elements.
        """
        file = self.read_to_numeric()
        num_of_el = max(file['element'])
        return num_of_el

    def read_solidified(self):
        """
        Reads the numeric DataFrame of cfd content of design point 'dp' and returns only the solidified part.

        Return
        ------
        pandas.DataFrame
            portion of cfd contents of design point 'dp' where solidification is in progress.
        """
        file_numeric = self.read_to_numeric()
        file_solidified = file_numeric[(file_numeric['ice'] > 0) & (file_numeric['ice'] < 1)]
        return file_solidified

    def read_min_max(self):
        """
        Reads solidification cfd results for all the elements of design point 'dp' and Calculated minimum and maximum
        time for solidification.

        Return
        ------
        tuple
            when solidification starts (float), when solidification ends (float)
        """
        file_solidified = self.read_solidified()
        min_time = min(file_solidified['time'])
        max_time = max(file_solidified['time'])
        return min_time, max_time

    def read_element(self):
        """
        Reads part of cfd content for design point 'dp' at desired element_number and during when solidification is happening
        anywhere within the solution.

        Return
        ------
        pandas.DataFrame
            Complete solidification information for during solidification happening anywhere in the solution
        """
        file = self.read_to_numeric()
        time_min, time_max = self.read_min_max()
        file_solidified_element = file[(file['element'] == self.element_number) & (file['time'] > time_min) &
                                       (file['time'] < time_max)]
        return file_solidified_element

    def read(self):
        file = self.read_to_numeric()
        number_of_elements = int(max(file['element']))
        time_min, time_max = self.read_min_max()
        number_of_timesteps = int((time_max-time_min)/0.05)
        file_solidified = file[(file['time'] > time_min) & (file['time'] < time_max)]

        total_results = pd.DataFrame()
        for t in range(number_of_timesteps):
            results = pd.DataFrame()
            for e in range(number_of_elements):
                results = results.append(file_solidified.iloc[t + e * number_of_elements])
            total_results = total_results.append(results)
            print(round((t/number_of_timesteps) * 100, 2), ' % completed')

        total_results.to_pickle(p.output_dir + 'parsed_content_dp_' + str(self.dp) + '.pkl')
        return total_results


class FindElements:
    """ This class finds elements and adjacent elements given the coordinates"""

    def __init__(self, dp=p.dp, r=p.r, z=p.z, r_n=p.r_n, z_n=p.z_n, index=p.index):
        """
        Constructor of FindElements class.

        Parameters
        -----
        dp: int
            Design Point number
        r:  float
            r-component (mm) of the solution geometry (Starts from center)
        z:  float
            z-component (mm) of the solution geometry (Starts from bottom)
        r_n:  float
            normalized r-component (between 0 and 1) of the solution geometry (Starts from center)
        z_n:  float
            normalized z-component (between 0 and 1) of the solution geometry (Starts from bottom)
        index:  int
            Index of center element_number adjacent of which are to be returned
        """
        self.r = r
        self.z = z
        self.dp = dp
        self.r_n = r_n
        self.z_n = z_n
        self.index = index

    def element_r_z(self):
        """
        Returns element_number element_number number given dp number and r,z

        Returns
        -----
        element_number:  int
            element_number element_number number for the given inputs
        """
        #   Selects the first solution file in the output folder
        path = p.cfd_content
        # file = 'temperature_dp_{}.pkl'.format(int(self.dp))
        file = 'contents_{}_freezing.pkl'.format(int(self.dp))
        #   This line is to show all the columns
        pd.set_option('display.expand_frame_repr', False)
        #   Reads the content to parse z, r coordinates associated with the elements
        content = pd.read_pickle(path + file)
        content = content[:max(content['element'])]
        # content.columns = ['element_number', 'z', 'r', 'temp', 'time', 'liquid']
        #   Calculate z, r relative to the bottom of solution and center axis
        content['z'] = (content['z'] - content['z'].min()) * 1000   # convert to mm
        content['r'] = (content['r'] - content['r'].min()) * 1000   # convert to mm
        #   calculate the distance as a new column in pandas DataFrame
        content['dz'] = abs(content['z'] - self.z)
        content['dr'] = abs(content['r'] - self.r)
        content['distance'] = np.sqrt(content['dz'] ** 2 + content['dr'] ** 2)
        #   find the element_number of min value in 'distance'
        min_index = np.where(content['distance'].values == content[
            'distance'].values.min())
        return int(min_index[0])

    def element_r_z_normalized(self):
        """
        Returns element_number element_number number given dp number and r_n,z_n (normalized coordinates)

        Returns
        -----
        element_number:  int
            element_number element_number number for the given inputs
        """
        #   Selects the first solution file in the output folder
        path = p.cfd_content
        #   This line is to show all the columns
        pd.set_option('display.expand_frame_repr', False)
        #   Reads the content to parse z, r coordinates associated with the elements
        content = pd.read_pickle(path + 'contents_{}_freezing.pkl'.format(self.dp))
        content = content[:max(content['element_number'])]
        #   calculate the distance as a new column in pandas DataFrame
        content['dz'] = content['z_n'] - self.z_n
        content['dr'] = content['r_n'] - self.r_n
        content['distance'] = np.sqrt(content['dz'] ** 2 + content['dr'] ** 2)
        #   find the element_number of min value in 'distance'
        min_index = np.where(content['distance'].values == content[
            'distance'].values.min())
        return int(min_index[0][0])

    def element_r_z_adjacent(self):
        """
        Returns adjacent element_number indexes given dp number and element_number element_number

        Returns
        -------
        adjacent_elements: list
            A list of four indexes [element_r_1, element_r_2, element_z_1, element_z_2]
            element_r_1: Index of element_number further from the center
            element_r_2: Index of element_number towards the center
            element_z_1: Index of element_number at the bottom
            element_z_2: Index of element_number on top
        """
        #   Define a tolerance for assuming two elements coincident
        tol = 1e-6
        #   Selects the first solution file in the adjusted_files folder
        path = p.cfd_content
        #   This line is to show all the columns
        pd.set_option('display.expand_frame_repr', False)
        #   Reads the content to parse x, y coordinates associated with the elements
        content = pd.read_pickle(path + 'contents_{}_freezing.pkl'.format(self.dp))
        content = content[:max(content['element_number'])]
        #   Calculate z, r relative to the bottom of solution and center axis
        content['z'] = content['z'] - content['z'].min()
        content['r'] = content['r'] - content['r'].min()
        element_z = content['z'][self.index]
        element_r = content['r'][self.index]
        #   draw horozontal and vertical lines of nodes passing the element_number
        line_h = content[abs(content.z - element_z) < tol].sort_values('r')
        line_v = content[abs(content.r - element_r) < tol].sort_values('z')
        #   Locate the node in the horizontal and vertical lines and the
        #   adjacent nodes
        index_h = np.where(line_h['element_number'].values == self.index + 1)[0]
        index_v = np.where(line_v['element_number'].values == self.index + 1)[0]
        index_r_before = index_h - 1
        index_r_after = index_h + 1
        index_z_before = index_v - 1
        index_z_after = index_v + 1
        #   calculate element_number element_number
        element_r_1 = line_h['element_number'].values[index_r_before]
        element_r_2 = line_h['element_number'].values[index_r_after]
        element_z_1 = line_v['element_number'].values[index_z_before]
        element_z_2 = line_v['element_number'].values[index_z_after]
        adjacent_elements = [element_r_1[0], element_r_2[0], element_z_1[0], element_z_2[0]]
        return adjacent_elements

    def generate_samples(self):
        """
        This function generates same number of sample elements for each design points for autoencoder model

        Returns
        -------
        sample_points_tot: pandas.DataFrame
            Returns sample element_number indexes and saves to pickle files
        """
        files = os.listdir(p.cfd_content)
        if 'sample_points.pkl' not in os.listdir(p.output_dir):
            dps = []
            sample_points_tot = pd.DataFrame()
            for file in files:
                if 'freezing' in file:
                    sample_points_dp = []
                    dp = file.split('_')[1]
                    r_list = np.linspace(0.05, 0.95, p.m)
                    z_list = np.linspace(0.05, 0.95, p.n)
                    for i in tqdm.tqdm(range(len(r_list)), desc='Generating Sample Points DP {}'.format(self.dp)):
                        r_n = r_list[i]
                        for z_n in z_list:
                            sample_points_dp.append(self.element_r_z_normalized())
                    sample_points_tot[str(self.dp)] = sample_points_dp
            sample_points_tot.to_pickle(p.output_dir + 'sample_points.pkl')
        else:
            print('Previous sample element_number data detected!')
            sample_points_tot = 0

        return sample_points_tot
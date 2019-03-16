"""DEM Data Downloader
This script allows the user to download Digital Elevation Model for a given area from SRTM mission. Script uses
Elevation Python library: http://elevation.bopen.eu/en/stable/

Library downloads global datasets SRTM 30m Global 1 arc second V003 elaborated by NASA and NGA hosted on Amazon S3
and SRTM 90m Digital Elevation Database v4.1 elaborated by CGIAR-CSI.

MAJOR DRAWBACK: only 9 tiles per request... It is overriden by the GenerateDataframe class in the
data processing module where for each point data is downloaded and stored in special folder.

Author: Szymon Moliński, Data Lions
Last change: 16-03-2019
Change by: SM
...
"""

from operator import itemgetter
import elevation
import pyproj


class DEMRequest:

    def __init__(self, interactive=False, output_folder='', bounds=None, crs=None):
        self.interactive = interactive
        self.destination_folder = output_folder
        self.bounds = bounds
        if crs is not None:
            self.initial_crs = pyproj.Proj(crs)
            self.destination_points = self._reproject()
        self.destination_crs_type = {'init': 'epsg:4326'}  # geodetic coordinates in the WGS84 refernce system EPSG:4326
        available_datasets = self._initialize_datasets()
        self.data_dict = available_datasets[0]
        self.datasets_description = available_datasets[1]


    @staticmethod
    def _initialize_datasets():
        """If you want to add new datasets do it inside this method.
        To make everything readable and clear create new variable for each parameter and update data type dictionary
        and description text.
        Example: SRTM 30m Global 1 arc second V003
        temperature2m = ['SRTM1', 'SRTM 30m Global 1 arc second V003;]
        Example: Some Parameter
        some_parameter = ['variable name for api request', 'variable name']"""

        # VARIABLES
        # Create variables based on this example below
        srtm30 = ['SRTM1', 'SRTM 30m Global 1 arc second V003']
        srtm90 = ['SRTM3', 'SRTM 90m Digital Elevation Database v4.1']

        # VARIABLES GROUP
        variables = [srtm30, srtm90]  # Add here new variables
        sorted_variables = sorted(variables, key=itemgetter(0))

        # DATA TYPE DICTIONARY and DESCRIPTION TEXT
        data_type_dict = {}
        description_text = 'Select number to get a SRTM set:\n'
        i = 0
        for variable in sorted_variables:
            i = i + 1
            data_type_dict[i] = variable[0]
            description_text = description_text + (str(i) + ': ' + variable[1] + '\n')

        return data_type_dict, description_text

    def _reproject(self):
        wgs84 = pyproj.Proj(self.destination_crs_type)
        first_pair = pyproj.transform(self.initial_crs, wgs84, self.bounds[0], self.bounds[1])
        second_pair = pyproj.transform(self.initial_crs, wgs84, self.bounds[2], self.bounds[3])
        destination_points = (first_pair[0], first_pair[1], second_pair[0], second_pair[1])
        return destination_points

    def _get_input_data(self):

        input_info = []

        # Select variable
        selected_variable = int(input(self.datasets_description + 'After selection press RETURN\n'))
        input_info.append(self.data_dict[selected_variable])

        # Select areas bounds
        area_bounds = 'Please provide bounding box as the geodetic coordinates of the desired area in the form: ' \
                     'upper left point x, upper left point y, bottom right point x, bottom right point y\n'

        area_bounds = input(area_bounds)

        points_list = area_bounds.split(' ')
        points_list = [float(p) for p in points_list]

        input_info.append(points_list)

        # Output file
        output_filename = self.destination_folder
        name = input('Please, provide output filename and press RETURN:\n')
        input_info.append(output_filename + name + '.tif')
        return input_info

    def download_area(self, srtm_model=1):
        if self.interactive:
            input_information = self._get_input_data()
        else:
            input_information = [self.data_dict[srtm_model], self.destination_points, self.destination_folder]

        elevation.clip(product=input_information[0], bounds=tuple(input_information[1]), output=input_information[2])
        # clean up stale temporary files and fix the cache in the event of a server error
        elevation.clean()

    def __str__(self):
        output = ''
        for key in self.data_dict:
            output = 'Select key {} to get the {}'.format(key, self.data_dict[key])
        return output


if __name__ == '__main__':
    dem = DEMRequest(interactive=True)
    dem.download_area()

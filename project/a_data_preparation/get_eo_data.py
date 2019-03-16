"""EO Data Downloader
This script allows the user to download modis terra LST / NDVI datasets from the modis website with pyModis
library: http://www.pymodis.org/.

Class retrieves:
1. MOD11B3: MODIS/Terra Land Surface Temperature and Emissivity Monthly L3 Global 6 km Grid SIN V006
- https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod11b3_v006
2. MOD13C2: MODIS/Terra Vegetation Indices Monthly L3 Global 0.05 Deg CMG V006
- https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/mod13c2_v006

in the HDF format

Author: Szymon Moliński, Data Lions
Last change: 15-03-2019
Change by: SM
...
"""

from operator import itemgetter
import pymodis


class ModisRequest:
    """Class is a container for available modis datasets and returns request form based on the user's input
    in the terminal.
    New datasets should be incorporated into a private method _initialize_datasets()"""

    def __init__(self, interactive=False, output_folder=''):
        """
        :param interactive: if True then script is performed in the shell, otherwise arguments must be passed
        into a methods
        :param output_folder: path where data should be stored
        """
        self.interactive = interactive
        self.modis_request = None
        available_datasets = self._initialize_datasets()
        self.data_dict = available_datasets[0]
        self.datasets_description = available_datasets[1]
        self.output = output_folder

    @staticmethod
    def _initialize_datasets():
        """If you want to add new datasets do it inside this method.
        To make everything readable and clear create new variable for each parameter and update data type dictionary
        and description text.
        Example: MODIS/Terra Land Surface Temperature and Emissivity Monthly L3 Global 6 km Grid SIN V006
        temperature2m = ['MOD11B3.006', 'MODIS/Terra Land Surface Temperature and Emissivity Monthly L3 Global 6 km Grid SIN V006']
        Example: Some Parameter
        some_parameter = ['variable name for modis api request', 'variable name']"""

        # VARIABLES
        # Create variables based on this example below
        lst_annual = ['MOD11B3.006',
                      'MODIS/Terra Land Surface Temperature and Emissivity Monthly L3 Global 6 km Grid SIN V006']
        vi_annual = ['MOD13C2.006',
                     'MODIS/Terra Vegetation Indices Monthly L3 Global 0.05 Deg CMG V006']

        # VARIABLES GROUP
        variables = [lst_annual, vi_annual]  # Add here new variables
        sorted_variables = sorted(variables, key=itemgetter(0))

        # DATA TYPE DICTIONARY and DESCRIPTION TEXT
        data_type_dict = {}
        description_text = 'Select number to get a modis set:\n'
        i = 0
        for variable in sorted_variables:
            i = i + 1
            data_type_dict[i] = variable[0]
            description_text = description_text + (str(i) + ': ' + variable[1] + '\n')

        return data_type_dict, description_text

    def prepare_requests(self, username=None, password=None, input_information=None):
        """
        Function prepares input for a request to retrieve MODIS datasets in the hdf format.
        :param password: password into the MODIS dataset library (LP DAAC),
        :param username: username into the MODIS dataset library (LP DAAC),
        :param input_information: input_data about spatial and temporal scale of a dataset in the form of Python list:
        [variable number (to check numbers invoke DataRequest object with argument data_dict or print
        DataRequest object),
        tiles names as a list - (for Germany, Poland, Czechia and Slovakia valid tiles are:
                                 h18v03, h18v04, h19v03, h19v04)
        start date in the form: 'YYYY-MM-DD',
        end date in the form: 'YYYY-MM-DD'
        output filename without '.hdf' ending]
        :return: cds api request
        """
        if self.interactive:
            input_information = self._get_input_data()

        variable = self.data_dict[input_information[0]]

        if username is None:
            username = input('Please, provide your username and press RETURN:\n')

        if password is None:
            password = input('Please, provide your password and press RETURN:\n')

        downloading_object = pymodis.downmodis.downModis(destinationFolder=input_information[4],
                                                         password=password,
                                                         user=username,
                                                         tiles=input_information[1],
                                                         path='MOLT',
                                                         product=variable,
                                                         today=input_information[2],
                                                         enddate=input_information[3])
        self.modis_request = downloading_object
        return downloading_object

    def _get_input_data(self):

        input_info = []

        # Select variable
        selected_variable = int(input(self.datasets_description + 'After selection press RETURN\n'))
        input_info.append(selected_variable)

        # Select tiles
        tiles_text = 'Please, choose tiles for download. Default are h18v03, h18v04, h19v03, h19v04\n' \
                     'If default type d and press RETURN else type tilenames separated by comma and press RETURN\n'

        tiles_text = input(tiles_text)

        if tiles_text == 'd':
            tiles = ['h18v03,h18v04,h19v03,h19v04']
        else:
            tiles = tiles_text

        input_info.append(tiles)

        # Select years
        year_selection_start = 'Please provide start year-month-day of analysis in the form:\n' \
                               'YYYY-MM-DD and press RETURN):\n'
        year_selection_end = 'Please provide end year-month-day of analysis in the form:\n' \
                             'YYYY-MM-DD and press RETURN):\n'
        input_info.append(input(year_selection_start))
        input_info.append(input(year_selection_end))

        # Output file
        output_filename = self.output
        name = input('Please, provide output filename and press RETURN:\n')
        input_info.append(output_filename + name)
        return input_info

    def get_modis_data(self):
        self.modis_request.connect()
        self.modis_request.downloadsAllDay()
        return True

    def __str__(self):
        output = ''
        for key in self.data_dict:
            output = 'Select key {} to get the {}'.format(key, self.data_dict[key])
        return output


if __name__ == '__main__':
    mr = ModisRequest(True)
    mr.prepare_requests()
    mr.get_modis_data()

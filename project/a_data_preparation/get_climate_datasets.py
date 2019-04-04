"""Climate Datasets Downloader
This script allows the user to download climate datasets from the Coperniucs Climate Change Serivice
by cdsapi package and terminal commands.
Actually class retrieves ERA5 hourly data on single levels from 1979 to present, for all months,
all days in a month, and all hours in a day in the NetCDF format
(https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form):
- 2m temperature,
Author: Szymon Moliński, Data Lions
Last change: 13-03-2019
Change by: SM
...
"""

from operator import itemgetter
import cdsapi


class DataRequest:
    """Class is a container for available data types and usually returns request form based on the user's input
    in the terminal.
    New datasets should be incorporated into a private method _initialize_datasets()"""

    def __init__(self, interactive=False, output_folder=''):
        """
        :param output_folder: path where data should be stored
        """
        self.interactive = interactive
        self.cds_request = None
        available_datasets = self._initialize_datasets()
        self.data_dict = available_datasets[0]
        self.datasets_description = available_datasets[1]
        self.output = output_folder

    def prepare_requests(self, input_information=None):
        """
        Function prepares input for a request to retrieve Copernicus ERA5 single level
        reanalysis datasets in the netcdf format.

        INPUT:
        :param input_information: input_data about spatial and temporal scale of a dataset in the form of Python list:
        [variable number (to check numbers invoke DataRequest object with argument data_dict or print
        DataRequest object),
        list of years from 1979 to 2018 as a strings,
        list of months from 1 to 12 as a strings,
        list of days from 1 to 31 as a strings,
        list of hours from 00:00 to 23:00 as a strings,
        output filename without '.nc' ending]

        OUTPUT:
        :return: cds api request
        """
        if self.interactive:
            input_information = self._get_input_data()
        request_type = 'reanalysis-era5-single-levels'
        product_type = 'reanalysis'
        file_format = 'netcdf'
        variable = self.data_dict[input_information[0]]
        years = input_information[1]
        months = input_information[2]
        days = input_information[3]
        hours = input_information[4]
        output_name = input_information[5]
        request_text = (
            request_type,
            {
                'product_type': product_type,
                'format': file_format,
                'variable': variable,
                'year': years,
                'month': months,
                'day': days,
                'time': hours
            },
            output_name
        )
        return request_text

    def _initialize_datasets(self):
        """If you want to add new datasets do it inside this method.
        To make everything readable and clear create new variable for each parameter and update data type dictionary
        and description text.
        Example: 2m Temperature
        temperature2m = ['2m_temperature', '2m Temperature;]
        Example: Some Parameter
        some_parameter = ['variable name for cds api request', 'variable name']

        OUTPUT:
        :return dictionary with datasets, description text for an interactive request setting
        """

        # VARIABLES
        temperature2m = ['2m_temperature', '2m Temperature']  # Create variables based on this example below

        # VARIABLES GROUP
        variables = [temperature2m]  # Add here new variables
        sorted_variables = sorted(variables, key=itemgetter(0))

        # DATA TYPE DICTIONARY and DESCRIPTION TEXT
        data_type_dict = {}
        description_text = 'Select number to get a climate variable:\n'
        i = 0
        for variable in sorted_variables:
            i = i + 1
            data_type_dict[i] = variable[0]
            description_text = description_text + (str(i) + ': ' + variable[1] + '\n')

        return data_type_dict, description_text

    def _get_input_data(self):
        """If interactive session is selected then this method serves as the communication channel between an user
        and a program. All text is printed in terminal and at the same place user provides information about needed
        variables.

        OUTPUT:
        :return input_info: A list in the form: [
                                                    selected dataset,
                                                    [list of years to get the data],
                                                    [list of months to get the data],
                                                    [list of days to get the data],
                                                    [list of hours to get the data],
                                                    output filename
                                                ]
        """
        input_info = []

        # Select variable
        selected_variable = int(input(self.datasets_description + 'After selection press RETURN\n'))
        input_info.append(selected_variable)

        # Select years
        year_selection_start = 'Please provide start and end year of the analysis:\n' \
                               'Start year (number in format XXXX, min. 1979, max. 2018, press RETURN):\n'
        year_selection_end = 'End year (number in format XXXX, min. 1979, max. 2018, press RETURN):\n'
        y_start = int(input(year_selection_start))
        y_end = int(input(year_selection_end))
        input_info.append([str(x) for x in range(y_start, y_end + 1)])

        # Select month
        month_selection_start = 'Please provide start and end month of the analysis:\n' \
                                'Start month (number from 1 to 12, press RETURN):\n'
        month_selection_end = 'End month (number from 1 to 12, press RETURN):\n'
        m_start = int(input(month_selection_start))
        m_end = int(input(month_selection_end))
        input_info.append([str(x) for x in range(m_start, m_end + 1)])

        # Select day (all days are chosen)
        days = range(1, 32)
        days = [str(x) for x in days]
        input_info.append(days)

        # Select hours
        slt_hours = '0: 00:00, \n1: 06:00, \n2: 12:00, \n3: 18:00, \n4: 00:00 + 06:00 + 12:00 + 18:00, \n5: all hours' \
                    'from 00:00 to 23:00. \nType number and press RETURN\n'
        hours = int(input(slt_hours))
        hours_dict = {0: '00:00',
                      1: '06:00',
                      2: '12:00',
                      3: '18:00',
                      4: ['00:00', '06:00', '12:00', '18:00'],
                      5: ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
                          '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
                          '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
                          '21:00', '22:00', '23:00']}
        selected_hours = hours_dict[hours]
        input_info.append(selected_hours)

        # Output file
        output_filename = self.output
        name = input('Please, provide output filename (without .nc format) and press RETURN:\n')
        input_info.append(output_filename + name + '.nc')
        return input_info

    def __str__(self):
        output = ''
        for key in self.data_dict:
            output = 'Select key {} to get the {}'.format(key, self.data_dict[key])
        return output


def download_climate_data(request_text):
    """Method uses cdsapi Client to get the requested data"""
    try:
        c = cdsapi.Client()
    except Exception:  # too broad exception, narrow it
        print(Exception)
        print('Follow tutorial here: https://cds.climate.copernicus.eu/api-how-to to configure an api')
        return 0
    else:
        c.retrieve(request_text[0], request_text[1], request_text[2])


if __name__ == '__main__':
    a = DataRequest(True, '')
    req = a.prepare_requests()
    download_climate_data(req)

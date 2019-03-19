"""GBIF Data Downloader
This script allows the user to download species occurences from GBIF database with pygbif client. This section is
under development due to the large amount of queries which can be done for the GBIF database and it is not usable yet.

Author: Szymon Moliński, Data Lions
Last change: 16-03-2019
Change by: SM
...
"""

from pygbif import occurrences as occ
from pygbif import species as sps

class SpeciesRequest:

    def __init__(self, interactive=False, output_folder='', species_name='', country_of_occurence=''):
        self.interactive = interactive
        self.destination_folder = output_folder
        self.species = species_name
        self.country = country_of_occurence
        self.information = []
        if not interactive:
            self.information = [self.species, self.country, self.destination_folder]

    def _get_input_data(self):

        # Select variable
        selected_variable = input('Provide latin species name and press RETURN\n')
        self.information.append(selected_variable)

        # Country of occurence
        selected_country = input('Provide country code where species occur and press RETURN\n')
        self.information.append(selected_country)

        # Output file
        output_filename = self.destination_folder
        name = input('Please, provide output filename and press RETURN:\n')
        self.information.append(output_filename + name)
        return self.information

    def download_area(self, user=None, password=None, email=None):
        if self.interactive:
            input_information = self._get_input_data()
        else:
            input_information = self.information

        # Search for data
        key = sps.name_backbone(name=self.information[0], rank='species')['usageKey']
        if (user is None or password is None):
            user = input('Provide username and press RETURN\n')
            password = input('Provide password and press RETURN\n')
            email = input('Provide email and press RETURN\n')

        tk = 'taxonKey = ' + str(key)
        ct = 'country = ' + self.information[1]
        hascoo = 'hasCoordinate = TRUE'
        hasissues = 'hasGeospatialIssue = False'
        data = occ.download([tk, ct, hascoo, hasissues], user=user, pwd=password, email=email)
        return data

if __name__ == '__main__':
    sr = SpeciesRequest(interactive=True)
    dataset = sr.download_area()

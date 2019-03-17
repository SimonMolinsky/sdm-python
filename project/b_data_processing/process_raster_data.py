"""Raster Data Processing functions
Scripts in this module are designed for raster data processing and information retrieval.
Module processes:
a) rasters in geotiff format given by the user,
b) MODIS time series,
c) DEM datasets.

The main purpose of the script is to identify value at a given location. Usually point coordinates are reprojected
into the raster coordinates to protect data from the distortions related to the reprojection between different CRS.

Author: Szymon Moliński, Data Lions
Last change: 17-03-2019
Change by: SM
...
"""

from .scripts.prepare_files import get_filelist

########################################################################################################################
###                                                                                                                  ###
###                                       MODIS DATA PROCESSING PART                                                 ###
###                                                                                                                  ###
########################################################################################################################


class ModisProcessing:
    """Class process Modis datasets stored in the given folder. The main method calculates means or medians of the
    given time series. Additional methods retrieves point values for a given coordinates."""

    def __init__(self, folder_with_data=None):
        self.datafolder = folder_with_data
        self.tiles_list = []
        self.grouping = {
            'all': self._merge_all,
            'by_year': self._merge_by_year,
            'by_season_all': self._merge_by_season_all,
            'by_season': self._merge_by_season_year,
            'full': self._create_full_timeseries
        }

    ####################################################################################################################
    ###                                                                                                              ###
    ###                                       TIME SERIES GENERATION                                                 ###
    ###                                                                                                              ###
    ####################################################################################################################

    def create_time_series(self, input_directory=None, output_directory='', grouping_method='all',
                           years_limit=None, months_limit=None, tiles_type=None, indicator=None):
        """
        Function performs time series calculation, stores calculated bands in the given folder and returns list
        with: [[date 1, file 1], [date 2, file 2], ..., [date 999, file 999]] where date is in the format 'MM-YYYY'
        or 'YYYY' and file is returned as a full path to the processed .tif file/
        :param input_directory: full path to the directory with hdf files,
        :param output_directory: full path to the directory where files must be stored,
        :param grouping_method: available methods:
        'all' -> sums over all tiles and returns their average as a single band,
        'by_year' -> sums over the years and returns list of tiles average for each year,
        'by_season_all' -> sums over the four seasons for whole dataset and returns list with four tiles - spring,
        summer, autumn, winter, where
        spring = sum of all tiles from March, April, May,
        summer = sum of all tiles from June, July, August,
        autumn = sum of all tiles from September, October, November,
        winter = sum of all tiles from December, January, February,
        if three tiles for a fiven season are not available then partial data is not included in the sum.
        'by_season': returns list of lists where each inner list represents one year and records in this list are
        seasonal sums. Partial years are not included in the output.
        'full': returns sorted by year and month list in the form:
        [[tile 1, file 1], [tile 2, file 2], ..., [tile 999, file 999]]
        :param years_limit: Python range of years to be included in the analysis as a list of years,
        :param months_limit: Python range of years to be included in the analysis as a list of months from 1 to 12,
        :param tiles_type: tile name, as example: 'h18v03'
        :param indicator: indicator number for a given .hdf datafile. Default is 0. Indices may be read from the
        MODIS documentation.
        :return output_files: list with: [[date 1, file 1], [date 2, file 2], ..., [date 999, file 999]]
        """
        self.tiles_list = get_filelist(input_directory, tiles_type, '.hdf')
        if grouping_method == 'full':
            tiles_groups_to_merge = self.grouping[grouping_method]
        else:
            tiles_groups_to_merge = self.grouping[grouping_method](years_limit, months_limit)






    def _merge_all(self, years, months):
        pass

    def _merge_by_year(self, years, months):
        pass

    def _merge_by_season_all(self, years, months):
        pass

    def _merge_by_season_year(self, years, months):
        pass

    def _create_full_timeseries(self):
        pass

    ####################################################################################################################
    ###                                                                                                              ###
    ###                                       POINTS VALUES RETRIEVAL                                                ###
    ###                                                                                                              ###
    ####################################################################################################################

########################################################################################################################
###                                                                                                                  ###
###                                       DEM AND EO DATA PROCESSING PART                                            ###
###                                                                                                                  ###
########################################################################################################################

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

import tempfile
from scripts.prepare_files import get_filelist
from scripts.prepare_files import create_modis_dataframe

########################################################################################################################
###                                                                                                                  ###
###                                       MODIS DATA PROCESSING PART                                                 ###
###                                                                                                                  ###
########################################################################################################################


class ModisProcessing:
    """Class process Modis datasets stored in the given folder. The main method calculates means or medians of the
    given time series. Additional methods retrieves point values for a given coordinates."""

    def __init__(self, lookup_table_leap='additional_data/lut_modis/julian_day_calendar_leap.csv',
                 lookup_table_regular='additional_data/lut_modis/julian_day_calendar_regular.csv'):
        self.tiles_list = []
        self.grouping = {
            'all': self._merge_all,
            'by_year': self._merge_by_year,
            'by_season_all': self._merge_by_season_all,
            'by_season': self._merge_by_season_year,
            'full': self._create_full_timeseries
        }
        self.leap_lut = lookup_table_leap
        self.regular_lut = lookup_table_regular
        self.tiles_dict = None

    ####################################################################################################################
    ###                                                                                                              ###
    ###                                       TIME SERIES GENERATION                                                 ###
    ###                                                                                                              ###
    ####################################################################################################################

    def create_time_series(self, input_directory=None, output_directory='', grouping_method='all',
                           years_limit=None, months_limit=range(1, 13), tiles_type=None, indicator=None):
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
        df = self._prepare_frame(years_limit, months_limit, tiles_type)
        tiles_groups_to_process = self.grouping[grouping_method](df)

    def _merge_all(self, modis_dataframe):
        print(modis_dataframe.head(20))

    def _merge_by_year(self, modis_dataframe, years, months):
        pass

    def _merge_by_season_all(self, modis_dataframe, years, months):
        pass

    def _merge_by_season_year(self, modis_dataframe, years, months):
        pass

    def _create_full_timeseries(self, modis_dataframe):
        pass

    def _prepare_frame(self, years, months, tilename):
        # Prepare dictionary with tiles for processing
        modis_data = create_modis_dataframe(self.tiles_list, self.leap_lut, self.regular_lut, tilename,
                                            sort_by_date=True)
        modis_data_updated = modis_data[modis_data[3].isin(years)]
        modis_data_updated = modis_data_updated[modis_data_updated[4].isin(months)]
        self.tiles_dict = modis_data_updated
        return modis_data_updated

    def _open_band(self, band_address, temp_output):
        """Function opens chosen modis band and save it as a tiff file then returns address to it."""
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


if __name__ == '__main__':
    mc = ModisProcessing()
    mc.create_time_series(input_directory='../sample_datamodis', output_directory='', years_limit=range(2002, 2011),
                          months_limit=[7], tiles_type='h18v03', indicator=0)

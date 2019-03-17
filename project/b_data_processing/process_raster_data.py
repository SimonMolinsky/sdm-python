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
                           years_limit=None, months_limit=None, tiles_type=None):
        pass

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

"""DEM Data Downloader
This script allows the user to download Digital Elevation Model for a given area from SRTM mission. Script uses
Elevation Python library: http://elevation.bopen.eu/en/stable/

Library downloads global datasets SRTM 30m Global 1 arc second V003 elaborated by NASA and NGA hosted on Amazon S3
and SRTM 90m Digital Elevation Database v4.1 elaborated by CGIAR-CSI.

Author: Szymon Moliński, Data Lions
Last change: 15-03-2019
Change by: SM
...
"""

import elevation


def _reproject(points, source_crs, destination_crs):
    pass


def download_area(bounds, crs):
    pass
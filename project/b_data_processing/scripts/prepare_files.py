import os
import datetime
import pandas as pd


def _only_chosen(bag_of_files, infile, file_end):
    f_list = []
    for f in bag_of_files:
        if f.endswith(file_end):
            for rec in infile:
                if rec in f:
                    f_list.append(f)
    return f_list


def get_filelist(folder, infile, file_ending):
    filelist = os.listdir(folder)
    filelist = _only_chosen(filelist, infile, file_ending)
    return filelist


def _get_tilename(tile, tilenames):
    if type(tilenames) == str:
        if tilenames in tile:
            return tilenames
    else:
        for tilename in tilenames:
            if tilename in tile:
                return tilename
            else:
                pass


def _leap_or_regular(year):
    if ((year % 4) == 0 and (year % 100) != 0) or ((year % 400) == 0):
        return True
    else:
        return False


def julian_date_to_month(name_str, lookup_table_leap, lookup_table_regular, tilenames):
    """Function for MODIS file name processing"""

    tilename = _get_tilename(name_str, tilenames)

    # Get year and Julian day from filename
    position = name_str.find('.')
    position = position + 2
    position_end = position + 7
    date = name_str[position:position_end]
    m_year = date[:4]
    m_year = int(m_year)
    julian_day = date[4:]
    julian_day = int(julian_day)

    # Check if year is leap or not
    is_leap = _leap_or_regular(m_year)

    # Find month of measurements
    if is_leap:
        lut_address = lookup_table_leap
    else:
        lut_address = lookup_table_regular

    lut_df = pd.read_csv(lut_address, index_col=0)

    cols = list(lut_df.columns)
    status = lut_df.isin([julian_day]).any().any()

    acquisition_time = '-1'
    nb_month = '-1'

    if status:
        for col in cols:
            if lut_df[col].isin([julian_day]).any():
                str_month = col
                nb_month = lut_df.columns.get_loc(str_month) + 1
                day = list(lut_df[col][lut_df[col] == julian_day].index)[0]

                # Set the date
                acquisition_time = datetime.date(year=m_year,
                                                 month=nb_month,
                                                 day=day)
        return [name_str, tilename, acquisition_time, m_year, nb_month]
    else:
        return [name_str, '-1', '-1', '-1', '-1', '-1']


def create_modis_dataframe(hdf_files, lookup_table_leap, lookup_table_regular, tilenames, sort_by_date=True):
    data = []
    for f in hdf_files:
        data.append(julian_date_to_month(f, lookup_table_leap, lookup_table_regular, tilenames))
    df = pd.DataFrame(data, columns=['filename', 'tile type', 'acquisition time', 'year', 'month'])
    if sort_by_date:
        df = df.sort_values(['acquisition time', 'filename'])
    df.drop_duplicates(inplace=True)
    return df

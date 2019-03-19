import rasterio as rio


def get_crs_from_raster(raster_address):
    """Function reads raster data and gets its coordinate reference system"""
    with rio.open(raster_address) as f:
        band_crs = f.crs
    return band_crs

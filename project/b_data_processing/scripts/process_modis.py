import os

import rasterio as rio
import rasterio.mask as rmask

from osgeo import gdal


def hdf_to_tiff(base_folder_modis, list_of_files, output_folder, datasets):

    for f in list_of_files:

        path_to_file = os.path.join(base_folder_modis, f)
        modis_data = gdal.Open(path_to_file)
        subdatasets = modis_data.GetSubDatasets()

        vals = []
        output_paths = []
        if type(datasets) == int:
            val = subdatasets[datasets][0]
            vals.append(val)
            filename = 'mod_' + f[:-4] + str(datasets) + '.tif'
            output_path = os.path.join(output_folder, filename)
            output_paths.append(output_path)
            gdal.Translate(output_path, val, options=gdal.TranslateOptions([b'-ot', b'Float32']))
        else:
            for ds in datasets:
                val = subdatasets[ds][0]
                vals.append(val)
                filename = 'mod_' + f[:-4] + str(ds) + '.tif'
                output_path = os.path.join(output_folder, filename)
                output_paths.append(output_path)
                gdal.Translate(output_path, val, options=gdal.TranslateOptions([b'-ot', b'Float32']))

        del modis_data
        for p in output_paths:
            print('File {} processed successfully'.format(p))
    return output_paths


def clip_area(vector_geometry, raster_file, save_image_to):
    with rio.open(raster_file, 'r') as raster_source:
        try:
            clipped_image, transform = rmask.mask(raster_source, vector_geometry, crop=True)
            metadata = raster_source.meta.copy()
            metadata.update({"driver": "GTiff",
                             "height": clipped_image.shape[1],
                             "width": clipped_image.shape[2],
                             "transform": transform})
            with rio.open(save_image_to, "w", **metadata) as g_tiff:
                g_tiff.write(clipped_image)

            message = 'STATUS 1: Clipped: {} saved successfully'.format(save_image_to)

        except ValueError:
            message = 'STATUS 0: ' + save_image_to + ' not clipped - wrong geometry'
            print(message)
            with open('log.txt', 'a') as the_file:
                the_file.write(message + '\n')

    return message
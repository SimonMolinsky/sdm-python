import numpy as np
import rasterio as rio


class RandomSubset:

    def __init__(self, band_file):
        self.file = band_file
        with rio.open(band_file, 'r') as f:
            self.band = f.read(1)
            self.transformation_matrix = f.transform
        self.random_coordinates = []
        self.coordinates_list = []

    @staticmethod
    def unique_rows(a):
        a = np.ascontiguousarray(a)
        unique_a = np.unique(a.view([('', a.dtype)] * a.shape[1]))
        return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

    def get_random_coordinates(self, ratio=10):
        # ratio in %
        # shape 0: rows
        # shape 1: cols
        s = self.band.shape
        rows = s[0]
        cols = s[1]
        number_of_pixels = int(rows * cols / ratio)
        random_rows = np.random.randint(rows, size=number_of_pixels)
        random_cols = np.random.randint(cols, size=number_of_pixels)
        random_coordinates = np.stack((random_cols, random_rows), axis=1)
        random_coordinates = self.unique_rows(random_coordinates)
        self.random_coordinates = random_coordinates
        return random_coordinates

    def get_values(self):
        for coordinate in self.random_coordinates:
            value = self.band[coordinate[1], coordinate[0]]
            if value > 0:
                transformed_coordinates = self.transformation_matrix * (coordinate[0], coordinate[1])
                self.coordinates_list.append([transformed_coordinates[0], transformed_coordinates[1], value])
            else:
                pass
        return self.coordinates_list
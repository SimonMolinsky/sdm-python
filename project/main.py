from a_data_preparation.get_eo_data import ModisRequest


if __name__ == '__main__':

    # Prepare MODIS data

    mr = ModisRequest(interactive=True, output_folder='sample_data')
    mr.prepare_requests()
    mr.get_modis_data()

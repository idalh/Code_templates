if __name__ == '__main__':
    # Import relevant libraries
    import xarray as xr
    from functions import getSceneMetadata
    import gdal

    Le = 2.454 * 10 ** 6 # J/kg, latent heat of vaporisation at 20 degrees

    # Import data
    filein = (r'/Users/ida/OneDrive_DTU/DTU/Kandidat/Speciale/Thesis_outputfiles/Budyko/Mean_all_years/all_years_precip.nc')
    Data = xr.open_dataset(filein)
    precip = Data.pred[:] ## mm/day

    filein = (r'/Users/ida/OneDrive_DTU/DTU/Kandidat/Speciale/Thesis_outputfiles/Budyko/Mean_all_years/all_years_AET.nc')
    Data = xr.open_dataset(filein)
    AET = Data.AET_ATI[:] # W/m^2
    AET = AET * 86400 / Le

    filein = (r'/Users/ida/OneDrive_DTU/DTU/Kandidat/Speciale/Thesis_outputfiles/Budyko/Mean_all_years/all_years_PET.nc')
    Data = xr.open_dataset(filein)
    PET = Data.PET[:] # mm/day

    # Define saving location:
    location = '/Users/ida/OneDrive - Danmarks Tekniske Universitet/Arbejde/Ansøgninger/phd_ecosystems/Presentation/'

    # For efficiency turn into numpy arrays: #
    P = precip.values
    A = AET.values
    POT = PET.values

    # Evaporative index
    EVA = A / P

    # Aridity Index
    ARI = POT/P

    # Get reference image to save data:
    reference_image = '/Users/ida/OneDrive_DTU/DTU/Kandidat/Speciale/Data_Ellen_Maria/Landcover Map/landuse_Spain_CLC_2012_1100m.tif'
    Metadata = getSceneMetadata(reference_image)  # Gets the information to create the file from AndaluciaRef.tif saved in the dat folder.

    # Save files with right projection
    # Save evaporative index data
    EVA_save = location + 'EVA_presentation.tif'
    tiff_file = gdal.GetDriverByName('GTiff').Create(EVA_save, 1115, 834, 1, gdal.GDT_Float64)
    tiff_file.SetGeoTransform(Metadata['gt'])  # specify coordinates

    outband = tiff_file.GetRasterBand(1)
    outband.WriteArray(EVA)
    tiff_file.FlushCache()
    tiff_file = None

    # Save aridity index data
    ARI_save = location + 'ARI_presentation.tif'
    tiff_file = gdal.GetDriverByName('GTiff').Create(ARI_save, 1115, 834, 1, gdal.GDT_Float64)
    tiff_file.SetGeoTransform(Metadata['gt'])  # specify coordinates

    outband = tiff_file.GetRasterBand(1)
    outband.WriteArray(ARI)
    tiff_file.FlushCache()
    tiff_file = None



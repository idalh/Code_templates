
def getSceneMetadata(reference_image):
    import gdal
    metadata = {'xsize':0 ,'ysize': 0, 'bands':0, 'gt':[], 'proj':''}
    inputImage = gdal.Open(reference_image, gdal.GA_ReadOnly)
    if inputImage:
        metadata['xsize'] = inputImage.RasterXSize
        metadata['ysize'] = inputImage.RasterYSize
        metadata['bands'] = inputImage.RasterCount
        metadata['gt'] = inputImage.GetGeoTransform()
        metadata['proj'] = inputImage.GetProjection()
        #inputImage = None # Maybe delete this part?
    return metadata
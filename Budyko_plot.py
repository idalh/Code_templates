if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")

    import geopandas as gpd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from rasterstats import zonal_stats
    from matplotlib import rcParams
    sns.set()

    # Shapefile location
    vec = '/Users/ida/OneDrive_DTU/DTU/Kandidat/Speciale/data/Cuencas/Gorkas/reprojected_cuencas.shp'
    bud = gpd.read_file(vec)

    # Raster file location
    EVA = '/Users/ida/OneDrive - Danmarks Tekniske Universitet/Arbejde/Ansøgninger/phd_ecosystems/Presentation/EVA_presentation.tif'
    ARI = '/Users/ida/OneDrive - Danmarks Tekniske Universitet/Arbejde/Ansøgninger/phd_ecosystems/Presentation/ARI_presentation.tif'

    # Calculate zonalstatistics for Evaporative and Aridity index:
    result = zonal_stats(vec, EVA, stats='mean', geojson_out=True)
    df = gpd.GeoDataFrame.from_features(result) # Make geopandas dataframe
    df.rename(columns={'mean': 'Evaporativ'}, inplace=True)
    bud = bud.join(df['Evaporativ'])

    result = zonal_stats(vec, ARI, stats='mean', geojson_out=True)
    df = gpd.GeoDataFrame.from_features(result)
    df.rename(columns={'mean': 'Aridity'}, inplace=True)
    bud = bud.join(df['Aridity'])

    location = '/Users/ida/OneDrive - Danmarks Tekniske Universitet/Arbejde/Ansøgninger/phd_ecosystems/Presentation/'
    bud.to_file(location + 'Budyko_all_years' + '.sh')

    fig = plt.figure()
    with sns.axes_style("whitegrid"):
        sns.scatterplot(bud['Aridity'], bud['Evaporativ'], label='Watershed')
        ax = plt.axes()
        ax.plot([0, 1], [0, 1], color='red', linewidth=1, label='limit')
        ax.plot([1, max(bud['Aridity'])], [1, 1], color='red', linewidth=1)
        ax.set_ylabel('Evaporative Index [$ET/P$]')
        ax.set_xlabel('Aridity Index [$ET_{p}/P$]')
        plt.legend()
        plt.show()

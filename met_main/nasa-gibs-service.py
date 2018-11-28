# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

import matplotlib.patheffects as PathEffects

from owslib.wmts import WebMapTileService

import cartopy.crs as ccrs


def main():
    # URL of NASA GIBS
    URL = 'http://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi'
    wmts = WebMapTileService(URL)

    # print(wmts.contents)

    sorted(wmts.contents)

    # Layers for MODIS true color and snow RGB
    # layers = ['MODIS_Terra_SurfaceReflectance_Bands143',
    #           'MODIS_Terra_CorrectedReflectance_Bands367',
    #           'AMSR2_Surface_Precipitation_Rate_Day',
    #           'AMSR2_Surface_Precipitation_Rate_Night']

    layers = [ 'MODIS_Terra_CorrectedReflectance_Bands367',
              'MODIS_Terra_SurfaceReflectance_Bands143']

    date_str = '2018-07-23'

    # Plot setup
    plot_CRS = ccrs.Mercator()
    geodetic_CRS = ccrs.Geodetic()

    # x0, y0 = plot_CRS.transform_point(4.6, 43.1, geodetic_CRS)
    # x1, y1 = plot_CRS.transform_point(11.0, 47.4, geodetic_CRS)

    x0, y0 = plot_CRS.transform_point(112,  30, geodetic_CRS)
    x1, y1 = plot_CRS.transform_point(125,  42, geodetic_CRS)


    ysize = 8
    xsize = 2 * ysize * (x1 - x0) / (y1 - y0)
    fig = plt.figure(figsize=(xsize, ysize), dpi=100)

    for layer, offset in zip(layers, [0, 0.5]):
        ax = fig.add_axes([offset, 0, 0.5, 1], projection=plot_CRS)
        ax.set_xlim((x0, x1))
        ax.set_ylim((y0, y1))
        ax.add_wmts(wmts, layer, wmts_kwargs={'time': date_str})
        txt = ax.text(4.7, 43.2, wmts[layer].title, fontsize=18, color='wheat',
                      transform=geodetic_CRS)
        # txt.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='black')])
        plt.title(wmts[layer].title, fontsize=18, color='wheat' )
        plt.show()

    plt.savefig("wmts_example.png")
    plt.close()

##################################################################

    fig = plt.figure(2, dpi=200)
    ax = fig.add_axes([0, 0, 1, 1], projection=plot_CRS)
    ax.set_xlim((x0, x1))
    ax.set_ylim((y0, y1))

    ax.add_wmts(wmts, layers[0], wmts_kwargs={'time': date_str})

    plt.title(wmts[layers[0]].title, fontsize=18, color='wheat')
    plt.savefig("wmts_layer00.png")
    plt.close()



    fig = plt.figure(3, dpi=200)
    ax = fig.add_axes([0, 0, 1, 1], projection=plot_CRS)
    ax.set_xlim((x0, x1))
    ax.set_ylim((y0, y1))

    ax.add_wmts(wmts, layers[1], wmts_kwargs={'time': date_str})

    plt.title(wmts[layers[1]].title, fontsize=18, color='wheat')
    plt.savefig("wmts_layer01.png")
    plt.close()


####################################################################

if __name__ == '__main__':
    main()
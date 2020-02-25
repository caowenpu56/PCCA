# -*- coding: utf-8 -*-
# Wenpu Cao caowenpu56@gmail.com

import numpy as np
import pickle
import queue
from math import fabs, sin, cos, sqrt, pi
from osgeo import gdal

# Calculate the cell's spherical area
def countSpheroidArea(lat, dLat, dLng):
    a = 6378.137
    b = 6356.752314245179
    e = sqrt(1 - (b / a) * (b / a))
    tmp = 1 - e * e * sin(lat) * sin(lat)
    m = a * (1 - e * e)/(tmp * sqrt(tmp))
    n = a / sqrt(tmp)
    area = dLat * dLng * m * n * cos(lat)
    return fabs(area)

# Binarize the raw data to the urban/non-urban data under each potential threshold
def BinarizeTiff(tiffData):
    # Set each value of the tiff data as a potential urban density threshold
    values = np.unique(np.floor(tiffData))
    thresholds = values[values > 0].astype(int)
    pccaUnits = {}  # <thres, list<urban_units>>
    for thres in thresholds:
        pccaUnits[thres] = {}

    # Binarize the tiff data to the urban/non-urban data under each potential threshold
    for i in range(tiffData.shape[0]):
        for j in range(tiffData.shape[1]):
            for thres in thresholds:
                if tiffData[i][j] > thres:
                    pccaUnits[thres][(i, j)] = 0
    return pccaUnits

# Merge urban cells into urban clusters with CCA
def CCA(ccaUnits):
    cIndex = 1  # cluster id
    for (i, j) in ccaUnits:
        if ccaUnits[i, j] == 0:  # Start with a random unprocessed urban cell (0)
            unitQueue = queue.Queue()
            unitQueue.put((i, j))
            ccaUnits[(i, j)] = cIndex
            while not unitQueue.empty():  # Add eight nearest urban cells recursively
                (curX, curY) = unitQueue.get()
                if (curX - 1, curY) in ccaUnits and ccaUnits[(curX - 1, curY)] == 0:
                    unitQueue.put((curX - 1, curY))
                    ccaUnits[(curX - 1, curY)] = cIndex
                if (curX + 1, curY) in ccaUnits and ccaUnits[(curX + 1, curY)] == 0:
                    unitQueue.put((curX + 1, curY))
                    ccaUnits[(curX + 1, curY)] = cIndex
                if (curX, curY - 1) in ccaUnits and ccaUnits[(curX, curY - 1)] == 0:
                    unitQueue.put((curX, curY - 1))
                    ccaUnits[(curX, curY - 1)] = cIndex
                if (curX, curY + 1) in ccaUnits and ccaUnits[(curX, curY + 1)] == 0:
                    unitQueue.put((curX, curY + 1))
                    ccaUnits[(curX, curY + 1)] = cIndex
                if (curX - 1, curY - 1) in ccaUnits and ccaUnits[(curX - 1, curY - 1)] == 0:
                    unitQueue.put((curX - 1, curY - 1))
                    ccaUnits[(curX - 1, curY - 1)] = cIndex
                if (curX + 1, curY + 1) in ccaUnits and ccaUnits[(curX + 1, curY + 1)] == 0:
                    unitQueue.put((curX + 1, curY + 1))
                    ccaUnits[(curX + 1, curY + 1)] = cIndex
                if (curX + 1, curY - 1) in ccaUnits and ccaUnits[(curX + 1, curY - 1)] == 0:
                    unitQueue.put((curX + 1, curY - 1))
                    ccaUnits[(curX + 1, curY - 1)] = cIndex
                if (curX - 1, curY + 1) in ccaUnits and ccaUnits[(curX - 1, curY + 1)] == 0:
                    unitQueue.put((curX - 1, curY + 1))
                    ccaUnits[(curX - 1, curY + 1)] = cIndex
            cIndex = cIndex + 1

    ccaClusters = {}   # <cluster_id, list<cluster_units>>
    for (i, j) in ccaUnits:
        if ccaUnits[(i, j)] not in ccaClusters:
            ccaClusters[ccaUnits[(i, j)]] = []
        ccaClusters[ccaUnits[(i, j)]].append((i, j))
    return ccaClusters


# Note：X corresponds to Latitude (Row), Y corresponds to Longitude (Column)

dataPath = ''

if __name__ == '__main__':
    for dataItem in ['CHN_VIIRS2016', 'CHN_HomeDensity', 'CHN_JuncDensity']:
        # Read raw urban data (tiff)
        tiff = gdal.Open('%sRaw_Data/%s.tif' % (dataPath, dataItem))
        band = tiff.GetRasterBand(1)
        leftY, pixelWidth, _, topX, _, pixelHeight = tiff.GetGeoTransform()
        dLat = pixelHeight * pi / 180.0
        dLng = pixelWidth * pi / 180.0
        tiffData = band.ReadAsArray(0, 0, tiff.RasterXSize, tiff.RasterYSize)
        rasterRows = tiffData.shape[0]
        rasterCols = tiffData.shape[1]
        print('%s: topX:%f leftY:%f pHeight:%f pWidth:%f rows:%d cols:%d' % (dataItem, topX, leftY, pixelHeight, pixelWidth, rasterRows, rasterCols))

        # Binarize the raw data to the urban/non-urban data under each potential threshold
        pccaUnits = BinarizeTiff(tiffData)  # <thres, list<urban_units>>

        # Merge urban cells into urban clusters under each potential threshold
        pccaClusters = {}  # <thres, <cluster_id, list<cluster_units>>>
        for thres in pccaUnits:
            pccaClusters[thres] = CCA(pccaUnits[thres])

        # Calculate the spherical area for all clusters under each potential threshold
        pccaClusterAreas = {}  # <thres, <cluster_id, cluster_area>>
        for thres in pccaClusters:
            if thres not in pccaClusterAreas:
                pccaClusterAreas[thres] = {}
            for cIndex in pccaClusters[thres]:
                if cIndex not in pccaClusterAreas[thres]:
                    pccaClusterAreas[thres][cIndex] = 0
                for (i, j) in pccaClusters[thres][cIndex]:
                    lat = (topX + (i + 0.5) * pixelHeight) * pi / 180.0
                    unitArea = countSpheroidArea(lat=lat, dLat=dLat, dLng=dLng)
                    pccaClusterAreas[thres][cIndex] = pccaClusterAreas[thres][cIndex] + unitArea

        # Save the percolation results, then display to find the optimal threshold
        fp = open('%s%s_pccaAreas' % (dataPath, dataItem), 'wb')
        pickle.dump(pccaClusterAreas, fp)
        fp.close()

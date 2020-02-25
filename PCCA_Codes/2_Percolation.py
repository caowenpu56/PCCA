# -*- coding: utf-8 -*-
# Wenpu Cao caowenpu56@gmail.com

import matplotlib.pyplot as plt
import numpy as np
import pickle
from math import log

totalColor = '#ef6548'  # color for results of all clusters
largeColor = '#4751b0'  # color for results of clusters > 20km2
lWidth = 1   # line width
mSize = 4   # marker size
textSize = 9  # text size
legSize = 6  # legend size

dataPath = ''

if __name__ == '__main__':
    minSize = 20  # the minimum size for a cluster
    fig = plt.figure(figsize=(7, 4), dpi=600)

    # Population
    dataItem = 'CHN_HomeDensity'
    fr = open('%s%s_pccaAreas' % (dataPath, dataItem), 'rb')
    pccaClusterAreas = pickle.load(fr)  # <thres, <cluster_id, cluster_area>>
    fr.close()

    thres = []  # potential thresholds
    totalPercolations = []  # largest cluster size under each potential threshold (results of all clusters)
    largePercolatinos = []  # largest cluster size under each potential threshold (results of clusters > 20km2)
    totalEntropys = []  # distribution entropy under each potential threshold (results of all clusters)
    largeEntropys = []  # distribution entropy under each potential threshold (results of clusters > 20km2)

    # mobile phone estimated population is only a sample of the whole population
    # scale up the data with a factor derived by (national population) / (number of mobile phone users in the sample)
    popNum = 1382710000
    sampleNum = 100608611
    sFactor = popNum/sampleNum

    count = 0
    for t in sorted(list(pccaClusterAreas.keys())):
        if int(t / 10.0) != count or t > 200:
            continue
        thres.append(t * sFactor)
        count += 1

        totalSizes = np.array(list(pccaClusterAreas[t].values()))  # all clusters

        tmps = []
        for s in totalSizes:
            if s > minSize:
                tmps.append(s)
        largeSizes = np.array(tmps)  # clusters > 20km2

        totalSizes.sort()
        largeSizes.sort()

        totalAreas = totalSizes.sum()
        totalEntropy = 0.0
        for s in totalSizes:
            p = s / totalAreas
            totalEntropy = totalEntropy - p * log(p)

        largeAreas = largeSizes.sum()
        largeEntropy = 0.0
        for s in largeSizes:
            p = s / largeAreas
            largeEntropy = largeEntropy - p * log(p)

        totalPercolations.append(totalSizes[len(totalSizes) - 1] / totalSizes.sum())
        largePercolatinos.append(largeSizes[len(largeSizes) - 1] / largeSizes.sum())
        totalEntropys.append(totalEntropy)
        largeEntropys.append(largeEntropy)

    totaldIndex = 40 * sFactor   # optimal threshold for population
    largedIndex = 40 * sFactor   # optimal threshold for population

    ax_percolation = fig.add_subplot(231)   # percolation_display
    ax_percolation.plot(thres, largePercolatinos, c=largeColor, marker='.', markersize=mSize, label='Small removal', lineWidth=lWidth)
    ax_percolation.plot(thres, totalPercolations, c=totalColor, lineStyle=(0, (2, 1)), marker='^', markersize=mSize/2, label='All', lineWidth=lWidth)
    ax_percolation.axvline(largedIndex, c='black', lineWidth=1)
    ax_percolation.axvline(totaldIndex, c='black', lineStyle=(0, (2, 1)), lineWidth=lWidth)
    ax_percolation.tick_params(labelsize=legSize)
    ax_percolation.set_xticks(np.arange(0, 3000, 500))
    ax_percolation.set_ylim(0, 0.6)
    ax_percolation.set_ylabel('Largest cluster', fontsize=textSize)
    ax_percolation.set_title('Population', fontsize=textSize)
    ax_percolation.legend(loc=0, fontsize=legSize)

    ax_entropy = fig.add_subplot(234)
    ax_entropy.plot(thres, largeEntropys, c=largeColor, marker='.', markersize=mSize, label='Small removal', lineWidth=lWidth)
    ax_entropy.plot(thres, totalEntropys, c=totalColor, lineStyle=(0, (2, 1)), marker='^', markersize=mSize/2, label='All', lineWidth=lWidth)
    ax_entropy.axvline(largedIndex, c='black', lineWidth=1)
    ax_entropy.axvline(totaldIndex, c='black', lineStyle=(0, (2, 1)), lineWidth=lWidth)
    largeMax = max(largeEntropys)
    totalMax = max(totalEntropys)
    ax_entropy.axhline(largeMax, c='gray', lineStyle=':', lineWidth=lWidth)
    ax_entropy.axhline(totalMax, c='gray', lineStyle=':', lineWidth=lWidth)
    ax_entropy.tick_params(labelsize=legSize)
    ax_entropy.set_xticks(np.arange(0, 3000, 500))
    ax_entropy.set_xlabel('Population per $km^2$', fontsize=textSize)
    ax_entropy.set_ylabel('Entropy', fontsize=textSize)
    ax_entropy.set_ylim(0.0, 9.0)
    ax_entropy.legend(loc=4, fontsize=legSize)

    # road network
    dataItem = 'CHN_JuncDensity'
    fr = open('%s%s_pccaAreas' % (dataPath, dataItem), 'rb')
    pccaClusterAreas = pickle.load(fr)
    fr.close()

    thres = []
    totalPercolations = []
    largePercolatinos = []
    totalEntropys = []
    largeEntropys = []

    count = 0
    for t in sorted(list(pccaClusterAreas.keys())):
        if int(t / 5.0) != count or t > 100:
            continue
        count += 1
        thres.append(t)

        totalSizes = np.array(list(pccaClusterAreas[t].values()))

        tmps = []
        for s in totalSizes:
            if s > minSize:
                tmps.append(s)
        largeSizes = np.array(tmps)

        totalSizes.sort()
        largeSizes.sort()

        totalAreas = totalSizes.sum()
        totalEntropy = 0.0
        for s in totalSizes:
            p = s / totalAreas
            totalEntropy = totalEntropy - p * log(p)

        largeAreas = largeSizes.sum()
        largeEntropy = 0.0
        for s in largeSizes:
            p = s / largeAreas
            largeEntropy = largeEntropy - p * log(p)

        totalPercolations.append(totalSizes[len(totalSizes) - 1] / totalSizes.sum())
        largePercolatinos.append(largeSizes[len(largeSizes) - 1] / largeSizes.sum())
        totalEntropys.append(totalEntropy)
        largeEntropys.append(largeEntropy)

    totaldIndex = 20   # optimal threshold for road
    largedIndex = 20   # optimal threshold for road

    ax_percolation = fig.add_subplot(232)
    ax_percolation.plot(thres, largePercolatinos, c=largeColor, marker='.', markersize=mSize, label='Small removal', lineWidth=lWidth)
    ax_percolation.plot(thres, totalPercolations, c=totalColor, lineStyle=(0, (2, 1)), marker='^', markersize=mSize/2, label='All', lineWidth=lWidth)
    ax_percolation.axvline(largedIndex, c='black', lineWidth=1)
    ax_percolation.axvline(totaldIndex, c='black', lineStyle=(0, (2, 1)), lineWidth=lWidth)
    ax_percolation.tick_params(labelsize=legSize)
    ax_percolation.set_xticks(np.arange(0, 120, 20))
    ax_percolation.set_title('Road', fontsize=textSize)
    ax_percolation.set_ylim(0.0, 0.9)
    ax_percolation.set_ylabel('Largest cluster', fontsize=textSize)
    ax_percolation.legend(loc=0, fontsize=legSize)

    ax_entropy = fig.add_subplot(235)
    ax_entropy.plot(thres, largeEntropys, c=largeColor, marker='.', markersize=mSize, label='Small removal', lineWidth=lWidth)
    ax_entropy.plot(thres, totalEntropys, c=totalColor, lineStyle=(0, (2, 1)), marker='^',  markersize=mSize/2, label='All', lineWidth=lWidth)
    ax_entropy.axvline(largedIndex, c='black', lineWidth=1)
    ax_entropy.axvline(totaldIndex, c='black', lineStyle=(0, (2, 1)), lineWidth=lWidth)
    largeMax = max(largeEntropys)
    totalMax = max(totalEntropys)
    ax_entropy.axhline(largeMax, c='gray', lineStyle=':', lineWidth=lWidth)
    ax_entropy.axhline(totalMax, c='gray', lineStyle=':', lineWidth=lWidth)
    ax_entropy.tick_params(labelsize=legSize)
    ax_entropy.set_xlabel('Intersections per $km^2$', fontsize=textSize)
    ax_entropy.set_ylabel('Entropy', fontsize=textSize)
    ax_entropy.set_ylim(0.0, 9.0)
    ax_entropy.legend(loc=4, fontsize=legSize)

    # nighttime light
    dataItem = 'CHN_VIIRS2016'
    fr = open('%s%s_pccaAreas' % (dataPath, dataItem), 'rb')
    pccaClusterAreas = pickle.load(fr)
    fr.close()

    thres = []
    totalPercolations = []
    largePercolatinos = []
    totalEntropys = []
    largeEntropys = []

    for t in sorted(list(pccaClusterAreas.keys())):
        if t > 20:
            continue
        thres.append(t)

        totalSizes = np.array(list(pccaClusterAreas[t].values()))

        tmps = []
        for s in totalSizes:
            if s > minSize:
                tmps.append(s)
        largeSizes = np.array(tmps)

        totalSizes.sort()
        largeSizes.sort()

        totalAreas = totalSizes.sum()
        totalEntropy = 0.0
        for s in totalSizes:
            p = s / totalAreas
            totalEntropy = totalEntropy - p * log(p)

        largeAreas = largeSizes.sum()
        largeEntropy = 0.0
        for s in largeSizes:
            p = s / largeAreas
            largeEntropy = largeEntropy - p * log(p)

        totalPercolations.append(totalSizes[len(totalSizes) - 1] / totalSizes.sum())
        largePercolatinos.append(largeSizes[len(largeSizes) - 1] / largeSizes.sum())
        totalEntropys.append(totalEntropy)
        largeEntropys.append(largeEntropy)

    totaldIndex = 3   # optimal threshold for nighttime light
    largedIndex = 3   # optimal threshold for nighttime light

    ax_percolation = fig.add_subplot(233)
    ax_percolation.plot(thres, largePercolatinos, c=largeColor, marker='.', markersize=mSize, label='Small removal', lineWidth=lWidth)
    ax_percolation.plot(thres, totalPercolations, c=totalColor, lineStyle=(0, (2, 1)), marker='^', markersize=mSize/2, label='All', lineWidth=lWidth)
    ax_percolation.axvline(largedIndex, c='black', lineWidth=1)
    ax_percolation.axvline(totaldIndex, c='black', lineStyle=(0, (2, 1)), lineWidth=lWidth)
    ax_percolation.tick_params(labelsize=legSize)
    ax_percolation.set_xticks(np.arange(0, 25, 5))
    ax_percolation.set_title('Nighttime light', fontsize=textSize)
    ax_percolation.set_ylabel('Largest cluster', fontsize=textSize)
    ax_percolation.set_ylim(0.0, 0.6)
    ax_percolation.legend(loc=0, fontsize=legSize)

    ax_entropy = fig.add_subplot(236)
    ax_entropy.plot(thres, largeEntropys, c=largeColor, marker='.', markersize=mSize, label='Small removal', lineWidth=lWidth)
    ax_entropy.plot(thres, totalEntropys, c=totalColor, lineStyle=(0, (2, 1)), marker='^', markersize=mSize/2, label='All', lineWidth=lWidth)
    ax_entropy.axvline(largedIndex, c='black', lineWidth=1)
    ax_entropy.axvline(totaldIndex, c='black', lineStyle=(0, (2, 1)), lineWidth=lWidth)
    largeMax = max(largeEntropys)
    totalMax = max(totalEntropys)
    ax_entropy.axhline(largeMax, c='gray', lineStyle=':', lineWidth=lWidth)
    ax_entropy.axhline(totalMax, c='gray', lineStyle=':', lineWidth=lWidth)
    ax_entropy.tick_params(labelsize=legSize)
    ax_entropy.set_xticks(np.arange(0, 25, 5))
    ax_entropy.set_xlabel('DN value', fontsize=textSize)
    ax_entropy.set_ylabel('Entropy', fontsize=textSize)
    ax_entropy.set_ylim(0.0, 9.0)
    ax_entropy.legend(loc=4, fontsize=legSize)

    fig.tight_layout()
    fig.savefig('PCCA_CHN.eps', bbox_inches='tight', dpi=600, pad_inches=0.0)

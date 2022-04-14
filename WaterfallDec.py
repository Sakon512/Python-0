import math
from itertools import *
import numpy as np
import pandas as pd

df = pd.read_csv('waterfall2.csv', sep=';', header=None)
combinatorArr = []
answer = []


def single_revenue(cpm, impressions):
    return cpm * impressions / 1000


npCpmImpArr = np.array(df)
for i in combinations(npCpmImpArr, 3):
    combinatorArr.append(i)
npCombinatorsArr = np.array(combinatorArr)


def delete_net(arr, k):
    if k < len(arr)-1:
        arr[k+1][1] = arr[k+1][1] + arr[k][1]
    return np.array(np.delete(arr, k, 0))


def waterfall_revenue(cpmImpArr):
    totRev = 0
    for p in cpmImpArr:
        totRev += p[0] * p[1] / 1000
    return totRev


totRev = 0
totRevPrev = 0
newWaterfall = []
for i in npCombinatorsArr:
    k = 0
    rowCount = 0
    curNpCpmImpArr = np.array(npCpmImpArr)
    for j in npCpmImpArr:
        if j[0] == i[k][0]:
            # print(j[0], "=", i[k][0], jCount)
            if rowCount < len(curNpCpmImpArr):
                curNpCpmImpArr = delete_net(curNpCpmImpArr, rowCount)
                rowCount -=1
            k = k + 1
        if k==3:
            totRev = waterfall_revenue(curNpCpmImpArr)
            if totRev > totRevPrev:
                answer = i
                totRevPrev = totRev
                newWaterfall = curNpCpmImpArr
            break
        rowCount += 1
        # if rowCount < 9: rowCount += 1
print(answer)
newWaterfall = np.array(newWaterfall)
print(newWaterfall)
newRevArr = []
for i in newWaterfall:
    newRevArr.append(np.round(i[0]*i[1] / 1000, 0))
newRevArr = np.array(newRevArr)
print(newRevArr)
newWaterfall = np.insert(newWaterfall, 2, newRevArr, axis=1)
print(newWaterfall)
newWaterfallDF = pd.DataFrame(newWaterfall)
newWaterfallDF.to_csv('New Waterfall.csv',sep=";", header=["CPM", "Impressions", "Revenue"], index=None)


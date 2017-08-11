import numpy as np
import random
import time


def UpdateCentroids(matTraining, matCodebook, vecPartition, K):
    
    N = int(np.mat(matCodebook).size / K)
    M = int(np.mat(matTraining).size / K)
    
    vecQty = np.zeros(N)
    
    for i in range(M):
        vecQty[int(vecPartition[i])] += 1
        
    for i in range(N):
        if(vecQty[i] > 0):
            for j in range(K):
                matCodebook[i][j] = 0
                
    for i in range(M):
        for j in range(K):
            matCodebook[int(vecPartition[i])][j] += matTraining[i][j]
            
    for i in range(N):
        if(vecQty[i] > 0):
            for j in range(K):
                matCodebook[i][j] = matCodebook[i][j] / vecQty[i]

    return matCodebook


def AverageDistortion(matTraining, matCodebook, vecPartition, K):
    
    dist = 0
    M = int(np.mat(matTraining).size / K)
    
    for i in range(M):
        for j in range(K):
            dist += (matCodebook[int(vecPartition[i])][j] - matTraining[i][j]) * (matCodebook[int(vecPartition[i])][j] - matTraining[i][j])

    return dist / (K * M)


def Partioning(matTraining, matCodebook, K):
    
    M = int(np.mat(matTraining).size / K)
    N = int(np.mat(matCodebook).size / K)
    
    vecPartition = np.zeros(M)
    
    for i in range(M):
        dist = 1e20
        
        for j in range(N):
            aux = 0
            
            for k in range(K):
                aux += (matCodebook[j][k] - matTraining[i][k]) * (matCodebook[j][k] - matTraining[i][k])
                
                if(aux > dist):
                    break
                
            if(aux < dist):
                dist = aux
                vecPartition[i] = j
    
    return vecPartition


def VectorQuantization(matTraining, N, K):
    
    matCodebook = RandomCodebook(matTraining, N, K)
    
    previousDist = 1e20
    
    while True:
        vecPartition = Partioning(matTraining, matCodebook, K)
        currentDist = AverageDistortion(matTraining, matCodebook, vecPartition, K)
        
        if(currentDist == 0 or (previousDist - currentDist) / previousDist < 0.001):
            break
        
        previousDist = currentDist
        
        UpdateCentroids(matTraining, matCodebook, vecPartition, K)

    return matCodebook


def RandomCodebook(matTraining, N, K):
    
    M = int(np.mat(matTraining).size / K)
    matCodebook = np.zeros((N, K))
    random.seed(time.clock())    
    
    for i in range(N):
        index = random.randint(0, M - 1)
        
        for j in range(K):
            matCodebook[i][j] = matTraining[index][j]
    
    return matCodebook


def PSNR(orig, quant, K):
    
    M = int(np.mat(orig).size / K)
    dim = 256
    seg = 128
    varxyseg = 0
    c = 0
    
    orig_seg = np.zeros(dim * dim)
    quant_seg = np.zeros(dim * dim)
    x = np.zeros(seg)
    y = np.zeros(seg)
    
    for i in range (M):
        for j in range(K):
            orig_seg[c] = orig[i][j]
            quant_seg[c] = quant[i][j]
            c += 1
    
    for j in range(0, dim * dim, seg):
        for i in range(seg):
            x[i] = orig_seg[j + 1]
            
        for i in range(seg):
            y[i] = quant_seg[j + 1]
            
        for i in range(seg):
            varxyseg += (x[i] - y[i]) * (x[i] - y[i])
    
    snrtotal = 10 * (np.log10(255 * 255) - np.log10(varxyseg/(256 * 256)))
    
    return snrtotal


def Encode(matCodebook, matTraining, K):
    
    M = int(np.mat(matTraining).size / K)
    
    vecPartition = np.zeros(M)
    
    for i in range(M):
        vecPartition[i] = SearchNearestNeighbor(matCodebook, matTraining[i], K);
    
    return vecPartition


def SearchNearestNeighbor(matCodebook, vec, K):

    N = int(np.mat(matCodebook).size / K)
    
    dist = SquaredRootDistance(matCodebook[0], vec, K);
    index = 0;
    
    for i in range (1, N):
        currentDist = SquaredRootDistance(matCodebook[i], vec, K)
        
        if(dist > currentDist):
            dist = currentDist
            index = i
    
    return index


def SquaredRootDistance(x, y, K):
    
    dist = 0

    for i in range(K):
        dist += (x[i] - y[i]) * (x[i] - y[i])

    dist = np.sqrt(dist);

    return dist


def Decode(matCodebook, vecPartition, K):
    
    M = int(np.array(vecPartition).size)
    
    data = np.zeros((M, K))
    
    for i in range(M):
        for j in range(K):
            data[i][j] = matCodebook[int(vecPartition[i])][j]
    
    return data


def ReconstructImage(matCodebook, vecPartition, K, width, height):

    M = int((width * height) / K)
    block = int(np.sqrt(K))
    image = np.zeros((width, height))
    
    x_aux = y_aux = 0

    for i in range(M):
        k = 0

        for y in range(block):
            for x in range(block):
                image[y + y_aux * block][x + x_aux * block] = matCodebook[int(vecPartition[i])][k];
                k += 1
                
        x_aux += 1

        if(x_aux == 64):
            x_aux = 0
            y_aux += 1

    return image


def LoadImageToBlocks(path, size):
    
    return 0
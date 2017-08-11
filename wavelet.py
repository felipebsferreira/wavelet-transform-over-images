import numpy as np
import util


def CreateHaarMatrix(dim):

#==============================================================================
#     Cria matriz 'dim' x 'dim' com os coeficientes da transformada de Haar.
#==============================================================================

    haarMatrix = np.zeros((int(dim), int(dim)))

    col = 0

    for x in range(int(dim / 2)):
        haarMatrix[x][col] = np.sqrt(2) / 2
        haarMatrix[x][col + 1] = np.sqrt(2) / 2

        haarMatrix[x + int(dim / 2)][col] = -np.sqrt(2) / 2
        haarMatrix[x + int(dim / 2)][col + 1] = np.sqrt(2) / 2
        col += 2

    return haarMatrix


def HaarTransform(image, iterating = 1, width = 256, height = 256):
    
#==============================================================================
#     Aplica a transformada de Haar na imagem 'image' utilizando a matriz
#     definida em 'haarMat'.
#==============================================================================
    
    result = image.copy()
    
    for level in range(iterating):
        width_aux = int(width / (np.power(2, level)))
        height_aux = int(height / (np.power(2, level)))
        
        aux = np.zeros((width_aux, height_aux))
        
        for y in range(height_aux):
            for x in range(width_aux):
                aux[x][y] = result[x][y]
        
        haarMat = CreateHaarMatrix(width_aux)
        aux = np.dot(haarMat, aux)
        haarMat = CreateHaarMatrix(height_aux)
        aux = np.dot(aux, haarMat.T)
        
        for y in range(height_aux):
            for x in range(width_aux):
                result[x][y] = aux[x][y]
    
    return result


def InverseHaarTransform(image, iterating = 1, width = 256, height = 256):
    
#==============================================================================
#     Aplica a transformada de Haar na imagem 'image' utilizando a matriz
#     definida em 'haarMat'.
#==============================================================================
    
    result = image.copy()
    
    for level in range(iterating - 1, -1, -1):
        width_aux = int(width / (np.power(2, level)))
        height_aux = int(height / (np.power(2, level)))
        
        aux = np.zeros((width_aux, height_aux))
        
        for y in range(height_aux):
            for x in range(width_aux):
                aux[x][y] = result[x][y]
        
        haarMat = CreateHaarMatrix(width_aux)
        aux = np.dot(haarMat.T, aux)
        haarMat = CreateHaarMatrix(height_aux)
        aux = np.dot(aux, haarMat)
        
        for y in range(height_aux):
            for x in range(width_aux):
                result[x][y] = aux[x][y]
    
    return result


def SaveHaarTransformImage(path, level):
    
#==============================================================================
#     Carrega a imagem do caminho 'path', aplica a transformada de Haar em 
#     'level' níveis e salva o resultado como imagem PGM e como arquivo de
#     dados DAT, usando para recuperação da imagem original no caminho 'path' 
#     adicionando o sufixo 'haar' no nome do arquivo.
#==============================================================================
    
    (image, width, height) = util.LoadImage(path)
    
    result = HaarTransform(image, level, width, height)
    
    util.WriteImage(str(path).split(".pgm")[0] + '_' + str(level) + '_haar.pgm', 
                  result, width, height)
    util.WriteFile(str(path).split(".pgm")[0] + '_' + str(level) + '_haar.dat', 
                  result, width, height)


def SaveInverseHaarTransformImage(path, level):
    
#==============================================================================
#     Carrega a imagem do caminho 'path', aplica a transformada inversa de 
#     Haar em 'level' níveis e salva o resultado no caminho 'path' adicionando 
#     o sufixo 'haar' no nome do arquivo.
#==============================================================================
    
    (image, width, height) = util.LoadFile(path)
    
    result = InverseHaarTransform(image, level, width, height)
    
    util.WriteImage(str(path).split(".pgm")[0] + '_' + str(level) + '_inv_haar.pgm', 
                  result, width, height)
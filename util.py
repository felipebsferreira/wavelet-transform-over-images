import numpy as np


def LoadImage(path):

#==============================================================================
#     Carregar imagem de formato PGM, no caminho 'path', em uma matriz
#     'width' x 'height' desconsiderando o cabeçalho.
#==============================================================================

    file = open(path, 'rt')

    file.readline()
    (width, height) = [int(i) for i in file.readline().split()]
    file.readline()

    data = file.readlines()
    file.close()
    
    image = np.zeros((width, height))
    x = y = 0

    for line in data:
        for i in line.split():
            image[x][y] = int(i)

            x += 1

            if(x >= width):
                x = 0
                y += 1

    return image, width, height
            
            
def LoadFile(path):

#==============================================================================
#     Carregar imagem de formato DAT, no caminho 'path', em uma matriz
#     'width' x 'height'.
#==============================================================================

    file = open(path, 'rt')

    (width, height) = [int(i) for i in file.readline().split()]

    data = file.readlines()
    file.close()
    
    image = np.zeros((width, height))
    x = y = 0

    for line in data:
        for i in line.split():
            image[x][y] = float(i)

            x += 1

            if(x >= width):
                x = 0
                y += 1

    return image, width, height


def LoadDat(path, M, K):

#==============================================================================
#     Carregar imagem de formato DAT, no caminho 'path', em uma matriz
#     'width' x 'height'.
#==============================================================================

    file = open(path, 'rt')

    data = file.readlines()
    file.close()
    
    image = np.zeros((M, K))
    x = y = 0

    for line in data:
        for i in line.split():
            image[y][x] = float(i)

            x += 1

            if(x >= K):
                x = 0
                y += 1

    return image


def WriteImage(path, image, width, height):
    
#==============================================================================
#     Salva a imagem em disco no caminho 'path' no formato PGM.
#==============================================================================

    file = open(path, 'wt')
    
    file.write('P2\n')
    file.write(str(width) + " ")
    file.write(str(height) + " \n")
    
    highest = 0
    
    for y in range(height):
        for x in range(width):
            if(image[x][y] > highest):
                highest = int(image[x][y])
                
    file.write(str(highest) + "\n")
    
    for y in range(height):
        for x in range(width):
            value = int(image[x][y])
            
            if(value < 0):
                value = 0
                
            file.write(str(value) + " ")

    file.close()
    

def WriteFile(path, image, width, height):
    
#==============================================================================
#     Salva os dados, da imagem transformada, em disco no caminho 'path'.
#==============================================================================

    file = open(path, 'wt')
    
    file.write(str(width) + " ")
    file.write(str(height) + " \n")
    
    for y in range(height):
        for x in range(width):
            value = image[x][y]
            file.write(str(value) + " ")

    file.close()
    

def ConvertToBlocks(image, width, height, K):
    
    M = int(np.mat(image).size / K)
    
    blocks = np.zeros((M, K))
    size = int(np.sqrt(K))
    
    x = y = 0
    
    for i in range(0, height, size):
           for j in range(0, height, size):
               for yaux in range (i, size + i):
                   for xaux in range(j, size + j):
                       blocks[y][x] = image[yaux][xaux]
                       
                       x += 1
                       
                       if(x >= K):
                           x = 0
                           y += 1
    
    return blocks
            
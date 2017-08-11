import numpy as np
import wavelet as wave
import util
import vq


def RunQuantization(path, N, K):
    
    (image, width, height) = util.LoadImage(path)
    matTraining = util.ConvertToBlocks(image, width, height, K)
    
    matCodebook = vq.VectorQuantization(matTraining, N, K)
    
    encodedImage = vq.Encode(matCodebook, matTraining, K)
    quantizedImage = vq.Decode(matCodebook, encodedImage, K)
    
    psnr = vq.PSNR(matTraining, quantizedImage, K)
    reconstructedImage = vq.ReconstructImage(matCodebook, encodedImage, K, width, height)
    
    return psnr, reconstructedImage


def RunWaveletQuantization(path, iterating, N, K):
    
    (image, width, height) = util.LoadImage(path)
    
    transformedImg = wave.HaarTransform(image, iterating, width, height)
    
#==============================================================================
#     Level 3 Shape 0
#==============================================================================
    
    width_aux = int(width / (np.power(2, 3)))
    height_aux = int(height / (np.power(2, 3)))
    
    shape = np.zeros((width_aux, height_aux))
    
    for y in range(height_aux):
        for x in range(width_aux):
            shape[x][y] = transformedImg[x][y]
    
    matTraining = util.ConvertToBlocks(shape, width_aux, height_aux, K)

    matCodebook = vq.VectorQuantization(matTraining, N, K)
    
    encodedImage = vq.Encode(matCodebook, matTraining, K)
    quantizedImage = vq.Decode(matCodebook, encodedImage, K)
    
    for y in range(height_aux):
        for x in range(width_aux):
            shape[x][y] = shape[x][y]
            
#    for level in range(iterating, 1, -1):
#        width_aux = int(width / (np.power(2, level)))
#        height_aux = int(height / (np.power(2, level)))
#            
#        for shape in range(4):
#            
#            matTraining = util.ConvertToBlocks(image, width, height, K)
#    
#            matCodebook = vq.VectorQuantization(matTraining, N, K)
#            
#            encodedImage = vq.Encode(matCodebook, matTraining, K)
#            quantizedImage = vq.Decode(matCodebook, encodedImage, K)
#            
#            
#    
#    
#    psnr = vq.PSNR(matTraining, quantizedImage, K)
#    reconstructedImage = vq.ReconstructImage(matCodebook, encodedImage, K, width, height)
    
    return psnr, reconstructedImage
    

def RunWaveletTransform(level, image):
    
    wave.SaveHaarTransformImage('images/' + image + '.pgm', level)
#    wave.SaveInverseHaarTransformImage('images/' + image + '_' + str(level)
#                                     + '_haar.dat', level)

#==============================================================================
# Aplicar wavelet na imagem e salvar os resultados
#==============================================================================
    
RunWaveletTransform(2, 'libelula')


#==============================================================================
# Aplicar quantização vetorial sem e com aplicação prévia de wavelet
#==============================================================================

#imageName = 'boat'
#N = 256
#K = 16
#
#(psnr, image) = RunQuantization('images/' + imageName + '.pgm', N, K)
#util.WriteImage('images/quantizadas/' + imageName + '_vq_' + str(N) + '.pgm', image, 256, 256)
#print(psnr)

#(psnr, image) = RunQuantization('images/' + imageName + '.pgm', N, K)
#util.WriteImage('images/quantizadas/' + imageName + '_wave_' + str(N) + '.pgm', image, 256, 256)
#print(psnr)

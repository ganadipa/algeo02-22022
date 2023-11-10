from PIL import Image
from CBIR_Color import NewtonSqrt
from math import sqrt
from math import log10

""" Actual Stuff """
# Grayscale rgb conversion
def GrayScaleValue(R: int, G: int, B: int) -> float:
    return int(0.29 * R + 0.587 * G + 0.114 * B)


# Do stuff
def CalculateGLCMMatrix(img: Image) -> list[list[int]]:

    # Declare stuff
    glcmMatrix = [[0 for i in range(256)] for j in range(256)]
    glcmMatrixTranspose = [[0 for i in range(256)] for j in range(256)]

    # Load stuff
    img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()

    # Process stuff
    for y in range(1, height):
        for x in range(1, width):


            R,G,B = pixels[x, y]
            Y1 = GrayScaleValue(R,G,B)

            R,G,B = pixels[x - 1, y - 1]
            Y2= GrayScaleValue(R,G,B)

            glcmMatrix[Y1][Y2] += 1
            glcmMatrixTranspose[Y2][Y1] += 1

    # Add glcm with glcm^T
    for i in range(256):
        for j in range(256):
            glcmMatrix[i][j] += glcmMatrixTranspose[i][j]

    return glcmMatrix

# Calculate contrast using info from GLCM
def calculateContrast(GLCM : list[list[int]]) -> float:
    
    contrast = 0
    for i in range(256):
        for j in range(256):

            contrast += (GLCM[i][j] * (i - j) * (i - j))

    return contrast

# Calculate Homogeneity using info from GLCM
def calculateHomogeneity(GLCM : list[list[int]]) -> float:
    
    homogeneity = 0
    for i in range(256):
        for j in range(256):

            homogeneity += (GLCM[i][j] / (1 + ((i - j) * (i - j))))

    return homogeneity

# Calculate contrast using info from GLCM
def calculateEntropy(GLCM : list[list[int]]) -> float:
    
    entropy = 0
    for i in range(256):
        for j in range(256):
            
            if GLCM[i][j] != 0:
                entropy += (GLCM[i][j] * log10(GLCM[i][j]))

    return (-entropy)


# For the purposes of this program, the length is pre conditioned to be 3
def cosineSimilarity(vector1 : list[float], vector2 : list[float]) -> float:

    dot_product = 0
    vectorlength1 = 0
    vectorlength2 = 0

    for i in range(1, 3):
        dot_product += (vector1[i] * vector2[i])
        vectorlength1 += (vector1[i] * vector1[i])
        vectorlength2 += (vector2[i] * vector2[i])

    result = (dot_product / (sqrt(vectorlength1) * sqrt(vectorlength2)))

    return result


# Texture Similarity (main function)
def similarityTexture(img1 : Image, img2 : Image) -> float:
    
    # Build Gray-Level Co-occurence matrix
    GLCM1 = CalculateGLCMMatrix(img1)
    GLCM2 = CalculateGLCMMatrix(img2)

    # Calculate contrast, homogeneity, and entropy of both images
    contrast1 = calculateContrast(GLCM1)
    homogeneity1 = calculateHomogeneity(GLCM1)
    entropy1 = calculateEntropy(GLCM1)
    contrast2 = calculateContrast(GLCM2)
    homogeneity2 = calculateHomogeneity(GLCM2)
    entropy2 = calculateEntropy(GLCM2)
    
    # Store them as 2 vectors
    CHEvector1 = [contrast1, homogeneity1, entropy1]
    CHEvector2 = [contrast2, homogeneity2, entropy2]

    print(CHEvector1)
    print(CHEvector2)

    # Cosine similarity the vectors
    result = cosineSimilarity(CHEvector1, CHEvector2)

    return result


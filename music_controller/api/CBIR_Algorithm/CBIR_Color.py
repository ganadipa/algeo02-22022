from PIL import Image
import os

""" Biar gk rusak """
# Saya pun tidak tahu kenapa, tetapi kemarin saya coba img nya kalau ngga diginiin dulu
# programnya gak mau run jadi yasudah. -Aldy


def biarGakRusak(img: Image):
    return img.convert('RGB')


""" RGB, HSV, Color, and Index/Color bin conversion """
# Definisi fungsi-fungsi untuk COLOR QUANTIZATION -> memindah RGB values ke 36 bin color
# Terdiri dari warna grayscale dibagi jadi 4, dan warna biasa ada 16 dikali 2 varian (gelap terang)
# Total ada 4 + 16*2 = 36 possible warna

# RGB to HSV. Mengembalikan three tuple (h,s,v) untuk sebuah RGB


def RGBtoHSV(R: int, G: int, B: int) -> (int, int, int):
    R = float(R / 255)
    G = float(G / 255)
    B = float(B / 255)

    CMax = max([R, G, B])
    CMin = min([R, G, B])
    delta = CMax - CMin

    hue = 'Okusawa'
    saturation = 'Misaki'
    value = 'Waifu Terbaik'  # Deklarasi :D

    # Value for hue
    if delta == 0:
        hue = 0
    elif CMax == R:
        hue = 60 * mod6((G - B) / delta)
    elif CMax == G:
        hue = 60 * (2 + (B - R) / delta)
    else:  # CMax == B
        hue = 60 * (4 + (R - G) / delta)

    # Value for saturation
    if delta == 0:
        saturation = 0
    else:
        saturation = delta / CMax

    # Value for value
    value = CMax

    return (hue, saturation, value)

# Define quantify hue to color (belum dibagi jadi gelap terang)


def HueToColor(h: int) -> str:

    if ((0 <= h <= 10) or (355 <= h <= 369)):
        return "Red"
    elif 11 <= h <= 20:
        return "RedOrange"
    elif 21 <= h <= 40:
        return "OrangeBrown"
    elif 41 <= h <= 50:
        return "OrangeYellow"
    elif 51 <= h <= 60:
        return "Yellow"
    elif 61 <= h <= 80:
        return "YellowGreen"
    elif 81 <= h <= 140:
        return "Green"
    elif 141 <= h <= 169:
        return "GreenCyan"
    elif 170 <= h <= 200:
        return "Cyan"
    elif 201 <= h <= 220:
        return "CyanBlue"
    elif 221 <= h <= 240:
        return "Blue"
    elif 241 <= h <= 280:
        return "BlueMagenta"
    elif 281 <= h <= 320:
        return "Magenta"
    elif 321 <= h <= 330:
        return "MagentaMink"
    elif 331 <= h <= 345:
        return "Pink"
    elif 346 <= h <= 355:
        return "PinkRed"

# Defined for when saturation is 0 or greyscale


def GreyScaleColor(v: int) -> str:
    if (v < 0.2):
        return "Black"
    elif (0.2 <= v < 0.5):
        return "DarkGray"
    elif (0.5 <= v < 0.9):
        return "LightGray"
    elif (0.9 <= v <= 1):
        return "White"
    else:
        print("Uh oh, what happened here???")

# Mengembalikan indeks atau bin untuk sebuah warna tertentu.


def ColorToIndex(color: str) -> int:
    if color == "Red":
        return 0
    if color == "RedOrange":
        return 1
    if color == "OrangeBrown":
        return 2
    if color == "OrangeYellow":
        return 3
    if color == "Yellow":
        return 4
    if color == "YellowGreen":
        return 5
    if color == "Green":
        return 6
    if color == "GreenCyan":
        return 7
    if color == "Cyan":
        return 8
    if color == "CyanBlue":
        return 9
    if color == "Blue":
        return 10
    if color == "BlueMagenta":
        return 11
    if color == "Magenta":
        return 12
    if color == "MagentaMink":
        return 13
    if color == "Pink":
        return 14
    if color == "PinkRed":
        return 15

    if color == "Black":
        return 0
    if color == "DarkGray":
        return 1
    if color == "LightGray":
        return 2
    if color == "White":
        return 3

# Define HSV to Index


def HSVToIndex(h: int, s: int, v: int) -> int:
    color = ''

    if s < 0.15:
        color = GreyScaleColor(v)
    else:
        color = HueToColor(h)

    return ColorToIndex(color)

# Ultimately, this is what we will use
#####   Define RGB to Index   #####


def RGBToIndex(r: int, g: int, b: int) -> int:
    h, s, v = RGBtoHSV(r, g, b)
    return HSVToIndex(int(h), s, v)


""" Utility Functions """
# Normalize vector
# Recieves a vector in the form of a list and returns a normalized version of the vector


def normalize(vector: list[float]) -> list[float]:
    vectorLength = 0

    for i in range(len(vector)):
        vectorLength += (vector[i] * vector[i])

    vectorLength = NewtonSqrt(vectorLength)

    for i in range(len(vector)):
        vector[i] /= vectorLength

    return vector

# Define mod 6 for RGB to HSV function:
# if n is -6 < n < 0, then we want to use n + 6 instead


def mod6(n: float) -> float:
    return n if n > 0 else (n + 6)

# Newton SQRT biar keren (cuman nambah ~100an operasi, it's fine...)


def NewtonSqrt(num: float):

    result = num/2  # initial guess
    for i in range(30):
        result = result - (((result * result) - num) / (2 * result))

    return result


""" Calculation Functions """
# Single block Cosine Similarity
# Obviously, pra kondisi: dimensi image harus lebih besar dari dimensi start/end dari block


def calculateBlockSimilarity(image1: Image, image2: Image,
                             start_x1, start_y1, end_x1, end_y1,
                             start_x2, start_y2, end_x2, end_y2) -> float:

    # Load stuff
    image1 = biarGakRusak(image1)
    image2 = biarGakRusak(image2)
    pixels1 = image1.load()
    pixels2 = image2.load()

    # compression values; increase to increase spatial averaging -> higher performance with lower acc
    # (value of 1 means images are not compressed at all)
    compression_x = 3
    compression_y = 3

    # Calculate HSV Histogram / freq table for image 1
    LightColors1 = [0 for i in range(16)]
    DarkColors1 = [0 for i in range(16)]
    GreyScaleColors1 = [0 for i in range(4)]

    for y in range(start_y1, end_y1 - compression_y, compression_y):
        for x in range(start_x1, end_x1 - compression_x, compression_x):

            # Access pixel color and allocate to {r,g,b}
            r, g, b = pixels1[x, y]
            h, s, v = RGBtoHSV(r, g, b)
            # Get color code for that particular RGB
            idx = HSVToIndex(int(h), s, v)

            if s < 0.15:                          # Increment frequency of that color by +1
                GreyScaleColors1[idx] += 1
                if idx == 1 or idx == 2:
                    GreyScaleColors1[idx-1] += 0.19628
                    GreyScaleColors1[idx+1] += 0.19628
            else:
                if v > 0.7:
                    LightColors1[idx] += 1
                    LightColors1[(idx - 1) % 16] += 0.499
                    LightColors1[(idx + 1) % 16] += 0.499
                    DarkColors1[idx] += 0.5
                    DarkColors1[(idx - 1) % 16] += 0.2499
                    DarkColors1[(idx + 1) % 16] += 0.2499
                else:
                    DarkColors1[idx] += 1
                    DarkColors1[(idx - 1) % 16] += 0.499
                    DarkColors1[(idx + 1) % 16] += 0.499
                    LightColors1[idx] += 0.5
                    LightColors1[(idx - 1) % 16] += 0.2499
                    LightColors1[(idx + 1) % 16] += 0.2499

    # Di sini kita "increment sorrounding colors by weight"

    # Calculate HSV Histogram / freq table for image 2
    # Process is the same as image 1
    LightColors2 = [0 for i in range(16)]
    DarkColors2 = [0 for i in range(16)]
    GreyScaleColors2 = [0 for i in range(4)]

    for y in range(start_y2, end_y2 - compression_y, compression_y):
        for x in range(start_x2, end_x2 - compression_x, compression_x):

            r, g, b = pixels2[x, y]
            h, s, v = RGBtoHSV(r, g, b)
            idx = HSVToIndex(int(h), s, v)

            if s < 0.15:
                GreyScaleColors2[idx] += 1
                if idx == 1 or idx == 2:
                    GreyScaleColors2[idx-1] += 0.19628
                    GreyScaleColors2[idx+1] += 0.19628
            else:
                if v > 0.7:
                    LightColors2[idx] += 1
                    LightColors2[(idx - 1) % 16] += 0.499
                    LightColors2[(idx + 1) % 16] += 0.499
                    DarkColors2[idx] += 0.5
                    DarkColors2[(idx - 1) % 16] += 0.2499
                    DarkColors2[(idx + 1) % 16] += 0.2499
                else:
                    DarkColors2[idx] += 1
                    DarkColors2[(idx - 1) % 16] += 0.499
                    DarkColors2[(idx + 1) % 16] += 0.499
                    LightColors2[idx] += 0.5
                    LightColors2[(idx - 1) % 16] += 0.2499
                    LightColors2[(idx + 1) % 16] += 0.2499

    # Create 36 feature vector
    color_vector1 = []
    color_vector2 = []

    for i in range(16):
        color_vector1.append(LightColors1[i])
        color_vector2.append(LightColors2[i])

    for i in range(16):
        color_vector1.append(DarkColors1[i])
        color_vector2.append(DarkColors2[i])

    for i in range(4):
        color_vector1.append(GreyScaleColors1[i])
        color_vector2.append(GreyScaleColors2[i])

    # Normalize vector
    color_vector1 = normalize(color_vector1)
    color_vector2 = normalize(color_vector2)

############################
    """ DEBUGGING """
############################
    # print("Color data: ")
    # for i in range(0,16,1):
    #     print(f"i = {i}: ", "{:.4f}".format(colors1[i]), "{:.4f}".format(colors2[i]))

    # print()
    # print("Greyscale: ")
    # for i in range(16,20,1):
    #     print(f"i = {i}: ", "{:.4f}".format(colors1[i]), "{:.4f}".format(colors2[i]))

    # print()

    # Calculate color frequency similarity
    # (karena sudah di-normalize, dot product adalah sama dengan cosine similarity
    # karena panjang kedua vektor sudah 1 jadi tidak harus dibagi lagi)
    dot_product = 0
    for i in range(36):
        dot_product += (color_vector1[i] * color_vector2[i])

    return dot_product


# COLOR SIMILARITY MAIN FUNCTION
# The main function: Calculate similarity for each 3x3 block and multiply them with
# their respective weight
# The blocks are the following: (numbered from 1 to 3 based on their weight)
# 1 2 2 3
# 4 5 5 6
# 4 5 5 6
# 7 8 8 9

def similarityColor(image1: Image, image2: Image) -> float:
    width1, height1 = image1.size
    width2, height2 = image2.size

    m = 4
    k = 3

    WQ1_img1 = width1 // m
    WQ3_img1 = k * (width1 // m)

    HQ1_img1 = height1 // m
    HQ3_img1 = k * (height1 // m)

    WQ1_img2 = width2 // m
    WQ3_img2 = k * (width2 // m)

    HQ1_img2 = height2 // m
    HQ3_img2 = k * (height2 // m)

    result = 0
    # Blocks 1, 3, 7, and 9 (corners)
    block1 = calculateBlockSimilarity(image1, image2,
                                      0, 0, WQ1_img1, HQ1_img1,
                                      0, 0, WQ1_img2, HQ1_img2)

    block1 += calculateBlockSimilarity(image1, image2,
                                       WQ3_img1, 0, width1, HQ1_img1,
                                       WQ3_img2, 0, width2, HQ1_img2)

    block1 += calculateBlockSimilarity(image1, image2,
                                       0, HQ3_img1, WQ1_img1, height1,
                                       0, HQ3_img2, WQ1_img2, height2)

    block1 += calculateBlockSimilarity(image1, image2,
                                       WQ3_img1, HQ3_img1, width1, height1,
                                       WQ3_img2, HQ3_img2, width2, height2)

    # Blocks 2, 4, 6, and 8 (edges)
    block2 = calculateBlockSimilarity(image1, image2,
                                      WQ1_img1, 0, WQ3_img1, HQ1_img1,
                                      WQ1_img2, 0, WQ3_img2, HQ1_img2)

    block2 += calculateBlockSimilarity(image1, image2,
                                       WQ1_img1, HQ3_img1, WQ3_img1, height1,
                                       WQ1_img2, HQ3_img2, WQ3_img2, height2)

    block2 += calculateBlockSimilarity(image1, image2,
                                       0, HQ1_img1, WQ1_img1, HQ3_img1,
                                       0, HQ1_img2, WQ1_img2, HQ3_img2)

    block2 += calculateBlockSimilarity(image1, image2,
                                       WQ3_img1, HQ1_img1, width1, HQ3_img1,
                                       WQ3_img2, HQ1_img2, width2, HQ3_img2)

    # Block 5 (middle)
    block3 = calculateBlockSimilarity(image1, image2,
                                      WQ1_img1, HQ1_img1, WQ3_img1, HQ3_img1,
                                      WQ1_img2, HQ1_img2, WQ3_img2, HQ3_img2)

    #  4            4               1
    result = (block1) + (block2 * 2) + (block3 * 8)
    # print("Block 1 =",block1 / 4)
    # print("Block 2 =",block2 / 8)
    # print("Block 3 =",block3)
    return (result / 20)

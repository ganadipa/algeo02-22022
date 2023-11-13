from PIL import Image
from api.CBIR_Algorithm.caching import *
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


def calculateBlockVector(image1: Image, start_x, start_y, end_x, end_y) -> list[float]:

    # Load stuff
    image1 = biarGakRusak(image1)
    pixels1 = image1.load()

    # compression values; increase to increase spatial averaging -> higher performance with lower acc
    # (value of 1 means images are not compressed at all)
    compression_x = 3
    compression_y = 3

    # Calculate HSV Histogram / freq table for image 1
    LightColors = [0 for i in range(16)]
    DarkColors = [0 for i in range(16)]
    GreyScaleColors = [0 for i in range(4)]

    for y in range(start_y, end_y - compression_y, compression_y):
        for x in range(start_x, end_x - compression_x, compression_x):

            # Access pixel color and allocate to {r,g,b}
            r, g, b = pixels1[x, y]
            h, s, v = RGBtoHSV(r, g, b)
            # Get color code for that particular RGB
            idx = HSVToIndex(int(h), s, v)

            if s < 0.15:                          # Increment frequency of that color by +1
                GreyScaleColors[idx] += 1
                if idx == 1 or idx == 2:
                    GreyScaleColors[idx-1] += 0.19628
                    GreyScaleColors[idx+1] += 0.19628
            else:
                if v > 0.7:
                    LightColors[idx] += 1
                    LightColors[(idx - 1) % 16] += 0.499
                    LightColors[(idx + 1) % 16] += 0.499
                    DarkColors[idx] += 0.5
                    DarkColors[(idx - 1) % 16] += 0.2499
                    DarkColors[(idx + 1) % 16] += 0.2499
                else:
                    DarkColors[idx] += 1
                    DarkColors[(idx - 1) % 16] += 0.499
                    DarkColors[(idx + 1) % 16] += 0.499
                    LightColors[idx] += 0.5
                    LightColors[(idx - 1) % 16] += 0.2499
                    LightColors[(idx + 1) % 16] += 0.2499

    # Di sini kita "increment sorrounding colors by weight"

    # Create 36 feature vector
    color_vector = []

    for i in range(16):
        color_vector.append(LightColors[i])

    for i in range(16):
        color_vector.append(DarkColors[i])

    for i in range(4):
        color_vector.append(GreyScaleColors[i])

    # Normalize vector
    color_vector = normalize(color_vector)

    return color_vector


# RETURNS NEW DATA AFTER WRITING NEW IMG'S DATUM
def writeImageBlockVectors(data, path_img1):

    image = Image.open(path_img1)
    width1, height1 = image.size

    m = 4
    k = 3

    # Weight Quartile 1 and 3
    WQ1_img = width1 // m
    WQ3_img = k * (width1 // m)

    # Height Quartile 1 and 3
    HQ1_img = height1 // m
    HQ3_img = k * (height1 // m)

    # Blocks 1, 3, 7, and 9 (corners)
    color_vector1 = calculateBlockVector(image, 0, 0, WQ1_img, HQ1_img)

    color_vector3 = calculateBlockVector(image, WQ3_img, 0, width1, HQ1_img)

    color_vector7 = calculateBlockVector(image, 0, HQ3_img, WQ1_img, height1)

    color_vector9 = calculateBlockVector(
        image, WQ3_img, HQ3_img, width1, height1)

    # Blocks 2, 4, 6, and 8 (edges)
    color_vector2 = calculateBlockVector(image, WQ1_img, 0, WQ3_img, HQ1_img)

    color_vector4 = calculateBlockVector(
        image, WQ1_img, HQ3_img, WQ3_img, height1)

    color_vector6 = calculateBlockVector(image, 0, HQ1_img, WQ1_img, HQ3_img)

    color_vector8 = calculateBlockVector(
        image, WQ3_img, HQ1_img, width1, HQ3_img)

    # Block 5 (middle)
    color_vector5 = calculateBlockVector(
        image, WQ1_img, HQ1_img, WQ3_img, HQ3_img)

    hash_val = custom_hash(abspath_image=path_img1)
    # print("\n\n\n\n\n\n\n\n\n\\n\n\n\n\n\n\n\n")
    # print(hash_val)
    # print("\n\n\n\n\n\n\n\n\n\\n\n\n\n\n\n\n\n")

    append_hash_and_9arrays(data, hash_val,
                            color_vector1,
                            color_vector2,
                            color_vector3,
                            color_vector4,
                            color_vector5,
                            color_vector6,
                            color_vector7,
                            color_vector8,
                            color_vector9)


def dotProduct(color_vector1: list[float], color_vector2: list[float]) -> float:

    result = 0
    for i in range(36):
        result += (color_vector1[i] * color_vector2[i])

    return result


def similarityColor(path_img1: str, path_img2: str, data) -> float:

    idx1 = get_index_by_abspath_image(data, path_img1)
    # bugnya di sini i guess karena kalo lu append data baru bisa aja idx 1 berubah.
    if (idx1 == -1):
        writeImageBlockVectors(data, path_img1)
        # idx1 = get_index_by_abspath_image(data, path_img1)

    idx2 = get_index_by_abspath_image(data, path_img2)
    if (idx2 == -1):
        writeImageBlockVectors(data, path_img2)
        idx2 = get_index_by_abspath_image(data, path_img2)

    idx1 = get_index_by_abspath_image(data, path_img1)

    color_vectors1 = data[idx1]['attribute']
    color_vectors2 = data[idx2]['attribute']

    similarity = 0

    for i in range(9):
        color_vector1 = color_vectors1[f"array_{i+1}"]
        color_vector2 = color_vectors2[f"array_{i+1}"]

        block_similarity = dotProduct(color_vector1, color_vector2)

        if (i+1) in [1, 3, 7, 9]:
            similarity += block_similarity

        elif (i+1) in [2, 4, 6, 8]:
            similarity += (2 * block_similarity)

        else:
            similarity += (9 * block_similarity)

    similarity /= 21

    return similarity

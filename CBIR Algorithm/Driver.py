from CBIR_Color import *
from CBIR_Texture import *
from fileLoader import *
import time


# main
key = input("Test 2 images (L) or tes a directory and a query (R): ")
parent = "C:\\Users\\Aldy\\Desktop\\archive\\dataset500img\\" # GANTI INI KE DIRECTORY FOLDER IMAGESET
filenames = loadFolder(parent)
images = loadImages(filenames)

if key == 'R':
    similarity_values = []
    query_img = input("Input query image name: ")
    query_img = Image.open(parent + query_img)

    start = time.time()

    for i in range(len(filenames)):

        val = similarityColor(query_img, images[i]) # Mode warna
        # val = similarityTexture(query_img, images[i]) # Mode tekstur

        similarity_values.append(val)

    for i in range(len(filenames)):
        for j in range(len(filenames)):
            if similarity_values[i] > similarity_values[j]:
                similarity_values[i], similarity_values[j] = similarity_values[j], similarity_values[i]
                filenames[i], filenames[j] = filenames[j], filenames[i]

    for i in range(len(filenames)):
        if i != 0:
            print(f"{i}:", filenames[i], "{:.2f}".format(similarity_values[i] * 100))


    end = time.time()
    print(f"Time elapsed: ", end = "")
    print("{:.2f}".format(1000* (end-start)), end = " ")
    print("ms")

else:
    # For testing 2 images only
    
    img1 = input("Image 1 filename (with extension): ")
    img2 = input("Image 2 filename (with extension): ")
    img1 = Image.open(parent + img1)
    img2 = Image.open(parent + img2)

    print("Similarity of these 2 images: ", end = "")

    start = time.time()

    print("{:.2f}".format(100 * similarityColor(img1, img2)), end = " "); print("%")

    end = time.time()
    print(f"Time elapsed: ", end = "")
    print("{:.2f}".format(1000 * (end-start)), end = " ")
    print("ms")
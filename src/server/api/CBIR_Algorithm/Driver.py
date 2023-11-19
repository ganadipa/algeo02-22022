from api.CBIR_Algorithm.CBIR_Color import *
from api.CBIR_Algorithm.CBIR_Texture import *
from api.CBIR_Algorithm.fileLoader import *
from api.CBIR_Algorithm.caching import *
from api.CBIR_Algorithm.texture_caching import *
import time
import os


def getSimiliarity(query, isTexture, NUM_THREAD, isScraping):
    if (isTexture):
        cache = get_texture_cache()
    else:
        cache = get_cache()

    parent = os.path.abspath("./") + '\\public\\'
    dataset_files = loadFolder(parent + "\\dataset_images\\")
    dataset_images = loadImages(dataset_files)
    startTime = time.time()
    similarity_values = []

    # ```revisi aldy -> bikin list baru buat result files nya
    result_dataset_files = list()

    if (isTexture):
        for i, img in enumerate(dataset_images):
            val = similarityTextureV2(
                query, dataset_files[i], cache)
            if val >= 0.6 - isScraping:
                similarity_values.append(val)
                result_dataset_files.append(dataset_files[i])

    else:
        for i, img in enumerate(dataset_images):
            val = similarityColor(
                query, dataset_files[i], cache)
            if val >= 0.6 - isScraping:
                similarity_values.append(val)
                result_dataset_files.append(dataset_files[i])



    # SORTING

    for i in range(len(result_dataset_files)):
        for j in range(len(result_dataset_files)):
            if similarity_values[i] > similarity_values[j]:
                similarity_values[i], similarity_values[j] = similarity_values[j], similarity_values[i]
                result_dataset_files[i], result_dataset_files[j] = result_dataset_files[j], result_dataset_files[i]

    dataset_files_relative_path = [0 for i in range(len(result_dataset_files))]
    for i in range(len(result_dataset_files)):
        path = result_dataset_files[i].split('\\')
        dataset_files_relative_path[i] = '/' + \
            path[len(path)-2] + '/' + path[len(path)-1]

    endTime = time.time()
    if (isTexture):
        update_texture_database(cache)
    else:
        update_database(cache)

    print(dataset_files_relative_path)

    return {
        "duration": endTime-startTime,
        "similiarity_arr": similarity_values,
        "dataset": dataset_files_relative_path
    }


# main
if __name__ == "__main__":
    key = input("Test 2 images (L) or tes a directory and a query (R): ")
    # GANTI INI KE DIRECTORY FOLDER IMAGESET
    parent = "C:\\Users\\Aldy\\Desktop\\archive\\dataset500img\\"
    filenames = loadFolder(parent)
    images = loadImages(filenames)

    if key == 'R':
        similarity_values = []
        query_img = input("Input query image name: ")
        query_img = Image.open(parent + query_img)

        start = time.time()

        for i in range(len(filenames)):

            val = similarityColor(query_img, images[i])  # Mode warna
            # val = similarityTexture(query_img, images[i]) # Mode tekstur

            similarity_values.append(val)

        for i in range(len(filenames)):
            for j in range(len(filenames)):
                if similarity_values[i] > similarity_values[j]:
                    similarity_values[i], similarity_values[j] = similarity_values[j], similarity_values[i]
                    filenames[i], filenames[j] = filenames[j], filenames[i]



        end = time.time()
        print(f"Time elapsed: ", end="")
        print("{:.2f}".format(1000 * (end-start)), end=" ")
        print("ms")

    else:
        # For testing 2 images only

        img1 = input("Image 1 filename (with extension): ")
        img2 = input("Image 2 filename (with extension): ")
        img1 = Image.open(parent + img1)
        img2 = Image.open(parent + img2)

        print("Similarity of these 2 images: ", end="")

        start = time.time()

        print("{:.2f}".format(100 * similarityColor(img1, img2)), end=" ")
        print("%")

        end = time.time()
        print(f"Time elapsed: ", end="")
        print("{:.2f}".format(1000 * (end-start)), end=" ")
        print("ms")

from api.CBIR_Algorithm.CBIR_Color import *
from api.CBIR_Algorithm.CBIR_Texture import *
from api.CBIR_Algorithm.fileLoader import *
import time
import os
from api.CBIR_Algorithm.CustomThreading import CustomThread


def getSimiliarity(query, isTexture):
    parent = os.path.abspath("./") + '\\public\\'
    dataset_files = loadFolder(parent + "\\dataset_images\\")
    dataset_images = loadImages(dataset_files)
    query_img = Image.open(query)
    start = time.time()
    similarity_values = []

    # ```revisi aldy -> bikin list baru buat result files nya
    result_dataset_files = list()

    def inside_loop(i: int):
        print(f"starting i: {i}")
        if (not isTexture):
            val = similarityColor(query_img, dataset_images[i])  # Mode warna
        else:
            val = similarityTexture(
                query_img, dataset_images[i])  # Mode tekstur
        if val >= 0.6:
            similarity_values.append(val)
            result_dataset_files.append(dataset_files[i])  # ```revisi aldy
        print(f"ending i: {i}")

    # multithreading
    i = [0]
    length_dataset: int = len(dataset_files)

    def thread_workload():
        while i[0] < length_dataset:
            t = CustomThread(target=inside_loop, args=(i[0],))
            t.start()
            i[0] += 1
            t.join()

    NUM_THREAD = 8
    for j in range(NUM_THREAD):
        thread_workload()

    # for i in range(0, length_dataset, 5):
    #     t1 = CustomThread(target=inside_loop, args=(i,))
    #     t1.start()

    #     if (i+1 < length_dataset):
    #         t2 = CustomThread(target=inside_loop, args=(i+1,))
    #         t2.start()

    #     if (i+2 < length_dataset):
    #         t3 = CustomThread(target=inside_loop, args=(i+2,))
    #         t3.start()

    #     if (i+3 < length_dataset):
    #         t4 = CustomThread(target=inside_loop, args=(i+3,))
    #         t4.start()

    #     if (i+4 < length_dataset):
    #         t5 = CustomThread(target=inside_loop, args=(i+4,))
    #         t5.start()

    #     t1.join()
    #     if (i+1 < length_dataset):
    #         t2.join()
    #     if (i+2 < length_dataset):
    #         t3.join()
    #     if (i+3 < length_dataset):
    #         t4.join()
    #     if (i+4 < length_dataset):
    #         t5.join()

    # dataset_files = dataset_files[:len(similarity_values)] # gak gini gan -Aldy
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

    for i in range(len(result_dataset_files)):
        if i != 0:
            print(f"{i}:", result_dataset_files[i], "{:.2f}".format(
                similarity_values[i] * 100))

    end = time.time()
    return {
        "duration": end-start,
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

        for i in range(len(filenames)):
            if i != 0:
                print(f"{i}:", filenames[i], "{:.2f}".format(
                    similarity_values[i] * 100))

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

from api.CBIR_Algorithm.CBIR_Color import *
from api.CBIR_Algorithm.CBIR_Texture import *
from api.CBIR_Algorithm.fileLoader import *
import time
import os
from api.CBIR_Algorithm.CustomThreading import CustomThread
from queue import Queue
from threading import Lock
from threading import Thread
from multiprocessing import Pool
def getSimiliarity(query, isTexture, NUM_THREAD):
    parent = os.path.abspath("./") + '\\public\\'
    dataset_files = loadFolder(parent + "\\dataset_images\\")
    # dataset_images = loadImages(dataset_files)
    startTime = time.time()
    similarity_values = []

    # ```revisi aldy -> bikin list baru buat result files nya
    result_dataset_files = list()

    def inside_loopTexture(i: int,img, querySomething : list[float]):
        global next_image
        # print(f"start: {i}")

        val = similarityTextureV2(
            querySomething, img)  # Mode tekstur
        if val >= 0.6:
            similarity_values.append(val)
            result_dataset_files.append(dataset_files[i])  # ```revisi aldy
        # print(f"end: {i}")
    
    def inside_loopColor(i: int,img, querySomething : Image):
        global next_image
        # print(f"start: {i}")

        val = similarityColor(querySomething, img)
        
        if val >= 0.6:
            similarity_values.append(val)
            result_dataset_files.append(dataset_files[i])
        # print(f"end: {i}")
        
    # for i in range(len(dataset_files)):
    #     inside_loop(i)
    i = [-1]
    length_dataset: int = len(dataset_files)
    def process_image(args):
        i, image_path, querySomething, isTexture = args
        img = Image.open(image_path)
        if isTexture:
            val = similarityTextureV2(querySomething, img)
        else:
            val = similarityColor(querySomething, img)
        if val >= 0.6:
            return (val, image_path)
        else:
            return None

    threads = [0 for i in range(NUM_THREAD)]
    load = [0 for i in range(NUM_THREAD)]

    # # def thread_workload(label, querySomething):
    # #     if isTexture:
    # #         for i, img in enumerate(loadImages(dataset_files)):
    # #             inside_loopTexture(i,img, querySomething)
    # #             load[label] += 1
    # #     else:
    # #         for i, img in enumerate(loadImages(dataset_files)):
    # #             inside_loopColor(i,img, querySomething)
    # #             load[label] += 1

    # # def thread_workload(label, querySomething):
    # #     while not image_queue.empty():
    # #         i, image_path = image_queue.get()
    # #         img = loadImage(image_path)
    # #         if isTexture:
    # #             inside_loopTexture(i, img, querySomething)
    # #         else:
    # #             inside_loopColor(i, img, querySomething)
    # #         load[label] += 
    global next_image
    next_image = 0
    lock = Lock()
    def thread_workload(label, querySomething):
        global next_image
        while True:
            with lock:
                if next_image >= len(dataset_files):
                    break  # No more images to process
                image_path = dataset_files[next_image]
                next_image += 1

            img = Image.open(image_path)
            if isTexture:
                inside_loopTexture(next_image, img, querySomething)
            else:
                inside_loopColor(next_image, img, querySomething)
            load[label] += 1

    # # make queryImg as a file in uploaded_images folder
    queryImg = Image.open(query)
    query_GLCM = CalculateGLCMMatrix(queryImg)
    query_contrast, query_homogeneity, query_entropy = calculateFeatures(query_GLCM)
    query_CHEvector = [query_contrast, query_homogeneity, query_entropy]
    # with Pool(NUM_THREAD) as p:
    #     results = p.map(process_image, [(i, image_path, query_CHEvector if isTexture else queryImg, isTexture) for i, image_path in enumerate(dataset_files)])


        # for result in results:
        #     if result is not None:
        #         val, image_path = result
        #         similarity_values.append(val)
        #         result_dataset_files.append(image_path)

    
    # # image_queue = Queue()
    # # for i, image_path in enumerate(dataset_files):
    # #     image_queue.put((i, image_path))
    
    for k in range(NUM_THREAD):
        if(isTexture):
            t = CustomThread(target=thread_workload,
                         args=(k, query_CHEvector))
        else:
            t = CustomThread(target=thread_workload,
                         args=(k, queryImg))
        t.start()
        threads[k] = t

    # for k in range(NUM_THREAD):
    #     if(isTexture):
    #         t = Thread(target=thread_workload, args=(k, query_CHEvector))
    #     else:
    #         t = Thread(target=thread_workload, args=(k, queryImg))
    #     t.start()
    #     threads.append(t)
            
    # for t in threads:
    #     t.join()

    for k in range(NUM_THREAD):
        threads[k].join()

    print(load)

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
    
    #SORTING
    
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

    endTime = time.time()
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

from api.CBIR_Algorithm.CBIR_Color import *
from api.CBIR_Algorithm.CBIR_Texture import *
from api.CBIR_Algorithm.fileLoader import *
import time


def getSimiliarity(query):
    parent = "C:\\ITB\\Semester 3\\algeo\\gana\\algeo02-22022\\public"
    dataset_files = loadFolder(parent + "\\dataset_images\\")
    dataset_images = loadImages(dataset_files)
    query_img = Image.open(query)
    start = time.time()
    similarity_values = []

    for i in range(len(dataset_files)):

        val = similarityColor(query_img, dataset_images[i]) # Mode warna
        # val = similarityTexture(query_img, images[i]) # Mode tekstur
        if val >= 0.6:
            similarity_values.append(val)

    dataset_files = dataset_files[:len(similarity_values)]
    for i in range(len(dataset_files)):
        for j in range(len(dataset_files)):
            if similarity_values[i] > similarity_values[j]:
                similarity_values[i], similarity_values[j] = similarity_values[j], similarity_values[i]
                dataset_files[i], dataset_files[j] = dataset_files[j], dataset_files[i]

    dataset_files_relative_path = [ 0 for i in range(len(dataset_files))]
    for i in range(len(dataset_files)):
        path = dataset_files[i].split('\\')
        dataset_files_relative_path[i] = '/' + path[len(path)-2] + '/' + path[len(path)-1]

    
    for i in range(len(dataset_files)):
        if i != 0:
            print(f"{i}:", dataset_files[i], "{:.2f}".format(similarity_values[i] * 100))


    
    
    end = time.time()
    return {
        "duration": end-start,
        "similiarity_arr": similarity_values,
        "dataset":dataset_files_relative_path
    }

# main
if __name__ == "__main__":
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
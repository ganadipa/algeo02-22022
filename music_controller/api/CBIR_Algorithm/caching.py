from PIL import Image
import hashlib
import os
import csv


def custom_hash(abspath_image):
    sha256 = hashlib.sha256()
    with open(abspath_image, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()


'''
type dataType = list of {
    hash: string
    attribute: {
        arr1: list dgn 36 nilai
        arr2: list dgn 36 nilai
        arr3: list dgn 36 nilai
        
        arr4: list dgn 36 nilai
        arr5: list dgn 36 nilai
        arr6: list dgn 36 nilai
        
        arr7: list dgn 36 nilai
        arr8: list dgn 36 nilai
        arr9: list dgn 36 nilai
    }
}
'''

example = [
    {
        "hash": "5b47d30988c7465e09b4ad7aefdb6556751449b1d837dcdd2a398e74ee8a597c",
        "attribute": {
            "array_1": [1 for i in range(36)],
            "array_2": [2 for i in range(36)],
            "array_3": [3 for i in range(36)],
            "array_4": [4 for i in range(36)],
            "array_5": [5 for i in range(36)],
            "array_6": [6 for i in range(36)],
            "array_7": [7 for i in range(36)],
            "array_8": [8 for i in range(36)],
            "array_9": [9 for i in range(36)],
        }
    },

    {
        "hash": "6b47d30988c7465e09b4ad7aefdb6556751449b1d837dcdd2a398e74ee8a597c",
        "attribute": {
            "array_1": [1 for i in range(36)],
            "array_2": [2 for i in range(36)],
            "array_3": [3 for i in range(36)],
            "array_4": [4 for i in range(36)],
            "array_5": [5 for i in range(36)],
            "array_6": [6 for i in range(36)],
            "array_7": [7 for i in range(36)],
            "array_8": [8 for i in range(36)],
            "array_9": [9 for i in range(36)],
        }
    },
    {
        "hash": "7b47d30988c7465e09b4ad7aefdb6556751449b1d837dcdd2a398e74ee8a597c",
        "attribute": {
            "array_1": [1 for i in range(36)],
            "array_2": [2 for i in range(36)],
            "array_3": [3 for i in range(36)],
            "array_4": [4 for i in range(36)],
            "array_5": [5 for i in range(36)],
            "array_6": [6 for i in range(36)],
            "array_7": [7 for i in range(36)],
            "array_8": [8 for i in range(36)],
            "array_9": [9 for i in range(36)],
        }
    },

]


def sort_by_hash(datum_1):
    return datum_1['hash']


def update_database(data):
    p = os.path.abspath(".\\database") + '\\'
    length = len(data)

    data.sort(key=sort_by_hash)

    with open(p+"cached_image.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow([data[i]['hash']])

    with open(p+"array1.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_1'])

    with open(p+"array2.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_2'])

    with open(p+"array3.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_3'])

    with open(p+"array4.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_4'])

    with open(p+"array5.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_5'])

    with open(p+"array6.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_6'])

    with open(p+"array7.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_7'])

    with open(p+"array8.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_8'])

    with open(p+"array9.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow(data[i]['attribute']['array_9'])


def get_index(data, hash):
    # pastiin datanya sorted karena mau pake binary search
    # if not found return -1
    lo = 0
    hi = len(data)-1
    while (lo <= hi):
        mid = (hi + lo)//2
        if (hash == data[mid]['hash']):
            return mid
        elif (hash > data[mid]['hash']):
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


def get_index_by_abspath_image(data, abspath):
    # pastiin datanya sorted karena mau pake binary search
    # if not found return -1
    hash_value = custom_hash(abspath)
    print(hash_value)
    lo = 0
    hi = len(data)-1
    while (lo <= hi):
        mid = (hi + lo)//2
        if (hash_value == data[mid]['hash']):
            return mid
        elif (hash_value > data[mid]['hash']):
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


# AP stands for absolute path


def get_array_AP(data, num_array, absolute_path):
    if (num_array < 1 or num_array > 9):
        raise ValueError("num_array mestinya diisi 1-9 bro.")
    if (not os.path.exists(absolute_path)):
        raise Exception(f"Absolute pathnya ga valid nih bray: {absolute_path}")

    idx = get_index_by_abspath_image(absolute_path)
    return data[idx]['attribute'][f'array_{num_array}']


def get_array_hash(data, num_array, hash_value):
    if (num_array < 1 or num_array > 9):
        raise ValueError("num_array mestinya diisi 1-9 bro.")
    idx = get_index(hash_value)

    if (idx == -1):
        raise Exception("Hashnya ga ada bro.")

    return data[idx]['attribute'][f'array_{num_array}']


def get_all_array_AP(data, absolute_path):
    if (not os.path.exists(absolute_path)):
        raise Exception(f"Absolute pathnya ga valid nih bray: {absolute_path}")

    idx = get_index_by_abspath_image(absolute_path)
    result = []

    for i in range(9):

        tmp = data[idx]['attribute'][f'array_{i+1}'].copy()
        result.append(tmp)

    return result


def get_all_array_hash(data, hash_value):

    idx = get_index(hash_value)
    if (idx == -1):
        raise Exception("Hashnya ga ada bro.")
    result = []

    for i in range(9):
        tmp = data[idx]['attribute'][f'array_{i+1}'].copy()
        result.append(tmp)

    return result


def get_cache():
    data = []
    p = os.path.abspath(".\\database") + '\\'

    with open(p+"cached_image.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            tmp = {"hash": row, 'attribute': {'array_1': [], 'array_2': [], 'array_3': [], 'array_4': [], 'array_5': [], 'array_6': [], 'array_7': [], 'array_8': [], 'array_9': []
                                              }}
            data.append(tmp)

    with open(p+"array1.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_1'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_1'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array2.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_2'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_2'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array3.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_3'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_3'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array4.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_4'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_4'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array5.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_5'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_5'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array6.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_6'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_6'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array7.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_7'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_7'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array8.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_8'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_8'][j] = int(value)
                j += 1

            i += 1

    with open(p+"array9.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        i = 0
        for row in csv_reader:
            data[i]['attribute']['array_9'] = [0 for i in range(36)]
            j = 0
            for value in row:
                data[i]['attribute']['array_9'][j] = int(value)
                j += 1

            i += 1

    print(data)


if __name__ == '__main__':
    root = os.path.abspath(".") + '\\'
    update_database(example)
    get_cache()

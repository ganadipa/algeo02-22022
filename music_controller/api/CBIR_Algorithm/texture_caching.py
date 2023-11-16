from api.CBIR_Algorithm.caching import *
import os
import csv


'''
type dataType = list of {
    hash: string
    attribute: list of 3 elmts where elmt1: contraset, elmt2: homogeneity, elmt3: entropy
}

'''

example = [{
    "hash": "hello-world",
    "attribute": [0.2, 0.3, 0.4]
}]


def RESET_TEXTURE_CACHE():
    p = os.path.abspath(".\\database") + '\\'

    with open(p+"texture_caching.csv", 'w', newline='') as f:
        f.truncate()


def update_texture_database(data):
    p = os.path.abspath(".\\database") + '\\'
    length = len(data)
    data.sort(key=sort_by_hash)

    with open(p+"texture_caching.csv", 'w', newline='') as f:
        for i in range(length):
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerow([data[i]['hash']]+data[i]['attribute'])


def get_index_by_abspath_image(data, abspath):
    if (len(data)) == 0:
        return -1

    # pastiin datanya sorted karena mau pake binary search
    # if not found return -1
    hash_value = custom_hash(abspath)
    # print(hash_value)
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


def get_all_array_texture_AP(data, absolute_path):
    if (not os.path.exists(absolute_path)):
        raise Exception(f"Absolute pathnya ga valid nih bray: {absolute_path}")

    idx = get_index_by_abspath_image(data, absolute_path)
    return data[idx]['attribute'].copy()


def get_texture_cache():
    data = []
    p = os.path.abspath(".\\database") + '\\'

    with open(p+"texture_caching.csv", 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            tmp = {"hash": row[0], 'attribute': [float(i) for i in (row[1:])]}
            data.append(tmp)

    return data


def append_hash_and_array_texture(data, hash_val, array):
    tmp = {
        'hash': hash_val,
        'attribute': array
    }
    old_length = len(data)

    # binary search to get the position
    lo = 0
    hi = old_length

    while (lo < hi):
        mid = (hi + lo)//2
        if (data[mid]['hash'] >= hash_val):
            if (data[mid]['hash'] == hash_val):
                return data
            hi = mid
        else:
            lo = mid + 1

    data.append(tmp)

    for i in range(len(data)-1, lo-1, -1):
        data[i] = data[i-1]
    data[lo] = tmp


def print_onlyhash(data):
    for i in range(len(data)):
        print(data[i]['hash'])


if __name__ == '__main__':
    update_texture_database(example)
    data = get_texture_cache()
    print(data)

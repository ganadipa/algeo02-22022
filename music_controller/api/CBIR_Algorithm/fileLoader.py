from PIL import Image
import os;

# Load image folder to filenames
def loadFolder(parentpath: str) -> list[str]:
    filenames = []
    extensions = [".jpg", ".jpeg", ".png"]
    for filename in os.listdir(parentpath):
        if any(filename.endswith(extension) for extension in extensions):
            filenames.append(os.path.join(parentpath, filename))

    return filenames

# Load images from filenames
# def loadImages(filenames: list[str]):
#     dataset = []
#     for filename in filenames:
#         dataset.append(Image.open(filename))
    
#     return dataset

def loadImages(filenames: list[str]):
    for filename in filenames:
        yield Image.open(filename)
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



def loadImages(filenames: list[str]):
    for filename in filenames:
        yield Image.open(filename)
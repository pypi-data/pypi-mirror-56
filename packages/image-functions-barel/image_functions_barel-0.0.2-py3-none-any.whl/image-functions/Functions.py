# standard library
import logging
from os import listdir, makedirs
from os.path import exists, isfile, isdir, join, splitext
from sys import argv, stdout
import time
from typing import Generator
# third party
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgba2rgb, rgb2gray
import cv2


###################
# LOGGING
###################

def create_log(name: str, level, out_format="[%(levelname)s] Module: %(name)s: %(message)s", filename="", filemode="w"):
    """Creates a logging object
    
    Args:
        name (str): log name
        level (level): log level
        filename (str, optional): [description]. Defaults to "".
        filemode (str, optional): [description]. Defaults to "w".
    """
    # create logger
    if level <logging.getLogger().level:
        logging.basicConfig(level=level)
    log = logging.getLogger(name)
    log.propagate = False
    log.setLevel(level)
    # decide on format
    formatter = logging.Formatter(out_format)
    # add output to stdout
    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    # add output file if needed
    if filename != "":
        file_handler = logging.FileHandler(filename, filemode)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    return log

# create log for this module
mylib_log = create_log(__name__, logging.WARN)

###################
# SHOWING IMAGES
###################

def show(*args, width: int=-1, height:int=-1, ndarray=False) -> None:
    """Gets images and desplay them.

    Images can be in a list or sent one by one.
    
    Args:
        width (int, optional): image grid width. Defaults to -1.
        height (int, optional): image grid height. Defaults to -1.
    
    Returns:
        None
    """
    mylib_log.info("Showing images")
    try:
        # handle list as input
        if len(args) == 1:
            if type(args[0]) == list:
                mylib_log.info("Got list of images")
                _show_list(args[0], width, height)
            elif type(args[0]) == np.ndarray and ndarray:
                mylib_log.info("Got ndarray")
                images = []
                for i in range(args[0].shape[0]):
                    images.append(args[0][i])
                    print(images[-1].shape)
                _show_list(images, width, height)
            else:
                mylib_log.info("Got a single image")
                plt.imshow(args[0], "gray") if len(args[0].shape) == 2 else plt.imshow(args[0])
        # handle multiple images
        elif len(args) > 1:
            mylib_log.info("Got multiple images")
            _show_list(args, width, height)
        else:
            mylib_log.error("Could not show images")
            return
        plt.show()
    except Exception as e:
        mylib_log.error(str(e))


def _show_list(images: list, width: int=-1, height: int=-1) -> None:
    """Gets list of images and display them all
    
    Args:
        images (list): list of numpy arrays
        width (int, optional): width of the image grid. Defaults to -1.
        height (int, optional): height of the image grid. Defaults to -1.
    
    Returns:
        None 
    """
    im_num = len(images)
    mylib_log.info(f"Showing {im_num} images")
    in_grid = width * height >= im_num
    if not in_grid:
        if width != -1 and height != -1:
            mylib_log.warn(
                f"Cant fit {im_num} images in a {width} by {height} grid")
        _show_line(images)
        return
    elif in_grid and (width == 1 or height == 1):
        mylib_log.info("Showing in line")
        _show_line(images, width == 1)
        return
    # showing in grid
    _, array = plt.subplots(height, width)
    for i in range(im_num):
        im = images[i]
        x = i % width
        y = int(i / width)
        array[y, x].imshow(im, "gray") if len(
            im.shape) == 2 else array[y, x].imshow(im)
       

def _show_line(images: list, horizontal: bool =True) -> None:
    """Show list of images in a straight line
    
    Args:
        images (list): list of images
    
    Returns:
        None
    """
    mylib_log.info("Showing images in a straight line")
    num_images = len(images)
    _, array = plt.subplots(
        1, num_images) if horizontal else plt.subplots(num_images)
    for i in range(num_images):
        im = images[i]
        array[i].imshow(im, "gray") if len(im.shape) == 2 else array[i].imshow(im)

###################
# PROGRESS REPORTS
###################

start = -1
elapsed = -1


def get_progress_marker(action: str, part: int, total: int, arrow_len=50, last_step=-1) -> str:
    """Return a string that shows progress
    
    Args:
        action (str): The action being performed
        part (int): the current number of actions that already finished
        total (int): the total number of actions
        arrow_len (int, optional): length of the arrow. Defaults to 50.
    
    Returns:
        str: representation of the progress
    """
    mylib_log.info("Creating progress arrow")
    full = int(part / total * arrow_len) + 1
    full_arrow = "-" * full
    empty_arrow = " " * (arrow_len - full)
    result = f"{action}: [{full_arrow}>{empty_arrow}]"
    if last_step != -1:
        estimated = last_step * (total-part)
        secs = int(estimated % 60)
        last_mins = (estimated - secs) / 60
        mins = int(last_mins % 60)
        hours = int((last_mins - mins) / 60)
        time_stamp = f"{hours:02d}:{mins:02d}:{secs:02d}"
        result += f" - {time_stamp} left"
    return result


def print_progress(action: str, part: int, total: int, end_msg="Done", arrow_len=50) -> None:
    """Prints progress nicly to screen
    
    Args:
        action (str): the action
        part (int): the current number of actions that already finished
        total (int): the total number of actions
        arrow_len (int, optional): length of the arrow. Defaults to 50.
    
    Returns:
        None: [description]
    """
    global start
    global elapsed
    # calculate elpsed time
    if start != -1:
        elapsed = time.time() - start
    end = "\r"
    done = part >= total - 1
    if done:
        end = ""
    print(get_progress_marker(action, part, total, arrow_len, elapsed), end=end)
    if done:
        # zero timer
        start = -1
        print(" - " + end_msg)
    else:
        # start timer
        start = time.time()

###################
# IMAGE CONVERTION
###################

def get_folders(path: str, full_path=False) -> list:
    """return all subfolders of a folder
    
    Args:
        path (str): path to folder
        full_path (bool, optional): add the folder joind with the path. Defaults to False.
    
    Returns:
        list: list of subfolder names
    """
    mylib_log.info(f"Getting all subfolders of {path}")
    folders = [f for f in listdir(path) if isdir(join(path, f))]
    if full_path:
        mylib_log.info(f"Adding path to foldernames of {path}")
        folders = [join(path, f) for f in folders]
    return folders


def get_files(path: str, extension: str="", full_path: bool=False) -> list:
    """return all fils with extension from folder
    
    Args:
        path (str): path to folder
        extension (str, optional): file extension, if none specified return all files. Defaults to "".
        full_path (bool, optional): add path to the file names. Defaults to False.
    
    Returns:
        list: list of files
    """
    mylib_log.info(f"Getting all files from {path}")
    # get only files
    files = [f for f in listdir(path) if isfile(join(path, f))]
    # get only files with extensions
    if extension != "":
        mylib_log.info(f"Getting only {extension} files from {path}")
        files = [f for f in files if f.endswith(extension)]
    # add path if needed
    if full_path:
        mylib_log.info(f"Adding path to filenames of {path}")
        files = [join(path, f) for f in files]
    return files


def get_all_files(path: str, extension: str="", full_path: bool=False) -> list:
    """recursivly get all files with extension from a folder and all its subfolders
    
    Args:
        path (str): path to folder
        extension (str, optional): get only files with this extension. Defaults to "".
        full_path (bool, optional): add path to output. Defaults to False.
    
    Returns:
        list: list of all files with extension
    """
    files = []
    files += get_files(path, extension, full_path)
    for folder in get_folders(path, True):
        files += get_all_files(folder, extension, full_path)
    return files


def convert_image(src: str, dst: str) -> None:
    """convert image
    
    Args:
        src (str): path to original image
        dst (str): path to new image with new extension
    
    Returns:
        None
    """
    mylib_log.info(f"Convertin {src} to {dst}")
    im = Image.open(src)
    im.save(dst)


def to_cv_format(im: np.ndarray) -> np.ndarray:
    """turns an image to uint8 in range [0, 255]
    
    Args:
        im (np.ndarray): original image
    
    Returns:
        np.ndarray: uint8 image with values in range [0, 255]
    """
    if np.amax(im) <= 1:
        im *= 255
    return cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2RGB)

###################
# IO
###################

def imread(path: str, gray: bool=False) -> np.ndarray:
    """Reads image as float array in range [0, 1]
    
    Args:
        path (str): path to image
        gray (bool, optional): convert to grayscale. Defaults to False

    Returns:
        np.ndarray: the image
    """
    mylib_log.info(f"Trying to read an image from file: {path}")
    try:
        im = plt.imread(path)
        # fix format
        im = image_to_format(im)
        # return image in correct format
        mylib_log.info(f"Image from {path} created sucssesfuly")
        return im
    except Exception as e:
        mylib_log.error(str(e))


def image_to_format(im: np.ndarray, gray: bool=False) -> np.ndarray:
    mylib_log.info("Correcting image format")
    # turn to float
    im = im.astype(np.float32)
    # correct colors
    if len(im.shape) == 3 and im.shape[2] == 4:
        mylib_log.warn(f"Convertin from RGBA to RGB - alpha is thrown")
        im = im[:, :, :3]
    if len(im.shape) == 3 and gray:
        mylib_log.info(f"Convertin from RGB to GRAY")
        im = rgb2gray(im)
    # normalize
    if np.amax(im) > 1:
        mylib_log.info(f"Normalizing to range [0, 1]")
        im /= 255.0
    return im


def video_generator(path: str, start: int) -> Generator[np.ndarray, None, None]:
    mylib_log.info(f"Creating video generator from {path}")
    try:
        capture = cv2.VideoCapture(path)
        length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if start < length or start < 0:
            capture.set(cv2.CAP_PROP_POS_FRAMES, start)
        else:
            mylib_log.error(f"Bad starting frame {start} for video with length {length}")
        for i in range(start, length):
            _, frame = capture.read()
            yield image_to_format(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    except Exception as e:
        mylib_log.error(str(e))

###################
# DEBUG
###################

if __name__ == "__main__":
    pass


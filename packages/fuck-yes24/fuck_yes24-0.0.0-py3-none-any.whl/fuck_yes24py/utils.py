import os
import shutil
import zipfile


def zipdir(path, zipf, compressFile = True):
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file)
            if compressFile:
                zipf.write(path, compress_type = zipfile.ZIP_DEFLATED)
            else:
                zipf.write(path, compress_type = zipfile.ZIP_STORED)


def zipafile(path, zipf, compressFile = True):
    if compressFile:
        zipf.write(path, compress_type = zipfile.ZIP_DEFLATED)
    else:
        zipf.write(path, compress_type = zipfile.ZIP_STORED)    


def zipdirs(paths, zip, compressFile = True):
    if os.path.isfile(zip):
        zipf = zipfile.ZipFile(zip, 'a')
    else:
        zipf = zipfile.ZipFile(zip, 'w')
    
    if type(paths) is str:
        if not os.path.isdir(paths):
            zipafile(paths, zipf, compressFile)
        else:
            zipdir(paths, zipf, compressFile)
    if type(paths) is list:
        for path in paths:
            zipdir(path, zipf, compressFile)

# TODO: DO DOCUMENTATION!!!

import os
import shutil
from urllib.parse import urlparse
import argparse
import pandas as pd
import re
import urldownload

__author__ = "Partha Das"
__version__ = "1.0.2"

def get_URLs(input_csv, column_name, downloadLocation=None, zip_location=None,
            remove_dir=False, filters=['.jpg', '.gif', '.png'], use_regex=False):


    results = open('linkDownloadReport.txt', 'w')
    with open(input_csv, 'r') as file:
        csvobject = pd.read_csv(file)

    tmpDownDir = False
    fileList = []
    searchfor = r'|'.join(filters)

    if downloadLocation is None:
        downloadLocation = 'tmp'
        tmpDownDir = True
    if zip_location is None:
        zip_location = '.'
    if not os.path.exists(downloadLocation):
        os.makedirs(downloadLocation)

    imageList = csvobject[column_name]

    for idx, item, in enumerate(imageList):
        if use_regex:
            ext = re.findall(searchfor, item)
            if len(ext) > 0:
                filename = str(idx) + ext[0]
                totalPath = os.path.join(downloadLocation, filename)
                if os.path.exists(totalPath):
                    print("[%d] Url: %s, already exists, skipping." % (idx, item))
                else:
                    print("[%d] Url: %s, Downloading..." % (idx, item), end='\r')
                    ret = urldownload.downloadImages(item, totalPath)
                    results.write(item + ', ' + str(ret) + '\n')
                    print("[%d] Url: %s, Downloaded --> %r" % (idx, item, ret))
                    if ret:
                        fileList.append(totalPath)
            else:
                print("""[%d] Url: %s \nFilter pattern not found or the link doesn't
                      link directly to the image, skipping.""" %(idx,
                                                                           item))
                results.write(item + ', False')
        else:
            parsed = urlparse(item)
            root, ext = os.path.splitext(parsed.path)
            if ext in filters:
                filename = str(idx) + ext
                totalPath = os.path.join(downloadLocation, filename)
                if os.path.exists(totalPath):
                    print("[%d] Url: %s, already exists, skipping." % (idx, item))
                else:
                    print("[%d] Url: %s, Downloading..." % (idx, item), end='\r')
                    ret = urldownload.downloadImages(item, totalPath)
                    results.write(item + ', ' + str(ret) + '\n')
                    print("[%d] Url: %s, Downloaded --> %r" % (idx, item, ret))
                    if ret:
                        fileList.append(totalPath)
            else:
                print("""[%d] Url: %s \nFilter pattern not found or the link doesn't
                      link directly to the image, skipping.""" %(idx,
                                                                           item))
                results.write(item + ', False')


    print("Downloading finished.")
    print("Creating archive....",end='\r')
    name, ext = os.path.splitext(input_csv)
    zip_name = os.path.join(zip_location, name)
    shutil.make_archive(zip_name, 'zip', downloadLocation)
    print("Collection archived at %s. Download report saved as file %s" %
          (zip_name + '.zip', 'linkDownloadReport.txt'))
    if remove_dir:
        print('Cleaning up....', end='\r')
        if tmpDownDir:
            shutil.rmtree(downloadLocation)
        else:
            for file in fileList:
                os.remove(file)
        print('Cleaned up temporary downloads!')
    results.close()

def str2bool(v):
    return v.lower() in ("false", "true")


if __name__ == '__main__':
    print("Hello world")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input csv file")
    parser.add_argument("-c", "--column", help="Name of the column which has the urls")
    parser.add_argument("-d", "--download", help="""Path to folder where the
                        downloaded files should be stored. Default is tmp,
                        at the current folder of the script. Recommended to
                        point to an empty folder in order to make the zip
                        only contain the files, otherwise it zips
                        everything in the directory.""", default=None)
    parser.add_argument("-z", "--zipLoc", help="""Location where the zipped file
                        should be saved. Only the folder is needed, the name of
                        the zip file is automatically inferred from the csv
                        input file. Default is the current folder of the
                        script.""", default=None)
    parser.add_argument("-r", "--remove", help="""Delete the folder where the
                        files were downloaded. Default is False.
                            !!!!!WARNING!!!!!: Deletes only the files that have
                        been downloaded this session. If there are files from
                        previous session, it won't be deleted""",
                        default=False, type=str2bool)
    parser.add_argument("-f", "--filter", help="""List of the filters to be
                        used. This further filters the list and downloads only
                        the links that have files with those extensions. Put
                        different filters as a space separated value.
                        Default value is .jpg .gif .png.""", nargs='+',
                        default=['.jpg', '.png', '.gif'])
    parser.add_argument("-x", "--regex", help="""Use the regex based detector
                        for the link filtering. More aggressive matcher, but
                        returns a false positives, especially for websites like
                        photobucket, where they have redirects for direct url
                        requests. Might result in files that don't open as
                        their extention should, because of the file being a
                        different thing, and just named with the extension.
                        Useful as a fallback if the default method fails on
                        links. Turned off by default.""", default=False,
                        type=str2bool)

    args = parser.parse_args()
    input = args.input
    column = args.column
    download = args.download
    zipLoc = args.zipLoc
    remove = args.remove
    filters = args.filter
    regex = args.regex

    print("Job Parameters: ")
    print("""\n\tInput file: %s\n\tTarget Column: %s\n\tDownload Location:
          %s\n\tZip Save Location: %s\n\tCleanup downloads: %r\n\tFilters:
          %s\n\tRegex Matcher: %r\n"""
                                                                   % (input,
                                                                       column,
                                                                       download,
                                                                       zipLoc,
                                                                       remove,
                                                                      """,
                                                                      """.join(filters),
                                                                      regex
                                                                      ))
    print("Job Started....\n\n")

    get_URLs(input, column, download, zipLoc, remove, filters, regex)




#    get_URLs('RC_2008-0-imageurl.csv', 'imageurl', remove_dir=True)

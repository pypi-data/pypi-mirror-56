"""
Identify TEM images from scientific articles using chemdataextractor

@author : Ed Beard

"""

from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division

from chemdataextractor import Document
import urllib
import multiprocessing as mp

import os
import csv
import io
import sys
import logging
import zipfile
import tarfile

logging.basicConfig()
log = logging.getLogger(__name__)


class TEMImageExtractor():

    def __init__(self, input, output='', typ='tem'):
        self.input = input
        self.output = output
        self.img_csv_path = str(os.path.join(self.output, os.path.basename(self.output) + '_raw.csv'))
        self.docs = []
        self.paths = []
        self.imgs = []
        self.urls = []
        self.img_type = typ

    def get_img_paths(self):
        """ Get paths to all images """

        docs = os.listdir(self.input)

        # Check for single file
        if len(docs) == 1:
            compressed = os.path.join(self.input, docs[0])

            if compressed.endswith('zip'):
                # Logic to unzip the file locally
                log.info('Opening zip file...')
                zip_ref = zipfile.ZipFile(compressed)
                zip_ref.extractall(self.input)
                zip_ref.close()

            elif compressed.endswith('tar.gz'):
                # Logic to unzip tarball locally
                log.info('Opening tarball file...')
                tar_ref = tarfile.open(compressed, 'r:gz')
                tar_ref.extractall(self.input)
                tar_ref.close()

            elif compressed.endswith('tar'):
                # Logic to unzip tarball locally
                log.info('Opening tarball file...')
                tar_ref = tarfile.open(compressed, 'r:')
                tar_ref.extractall(self.input)
                tar_ref.close()
            else:
                raise Exception('Only one file provided - please use extract_document() instead')

            log.info('Removing compressed file...')
            os.remove(compressed)
            docs = os.listdir(self.input)

        self.docs = [(doc, os.path.join(self.input, doc)) for doc in docs]

        # Create image folders if it doesn't exist
        if not os.path.exists(os.path.join(self.output, 'raw_images')):
            os.makedirs(os.path.join(self.output, 'raw_images'))

    def get_img(self, doc):
        """Get images from doc using chemdataextractor"""

        # Load document image data from file
        tem_images = []
        cde_doc = Document.from_file(open(doc[1], "rb"))
        log.info('This article is : %s' % doc[0])
        imgs = cde_doc.figures
        del cde_doc

        # Identify relevant images from records
        for img in imgs:
            detected = False  # Used to avoid processing images twice
            records = img.records
            caption = img.caption
            for record in records:
                if detected is True:
                    break

                rec = record.serialize()
                if [self.img_type] in rec.values():
                    detected = True
                    log.info('%s instance found!' % self.img_type)
                    tem_images.append((doc[0], img.id, img.url, caption.text.replace('\n', ' ')))

        if len(tem_images) != 0:
            return tem_images
        else:
            return None

    def download_image(self, url, file, id):
        """ Download all TEM images"""

        imgs_dir = os.path.join(self.output, 'raw_images')

        if len(os.listdir(imgs_dir)) <= 999999999:
            img_format = url.split('.')[-1]
            log.info(url, img_format)
            filename = file.split('.')[0] + '_' + id + '.' + img_format
            path = os.path.join(imgs_dir, filename)

            log.info("Downloading %s..." % filename)
            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path) # Saves downloaded image to file
            else:
                log.info("File exists! Going to next image")
        else:
            sys.exit()

    def save_img_data_to_file(self):
        """ Saves list of tem images"""

        imgf = open(self.img_csv_path, 'w')
        output_csvwriter = csv.writer(imgf)
        output_csvwriter.writerow(['article', 'fig id', 'url', 'caption'])

        for row in self.imgs:

            # Ignore results without a URL
            if row[2] != '':
                output_csvwriter.writerow(row)

    def get_all_tem_imgs(self, parallel=True):
        """ Get all TEM images """

        self.get_img_paths()

        # Check if TEM images info found
        if os.path.isfile(self.img_csv_path):
            with io.open(self.img_csv_path, 'r') as imgf:
                img_csvreader = csv.reader(imgf)
                next(img_csvreader)
                self.imgs = list(img_csvreader)
        else:

            # If not found, identify TEM images
            if parallel:
                pool = mp.Pool(processes=mp.cpu_count())
                tem_images = pool.map(self.get_img, self.docs)
            else:
                tem_images =[]
                for doc in self.docs:
                    try:
                        imgs = self.get_img(doc)
                        if imgs is not None:
                            tem_images.append(imgs)
                    except Exception as e:
                        log.error(e)

            self.imgs = [img for doc in tem_images if doc is not None for img in doc]

            self.save_img_data_to_file()
            log.info('%s image info saved to file' % self.img_type)

        # Download TEM images
        for file, id, url, caption in self.imgs:
            self.download_image(url, file, id)

    def get_tem_imgs(self):
        """ Get the TEM images for a single Document"""

        if not os.path.isfile(self.input):
            raise Exception('Input should be a single document for this method')

        # Create image folders if it doesn't exist
        if not os.path.exists(os.path.join(self.output, 'raw_images')):
            os.makedirs(os.path.join(self.output, 'raw_images'))

        # Check if TEM images info found
        if os.path.isfile(self.img_csv_path):
            with io.open(self.img_csv_path, 'r') as imgf:
                img_csvreader = csv.reader(imgf)
                next(img_csvreader)
                self.imgs = list(img_csvreader)
        else:
            try:
                doc = (self.input.split('/')[-1], self.input)
                self.imgs = self.get_img(doc)
            except Exception as e:
                log.error(e)

        self.save_img_data_to_file()
        log.info('%s image info saved to file' % self.img_type)

        # Download TEM images
        for file, id, url, caption in self.imgs:
            self.download_image(url, file, id)
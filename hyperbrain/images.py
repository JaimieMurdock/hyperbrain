from __future__ import print_function

from progressbar import ProgressBar, Percentage, Bar

import os, os.path
import requests
import wget
import xml.etree.ElementTree as ET

def get_image_ids():
    """ Get image ids from the Allen Brain Atlas API. """
    # build url query
    url = "http://api.brain-map.org/api/v2/data/query.xml?criteria=model::AtlasImage,"
    url += "rma::criteria,"
    url += "[annotated$eqtrue],"
    url += "atlas_data_set(atlases[id$eq265297125]),"
    url += "alternate_images[image_type$eq'Atlas+-+Human'],"
    url += "rma::options[order$eq'sub_images.section_number'][num_rows$eqall]"

    # create request object
    r = requests.get(url)

    # parse XML
    root = ET.fromstring(r.text)
    image_ids = []
    for image in root.iter('atlas-image'):
        image_id = image.find('id').text
        image_ids.append(image_id)

    return image_ids

def download_images(image_ids, output_dir=None):
    """ Downloads images from the Allen Brain Atlas. """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), '../images/')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # url builder
    url = "http://api.brain-map.org/api/v2/svg_download/{id}"
    url += "?groups=265297119,266932194,266932196,266932197&downsample=7"

    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(image_ids)).start()
    for i,image_id in pbar(enumerate(image_ids)):
        output_file = '{i:04d}_{image_id}.svg'.format(i=i,image_id=image_id)
        output_file = os.path.join(output_dir, output_file)
        wget.download(url.format(id=image_id), output_file)

# main execution of script
if __name__ == '__main__':
    image_ids = get_image_ids()

    download_images(image_ids)


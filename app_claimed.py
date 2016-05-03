import requests
import json
import sys
import urllib2
import os
import zipfile


'''
Makes Requests to Content API
Takes 2 command line arguments

argv1 = gallery_id
argv2 = access_token

*OPTIONAL PARAMETER:
argv3 = social_platform

Currently only saves 'medium_image' on line 45
'''
def make_request(page, social_platform='instagram,twitter,direct,facebook,vinetweet,tumblr'):
    BASE_URL = 'https://api.offerpop.com/v1/ugc/collections/'
    gallery_id = sys.argv[1]
    access_token = sys.argv[2]

    raw_request = requests.get(
                    BASE_URL +
                    gallery_id +
                    '?access_token=' + access_token +
                    '&page=' + str(page) +
                    '&social_platform=' + social_platform +
                    '&approval_status=app' +
                    '&media_type=image' +
                    '&claimed=yes'
    )

    parsed_request = json.loads(raw_request.text)
    handle_response(page, gallery_id, parsed_request, social_platform)

def handle_response(page, gallery_id, parsed_request, social_platform):
    for ugc in range(len(parsed_request['_embedded']['ugc:item'])):
        content = parsed_request['_embedded']['ugc:item'][ugc]['content']
        author = content['author']['username']
        created_on = content['media']['created_on']
        created_on2 = created_on.replace(":", "-");
        image_key = author + '_' + created_on2
        imagePath = content['media']['media_urls']['large_image']
        print image_key

        if image_key:
            store_images_locally(gallery_id, image_key, imagePath)

    if parsed_request['_links']['next']['href']:
        page += 1
        make_request(page, social_platform) # get next page of content
    else:
        zip_folder(gallery_id) # generate zip folder

def store_images_locally(directory, filename, imagePath):
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory + '/' + filename.replace("/", "-") + '.png', 'wb')
    f.write(urllib2.urlopen(imagePath).read())
    f.close()

'''
Functions to create zip folder locally
Folder/Zip name are created by gallery_id
'''
def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

def zip_folder(directory):
    zipf = zipfile.ZipFile(directory + '.zip', 'w')
    zipdir(directory, zipf)
    zipf.close()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        make_request(1, sys.argv[3])
    else:
        make_request(1)
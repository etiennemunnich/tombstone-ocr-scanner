'''
Process images via AWS Rekognition

@Author: Etienne Munnich
'''

import boto3
import glob
import json
import sys

# PHOTOS Directory/bucket
photo_dir = '/yourlocalfiles/photos/'
photo_bucket = 'yourbuckethere'
photo_bucket_prefix = ''

# Get files (folder)
# files = ''
# files = glob.glob(photo_dir + "*.jpg")
# files.extend(glob.glob(photo_dir + "*.JPG"))
# print('Files :'files)

# Get files (S3)
s3 = boto3.resource('s3')
bucket = s3.Bucket(photo_bucket)
s3objectnames = []
s3jsonobjectnames = []
s3jpgobjectnames = []
for obj in bucket.objects.all():
    s3objectnames.append(obj.key)
    if obj.key.find(".json") >= 0:
        s3jsonobjectnames.append(obj.key)
    if obj.key.find(".jpg") >= 0:
        s3jpgobjectnames.append(obj.key)

print("all objects " + s3objectnames.__str__())
print("jpg objects" + s3jpgobjectnames.__str__())
print("json objects" + s3jsonobjectnames.__str__())

# Client connection to AWS
try:
    myrekognition = boto3.client('rekognition', region_name='us-east-1',
        endpoint_url='https://rekognition.us-east-1.amazonaws.com')
except: # catch *all* exceptions
   e = sys.exc_info()[0]
   print( "AWS Client Connection Error: %s" % e)

# Process images
for idx, value in enumerate(s3jpgobjectnames):
    print("Processing :" + s3jpgobjectnames[idx])
    print("Value :" + value)

    #check if json exists
    if (s3jpgobjectnames[idx].rstrip('.jpg') + ".json") in s3jsonobjectnames:
        print('Skipping as json exists')
    else:
        try:
            rek_response = myrekognition.detect_text(
                Image={
                    'S3Object': {
                        'Bucket': photo_bucket,
                        'Name': s3jpgobjectnames[idx]
                        }
                    }
                )
            print(json.dumps(rek_response, sort_keys=False, indent=2).__str__())
        except:  # catch *all* exceptions
            e4 = sys.exc_info()[0]
            print("AWS Rekognition submit Error: %s" % e4)

        #write to s3
        s3newfilename = photo_bucket_prefix + s3jpgobjectnames[idx].rstrip('.jpg') + ".json"
        print('S3 New Object file name :' + s3newfilename)
        try:
            s3.Object(photo_bucket, s3newfilename).put(Body=json.dumps(rek_response, sort_keys=False, indent=2).__str__(), ServerSideEncryption='AES256')
        except:  # catch *all* exceptions
            e3 = sys.exc_info()[0]
            print("S3 write Error: %s" % e3)

        # #write file locally
        # newfilename = photo_dir + s3jpgobjectnames[idx].rstrip('.jpg') + ".json"
        # print("New object files name: " + newfilename)
        # try:
        #     with open(newfilename, 'wb') as newfilejson:
        #         filedata = json.dumps(rek_response, sort_keys=False, indent=2).__str__()
        #         newfilejson.write(filedata)
        #         print(filedata)
        #         #newfilejson.close()   Apparrently not required when ising with open.
        # except: # catch *all* exceptions
        #    e = sys.exc_info()[0]
        #    print("File write Error: %s" % e)

# Dependencies: boto3
# pip install boto3

import time
import os
import datetime
import boto3

# SET ACCORDING TO UE4 SAVE LOCATION
savefilepath = os.path.abspath('.')
savefilename = os.path.abspath('./jengastate.sav')
s3 = boto3.resource('s3')
bucket = 'jengalongdistance'
gameidkey = 'game1'
checkperiod = 15 # seconds
# to prevent infinite upload/download loop
margin = 30 # seconds

def main():
    while True:
        cloud_file = s3.Object(bucket, gameidkey)
        cloud_mtime = cloud_file.last_modified
        local_mtime = datetime.datetime.replace(datetime.datetime.fromtimestamp(os.path.getmtime(savefilename)), tzinfo=datetime.timezone(datetime.timedelta(hours=-6)))
        print()
        print('Cloud', cloud_mtime)
        print('Local', local_mtime)
        print('Cloud - Local', cloud_mtime - local_mtime)
        print('Local - Cloud', local_mtime - cloud_mtime)
        print('L - C > margin', (local_mtime - cloud_mtime) > datetime.timedelta(seconds = margin))
        print('C - L > margin', (cloud_mtime - local_mtime) > datetime.timedelta(seconds = margin))
        
        # local check
        if local_mtime - cloud_mtime > datetime.timedelta(seconds = margin):
            uploadsave()
            
        # cloud check
        if cloud_mtime - local_mtime > datetime.timedelta(seconds = margin):
            downloadsave()
        
        # check period
        time.sleep(checkperiod)
      
def uploadsave():
    data = open(savefilename, 'rb')
    s3.Bucket(bucket).put_object(Key=gameidkey, Body=data)
    data.close()
    print(savefilename, 'uploaded at', datetime.datetime.now())

def downloadsave():
    data = open(savefilename, 'wb')
    s3.Object(bucket, gameidkey).download_fileobj(data)
    data.close()
    print(savefilename, 'downloaded at', datetime.datetime.now())
    
main()
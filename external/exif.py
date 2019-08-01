#Input image and Output file 


import exiftool
import sys
import os
import json
import pprint


class Extract_Exif :
    # extensions supported
    img_extensions = ['JPEG','PNG','TIFF','JPG']

    # unwanted items
    unwanted = ["ExifToolVersion","ImageDescription"]

    def __init__(self):
        return
    
    def Extract_MetaData(self, Directory):
        img_extensions = Extract_Exif.img_extensions
        unwanted = Extract_Exif.unwanted
        listOfFiles = []
        for file in os.listdir(Directory) :
            i = file.rfind('.')
            extension = file[i+1:]
            extension  = extension.upper()
            if extension in img_extensions :
                listOfFiles.append(os.path.join(Directory,file))

        print(listOfFiles)

        Exif_Result_dict = {}

        with exiftool.ExifTool() as et:
            metadata = et.get_metadata_batch(listOfFiles)
    
        for d in metadata:
            txt = d['File:FileName']
            keys_d = d.keys()
            newkeys = list() #[]
            newdict = dict() #{}
            for s in keys_d :
                if ':' in s:
                    l=s.split(':')
                    if (l[1] in unwanted) :
                        continue
                    if (l[0] not in newdict.keys()) :
                        subdict = {}
                        subdict.update({l[1] : d[s]})
                        newdict.update({l[0] : subdict})
                    else :
                        subdict = newdict[l[0]]
                        subdict.update({l[1] : d[s]})
                        newdict.update({l[0] : subdict})
                else:
                    newdict.update({s : d[s]})
           
            Exif_Result_dict.update({txt : newdict})
            

        return Exif_Result_dict


e = Extract_Exif()
#pprint.pprint(e.Extract_MetaData('/home/sameer/Datasets/RGB/images_RGB/new'))
                                 
x = (e.Extract_MetaData('/home/sameer/Datasets/RGB/images_RGB/new'))                     


with open('Exif.json', 'w') as f:
            
#    json.dump(x,f)
    json.dump(x,f, indent=4, sort_keys = True)
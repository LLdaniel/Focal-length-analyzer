from PIL import Image, ExifTags
from matplotlib import pyplot
import numpy
import os, sys, re

#######################################################################################
class Extractor:
        def __init__(self, path, compare_path):
                self.path = path
                self.compare_path = compare_path
                self.images = self.getImages(self.path)
                self.compare_images = []
                self.compareMode = False
                if compare_path != 'None':
                        self.compareMode = True
                        self.compare_images = self.getImages(self.compare_path)
                self.focal_length = []
                self.focal_length_compare = []
        def getImages(self, whichpath):
                try:
                        return os.listdir(whichpath)
                except FileNotFoundError:
                        print('The given path "' + whichpath + '" does not exist!')
        def extract(self):
                # normal extraction
                for img in self.images:
                        #print(self.images)
                        self.focal_length.append( self.getExifData( Image.open(self.path + os.path.sep + img) ) )
                print(self.focal_length)
                # extraction for comparing directory
                if(self.compareMode):
                        for img in self.compare_images:
                                #print(self.compare_images)
                                self.focal_length_compare.append( self.getExifData( Image.open(self.compare_path + os.path.sep + img) ) )
                        print(self.focal_length_compare)
                                
        def getExifData(self, img):
                exif_data = {
                        ExifTags.TAGS[k]: v
                        for k, v in img._getexif().items()
                        if k in ExifTags.TAGS
                }
                #print(exif_data)
                #print(focal_length)
                return exif_data.get('FocalLength') #current sensor
                #return exif_data.get('FocalLengthIn35mmFilm') #35mm equiv

#######################################################################################      
class Histogram:
        def __init__(self, Extractor):
                self.Extractor = Extractor
                self.focal_length = []
                self.focal_length2 = []
                
        def plot(self):
                #print(self.Extractor.focal_length)
                self.focal_length = numpy.array(self.Extractor.focal_length)
                if(self.Extractor.compareMode):
                        self.focal_length2 = numpy.array(self.Extractor.focal_length_compare)
                fig, axis = pyplot.subplots(figsize =(10, 5))
                bins = numpy.arange(self.getMinVal(), self.getMaxVal()+1, 1)
                pyplot.title("focal length distribution (FF equivalent)")
                pyplot.xlabel("focal length [mm]")
                pyplot.ylabel("number of pictures")
                sum1 = len(self.Extractor.focal_length)
                sum2 = -1
                if(self.Extractor.compareMode):
                        sum2 = len(self.Extractor.focal_length_compare)
                pyplot.hist(self.focal_length, bins, label="collection 1 ", alpha=0.5, color='blue')
                if(self.Extractor.compareMode):
                        pyplot.text(self.getMaxVal()-10, 10, r'$\Sigma_1=%s,\ \Sigma_2=%s$'%(sum1,sum2))
                else:
                        pyplot.text(self.getMaxVal()-10, 10, r'$\Sigma_1=%s$'%(sum1))
                if(self.Extractor.compareMode):
                        pyplot.hist(self.focal_length2, bins, label="collection 2", alpha=0.5, color='red' )
                pyplot.legend()
                pyplot.show()

        def getMaxVal(self):
                if(self.Extractor.compareMode):
                        if(max(self.focal_length) >= max(self.focal_length2) ):
                                return max(self.focal_length)
                        else:
                                return max(self.focal_length2)
                else:
                        return max(self.focal_length)
        def getMinVal(self):
                if(self.Extractor.compareMode):
                        if(min(self.focal_length) <= min(self.focal_length2) ):
                                return min(self.focal_length)
                        else:
                                return min(self.focal_length2)
                else:
                        return min(self.focal_length)

###############################################################################
if __name__ == "__main__":
        extractor = None
        isValid = False
        if len(sys.argv) == 1:
                print("Pass a valid directory with images as an argument!")
        elif len(sys.argv) == 2:
                extractor = Extractor(sys.argv[1], None)
                isValid = True
        elif len(sys.argv) == 3:
                extractor = Extractor(sys.argv[1], sys.argv[2])
                isValid = True
        else:
                print("Too many arguments passed! Maximum is two directories.")

        # go on, if there is an directory to analyze
        if(isValid):
                extractor.extract()
                histo = Histogram(extractor)
                histo.plot()

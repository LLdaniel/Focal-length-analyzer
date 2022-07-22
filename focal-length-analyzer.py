from PIL import Image, ExifTags
from matplotlib import pyplot
import numpy
import os, sys, re, getopt

#######################################################################################
class Extractor:
        def __init__(self, path, compare_path, sensor):
                self.path = path
                self.compare_path = compare_path
                self.images = self.getImages(self.path)
                self.compare_images = []
                self.compareMode = False
                if(compare_path):
                        self.compareMode = True
                        self.compare_images = self.getImages(self.compare_path)
                self.focal_length = []
                self.focal_length_compare = []
                self.crop = self.getCropSize(sensor)

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

        def getCropSize(self, sensor):
                if(sensor == 'ff'):
                        print('Using full frame equivalent.')
                        return 1.0 #35mm equiv
                elif(sensor.startswith('aps-c')):
                        crop_option = re.search(r"aps-c(\d+.{0,1}\d*)", sensor)
                        crop = 1.0
                        if(crop_option.group(1)):
                                crop = crop_option.group(1)
                                print('Crop factor of "' + crop + '" assumed.')
                        else:
                                print('Wrong sensor format "' + sensor + '". Value like "aps-c1.6" expected. Using 1.6 now.')
                                crop = 1.6
                        return float(crop) #aps-c crop sensor
                else:
                        print('Using local sensor size without re-calculation.')
                        return -1
                        
        def getExifData(self, img):
                exif_data = {
                        ExifTags.TAGS[k]: v
                        for k, v in img._getexif().items()
                        if k in ExifTags.TAGS
                }
                #print(exif_data)
                #print(focal_length)
                if(self.crop < 0): # local sensor without recalculation
                        return exif_data.get('FocalLength')
                else:
                        return exif_data.get('FocalLengthIn35mmFilm')/self.crop # case = 1 -> FF | case != 1 -> aps-c sensor

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
                pyplot.title("focal length distribution (" + self.specifyTitle() + ")")
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
                
        def specifyTitle(self):
                if(self.Extractor.crop < 0):
                        return 'local sensor'
                elif(self.Extractor.crop == 1.0):
                        return 'FF equivalent'
                else:
                        return 'APS-C sensor'

###############################################################################
def helpME():
        print('usage: ./focal-length-analyzer [DIR1] <DIR2> <OPTIONS>')
        print()
        print('       <DIR2> is optional and triggers the compare mode when present')
        print()
        print('       options:')
        print('                -s, --sensor [ff|aps-c<crop>|none]    ff:          Full frame (DEFAULT)')
        print('                              ff:          Full frame (DEFAULT)')
        print('                              aps-c<crop>: APS-C sensor with <crop> factor, e.g. 1.6')
        print('                              none:        use the sensor of the image (local sensor)')
        print('                -h, --help                            show this help')


if __name__ == "__main__":
        extractor = None
        isValid = False
        sensor = 'ff'

        try:
                print( 'ARGV      :', sys.argv[1:])

                options, dirs = getopt.gnu_getopt(sys.argv[1:], 's:h', ['sensor=','help'])
                print( 'OPTIONS   :', options)

                for opt, arg in options:
                        if opt in ('-s', '--sensor'):
                                sensor = arg
                        elif opt in ('-h', '--help'):
                                helpME()
                                break
                print( 'SENSOR    :', sensor)
                if( len(dirs) == 0 ):
                        print("Pass a valid directory with images as an argument!")
                        helpME()
                elif( len(dirs) == 1 ):
                        print( 'dir1 :', dirs[0])
                        isValid = True
                        extractor = Extractor(dirs[0], None, sensor)
                elif( len(dirs) < 3 ):
                        print( 'dir1 :', dirs[0])
                        print( 'dir2 :', dirs[1])
                        isValid = True
                        extractor = Extractor(dirs[0], dirs[1], sensor)
                else:
                        print("Too many arguments passed! Maximum is two directories.")
                        helpME()
        except getopt.GetoptError:
                helpME()
                
                
        if(isValid):
                extractor.extract()
                histo = Histogram(extractor)
                histo.plot()

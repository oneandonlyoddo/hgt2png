#!/usr/bin/python
 
# hgt to png
# Jonas Otto - helloworld@jonasotto.de
# based on information found here https://gis.stackexchange.com/questions/43743/how-to-extract-elevation-from-hgt-file
# and the official SRTM Documentation https://dds.cr.usgs.gov/srtm/version2_1/Documentation/SRTM_Topo.pdf
 
import sys
import struct
from PIL import Image
 
def map(val, in_min, in_max, out_min, out_max ):
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def usage():
    print(".hgt to png converter usage: python hgt2png.py <inputfile.hgt>  <resolution 1 or 3 standard is 1>")
 
def main (argv):
    print (argv)
    data_resolution = 1
    image_resolution = 3601
    height_source_file = ""
    if len(argv) == 0:
        usage()
        sys.exit()
    if len (argv) == 1:
        if not str(argv[0]).endswith("hgt"):
            print("please supply a valid .hgt file as first argument")
            usage()
            sys.exit()
        else:
            height_source_file = argv[0]
    elif len (argv) > 1:
        if not str(argv[0]).endswith("hgt"):
            print("please supply a valid .hgt file as first argument")
            usage()
            sys.exit()
        else:
            height_source_file = argv[0]
        if argv[1] == 3:
            image_resolution = 1201
            data_resolution = 3
        elif argv[1] != 1:
            print('please supply a valid resolution of 1" or 3" as second argument. using standard of 1 arc second')
            usage()
    height_map = Image.new('RGB', (image_resolution, image_resolution))
    min_value = 0
    max_value = 0
    height_map_data_ordered = []
    height_map_data = []
    void_counter = 0
    void_value = -32768
    print ("reading in data for "+height_source_file+". applying the standard resolution of 1 arc second")
 
    with open(height_source_file, "rb") as source_file:
        print("parsing data")
        for y in range(image_resolution):
            for x in range(image_resolution):
                index = (( y * image_resolution) + x)*2
                source_file.seek( index )
                buf = source_file.read(2)
                value = struct.unpack('>h', buf)[0]
                if value != void_value:
                    height_map_data_ordered.append(value); 
                    if x==0 and y==0:
                        max_value = value
                        min_value = value
                    elif value > max_value:
                        max_value = value
                    elif value < min_value:
                        min_value = value 
                else:
                    void_counter += 1
                    height_map_data_ordered.append(0)
                    if 0 < min_value:
                        min_value = 0
    print("parsing done. there are "+str(void_counter)+" void pixels.")
    print ("final min and max values are: ", min_value, max_value)
    print ("map data to greyscale")
    for value in height_map_data_ordered:
        mapped_value = int(round(map(value,min_value,max_value,0,255)))
        height_map_data.append((mapped_value,mapped_value,mapped_value))
    print ("drawing Heightmap")
    height_map.putdata(height_map_data)
    print ("saving Heightmap")
    height_map.save("height_map_"+height_source_file+".png")
    print ("done")
 
if __name__ == "__main__":
   main(sys.argv[1:])
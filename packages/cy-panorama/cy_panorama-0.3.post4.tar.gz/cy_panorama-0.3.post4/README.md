# Panorama converter for Facebook
Panorama converter for Facebook

## TODO
1. Upload to pypi
    * https://python-packaging.readthedocs.io/en/latest/minimal.html
1. Add Stitch function

## Usage
* convert.py [-h] [-o OUTPUTIMG] [-w IMGOUTWIDTH] [-b IMGBGCOLOR] inputImage
   * inputImage: A Panorama image with Spherical projection
   * OUTPUTIMG: A Panorama image that can be accepted by Facebook
* Example: 
   * python convert.py PANO0001_stitch.jpg -o out.jpg

### Requirements of Facebook's Panaroma image:
* Image smaller than 6000×3000 pixels
* Image ratio(width:height) is 2:1
* EXIF:
   * make: RICOH
   * model: RICOH THETA S


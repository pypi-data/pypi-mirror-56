# cy_panorama
A simple panorama tool

Features:
1. convert a panorama image to a Facebook supported format

## TODO
1. Add Stitch function

## Install
`pip install cy_panorama`

## Usage
`panorama_convert_fb input.jpg -o output.jpg`

## Note
Requirements of Facebook's Panaroma image:
* Image width less than 6000 pixels
* Image ratio(width:height) is 2:1
* EXIF contains:
   * make: RICOH
   * model: RICOH THETA S


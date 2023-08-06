import logging
import piexif
from PIL import Image


class Panorama(object):
    FB_MAX_WIDTH = 6000
    FB_IMG_RATIO = 2

    DEFAULT_BG_COLOR = 'black'
    DEFAULT_OUT_WIDTH = 0  # 0: auto

    def __init__(self, img_file=None):
        self.log = logging.getLogger(self.__class__.__name__)
        self.panorama = None
        if img_file:
            self.reload_panorama(img_file)

    def reload_panorama(self, img_file=None):
        try:
            self.panorama = Image.open(img_file)
        except Exception as e:
            self.log.error(e)

    def convert_fb(self, out_file=None, bg_color=DEFAULT_BG_COLOR):
        if not self.panorama:
            self.log.error("no panorama img, call load_panorama() first!")
            return

        if not out_file:
            out_file = 'pano_fb.jpg'

        src_width, src_height = self.panorama.size
        src_ratio = float(src_width) / src_height
        out_width = \
            src_width if src_width < self.FB_MAX_WIDTH else self.FB_MAX_WIDTH
        out_height = int(float(out_width) / self.FB_IMG_RATIO)
        self.log.debug("src image size: (%s,%s), ratio: %s", src_width,
                       src_height, src_ratio)
        self.log.debug("out image size: (%s,%s)", out_width, out_height)

        out_img = Image.new('RGB', (out_width, out_height), color=bg_color)

        paste_width = out_width
        if src_ratio <= self.FB_IMG_RATIO:
            # scale to fill output
            paste_height = out_height
        else:
            # align the bottom
            paste_height = int(out_width / src_ratio)
        h_offset = out_height - paste_height
        out_img.paste(self.panorama.resize((paste_width, paste_height),
                                           Image.LANCZOS), (0, h_offset))

        # copy exif from input image, modify manufacturer/device
        exif = piexif.load(self.panorama.info["exif"])
        exif["0th"][271] = b'RICOH'
        exif["0th"][272] = b'RICOH THETA S'
        exif_bytes = piexif.dump(exif)

        out_img.save(out_file, exif=exif_bytes)

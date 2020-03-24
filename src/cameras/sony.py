from .factory import Camera
from .factory import Exposure
import re


class ILCE_7M3(Camera):

    def __init__(self, data):
        self.data = data

    def get_focal_length(self):
        f = self.data.get('Focal Length In 35mm Format', None)
        m = re.match(r'(\d+).*mm$', f)
        if m:
            return m.group(1)
        else:
            return None

    @property
    def make(self):
        return self.data.get('Make', None)

    @property
    def model(self):
        return self.data.get('Camera Model Name', None)

    @property
    def megapixels(self):
        return self.data.get('Megapixels', None)

    @property
    def software(self):
        return self.data.get('Software', None)

    @property
    def lens(self):
        return self.data.get('Lens ID', None)

    @property
    def image_size(self):
        """Tuple of with and height"""
        return (self.data.get('Sony Image Width Max', None), self.data.get('Sony Image Height Max', None))

    @property
    def exposure(self):

        e = Exposure(shutterspeed=self.data.get("Exposure Time", None),
                     iso=self.data.get("ISO", None),
                     aperture=self.data.get("F Number", None), focal_length=self.get_focal_length())
        return e

    def dump(self):
        return self.data
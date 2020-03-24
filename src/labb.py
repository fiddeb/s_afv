from src.cameras.sony import ILCE_7M3
import subprocess
import json

EXIF_PATH = "/usr/local/bin"

def read_exif(filename):
    raw_exif = subprocess.run("{}/exiftool {}".format(EXIF_PATH, filename), shell=True, stdout=subprocess.PIPE, text=True)
    return {
      key.strip(): value.strip()
      for key, value in [
        s.split(':', 1)
        for s in raw_exif.stdout.splitlines()
      ]
    }

img = "/Users/faar/Documents/Src/priv/s_afv/src/img/_A736587.ARW"
data = read_exif(img)
print(json.dumps(data, indent=4))
c = ILCE_7M3(data)
print(c.exposure.iso, c.exposure.shutterspeed, c.exposure.aperture, c.exposure.focal_length, c.exposure.ssr)

print(c.image_size)

import os
import re
import subprocess
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
from matplotlib.widgets import Button
import tkinter as tk
import tkinter.filedialog as tkFileDialog
from PIL import Image
import numpy as np
import rawpy

filename = "img/_A736587.ARW"


def norm(val):
    ret = float(val)
    ret = ret / 1000
    if ret > 1:
        ret = 1
    ret = 1 - ret
    ret = str(ret)
    return ret

class messylogics:


    def read_exif(self):
        return subprocess.run("exiftool {}".format(self.filename), shell=True, stdout=subprocess.PIPE,text=True)

    def start(self):
        self.z_status = 0
        self.file_data = f"{os.path.basename(self.filename)} ({self.pos + 1}/{len(self.flist)})"

        plt.sca(ax)
        plt.cla()
        self.ax.axis('off')
        self.fig.canvas.set_window_title(os.path.basename(self.filename))
        if '.arw' in self.filename.lower():
            rw = open(self.filename, 'rb')
            raw = rawpy.imread(rw)
            im = raw.postprocess(use_camera_wb=True, user_flip=0)
            rw.close()

        if '.jpg' in self.filename.lower():
            try:
                f = Image.open(self.filename)
                im = np.array(f, dtype=np.uint8)
                self.f.close()
            except Exception as e:
                print(e)
        self.ypixels, self.xpixels, _ = im.shape

        # F is the path to your target image file.
        self.exifdata = self.read_exif()

        ## fix base settings
        self.base_data(im)

        if 'AF Type' in self.exif:
            if self.exif.get('AF Type') in ('15-point'):
                print("printer 14")
                self.fifteen()
            if self.exif.get('AF Type') in ('19-point'):
                print("printer 13")
                self.nineteen()
            if self.exif.get('Camera Model Name') in ('ILCA-77M2', 'ILCA-99M2'):
                if 'AF Points Used' in self.exif:
                    print("printer 12")
                    self.afpoints()

        if 'Faces Detected' in self.exif and int(self.exif.get('Faces Detected', 0)) > 0:
            self.facedetect()

        if (self.exif.get('Focal Plane AF Points Used')):
            self.focal_plane_af()

        if 'Focus Location' in self.exif:
            self.focus_location()


        elif (self.exif.get('Focal Plane AF Points Used')):

            if self.exif.get('Camera Model Name') in ('ILCE-6000', 'ILCE-5100', 'ILCE-7RM2', 'ILCE-7M2'):
                if self.exif.get('AF Tracking') == 'Face tracking':
                    print("printer 8")
                    self.ax.text(self.header_xy,
                                 self.file_data + '\n' + 'Model with Focal Plane AF Points detected (' + str(
                                     self.exif.get('Camera Model Name')) + '). Focus Mode: ' + str(
                                     self.exif.get('Focus Mode')) + '\nFocal Plane AF points used = ' + str(
                                     len(self.foc)) + '\n' + 'EYE AF or Face Tracking engaged!', color='y',
                                 weight='bold', fontsize='small', ha='left', va='top')
                else:
                    print("printer 7")
                    self.ax.text(self.header_xy,
                                 self.file_data + '\n' + 'Model with Focal Plane AF Points detected (' + str(
                                     self.exif.get('Camera Model Name')) + '). Focus Mode: ' + str(
                                     self.exif.get('Focus Mode')) + '\nFocal Plane AF points used = ' + str(
                                     len(self.foc)), color='y', weight='bold', fontsize='small', ha='left', va='top')

            if self.exif.get('Camera Model Name') in (
                    'ILCE-6300', 'ILCE-6500', 'ILCA-99M2', 'ILCA-77M2', 'ILCE-9', 'DSC-RX10M4', 'DSC-RX100M5',
                    'ILCE-7RM3',
                    'ILCE-7M3', 'DSC-RX100M6', 'ILCE-6400', 'ILCE-6100', 'ILCE-6600', 'DSC-RX0', 'DSC-RX0M2',
                    'MODEL-NAME',
                    'DSC-RX100M7', 'ILCE-7RM4'):

                if self.exif.get('AF Area Mode') == 'Tracking' and self.exif.get(
                        'AF Tracking') == 'Lock On AF':  # and self.exif.get('Camera Model Name') in ('ILCE-6400','ILCE-9','ILCE-7RM4','ILCE-RX100M7'):
                    print("printer 6")
                    self.txt = self.ax.text(self.header_xy,
                                            str(os.path.basename(self.filename)) + ' (' + str(self.pos + 1) + '/' + str(
                                                len(
                                                    self.flist)) + ')\n' + 'Model with Focal Plane AF Points detected (' + str(
                                                self.exif.get('Camera Model Name')) + '). Focus Mode: ' + str(
                                                self.exif.get('Focus Mode')) + '\nFocal Plane AF points used = ' + str(
                                                self.foc) + '\n' + 'Real time object tracking used', color='y',
                                            weight='bold', fontsize='small', ha='left', va='top')

                if self.exif.get(
                        'AF Area Mode') == 'Animal Eye Tracking':  # and self.exif.get('AF Tracking') == 'Lock On AF' and self.exif.get('Camera Model Name') in ('ILCE-6400','ILCE-9','ILCE-7RM4','ILCE-RX100M7'):
                    print("printer 5")
                    self.txt = self.ax.text(self.header_xy,
                                            str(os.path.basename(self.filename)) + ' (' + str(self.pos + 1) + '/' + str(
                                                len(
                                                    self.flist)) + ')\n' + 'Model with Focal Plane AF Points detected (' + str(
                                                self.exif.get('Camera Model Name')) + '). Focus Mode: ' + str(
                                                self.exif.get('Focus Mode')) + '\nFocal Plane AF points used = ' + str(
                                                self.foc) + '\n' + 'Animal Eye AF used', color='y', weight='bold',
                                            fontsize='small', ha='left', va='top')

                if self.exif.get('AF Tracking') == 'Face tracking' and self.exif.get('AF Area Mode') == ('Tracking'):
                    print("printer 4")
                    text = f"{os.path.basename(self.filename)} ({self.pos + 1})/"
                    self.txt = self.fix_text(
                        self.ax.text(x=self.header_xy[0], y=self.header_xy[1], s=text, color='y', weight='bold',
                                     fontsize='small', ha='left', va='top'))

                if self.exif.get('AF Tracking') == 'Face tracking' and self.exif.get('AF Area Mode') == (
                'Face Tracking'):
                    print("printer 3")
                    self.txt = self.fix_text(self.ax.text(self.header_xy,
                                                          str(os.path.basename(self.filename)) + ' (' + str(
                                                              self.pos + 1) + '/' + str(len(
                                                              self.flist)) + ')\n' + 'Model with Focal Plane AF Points detected (' + str(
                                                              self.exif.get(
                                                                  'Camera Model Name')) + '). Focus Mode: ' + str(
                                                              self.exif.get(
                                                                  'Focus Mode')) + '\nFocal Plane AF points used = ' + str(
                                                              self.foc) + '\n' + 'Face Tracking used', color='y',
                                                          weight='bold', fontsize='small', ha='left', va='top'))


                else:
                    print("printer 1")
                    self.txt = self.ax.text(*self.header_xy, s=str(os.path.basename(self.filename)) + ' (' + str(
                        self.pos + 1) + '/' + str(
                        len(self.flist)) + ')\n' + 'Model with Focal Plane AF Points detected (' + str(
                        self.exif.get('Camera Model Name')) + '). Focus Mode: ' + str(
                        self.exif.get('Focus Mode')) + '\nFocal Plane AF points used = ' + str(self.foc), color='y',
                                            weight='bold', fontsize='small', ha='left', va='top')
        else:
            print("printer 0")

            text = {"x": self.header_xy[0], "y": self.header_xy[1],
                    "s": f"{os.path.basename(self.filename)} ({self.pos + 1}/ {len(self.flist)})\n "
                         f"{self.exif.get('Camera Model Name', 'None')}. Focus Mode: {self.exif.get('Focus Mode', 'None')}",
                    "color": "y", "weight": "bold", "fontsize": "small", "ha": "left", "va": "top"}

            self.add_text(**text)

        self.ax.imshow(im)

        plt.draw()


class af:
    def fifteen(self):
        for key in sorted(self.exif.items()):
            if key[0].startswith('AF Status'):
                vl = re.findall('\d+', key[1])
                if not vl:
                    vl.append('32768')
                if key[0] == 'AF Status Center Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Center Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center), self.r_size, self.r_size,
                                          linewidth=1,
                                          edgecolor='limegreen',
                                          facecolor=norm(cross),
                                          alpha=0.9))
                    self.txt = self.fix_text(self.ax.text(self.x_center, self.y_center, cross,
                                                          color='w',
                                                          weight='bold',
                                                          fontsize='small',
                                                          ha='center',
                                                          va='center'))

                if key[0] == 'AF Status Bottom Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Bottom Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center + 2 * self.spacer), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(cross), alpha=0.9))
                    self.txt = self.fix_text(
                        self.ax.text(self.x_center, self.y_center + 2 * self.spacer, cross, color='w',
                                     weight='bold',
                                     fontsize='small', ha='center', va='center'))

                if key[0] == 'AF Status Top Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Top Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center - 2 * self.spacer), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(cross), alpha=0.9))
                    self.txt = self.fix_text(
                        self.ax.text(self.x_center, self.y_center - 2 * self.spacer, cross, color='w',
                                     weight='bold',
                                     fontsize='small', ha='center', va='center'))

                if key[0] == 'AF Status Lower-middle':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center + self.spacer), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.txt = self.fix_text(
                        self.ax.text(self.x_center, self.y_center + self.spacer, vl[0], color='w',
                                     weight='bold',
                                     fontsize='small', ha='center', va='center'))

                if key[0] == 'AF Status Upper-middle':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center - self.spacer), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.txt = self.ax.text(self.x_center, self.y_center - self.spacer, vl[0], color='w',
                                            weight='bold',
                                            fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Near Left':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center - self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.txt = self.ax.text(self.x_center - self.spacer, self.y_center, vl[0], color='w',
                                            weight='bold',
                                            fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Near Right':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center + self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.txt = self.ax.text(self.x_center + self.spacer, self.y_center, vl[0], color='w',
                                            weight='bold',
                                            fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Left':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center - 3.5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.txt = self.ax.text(self.x_center - 3.5 * self.spacer, self.y_center, vl[0], color='w',
                                            weight='bold',
                                            fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Right':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center + 3.5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.txt = self.ax.text(self.x_center + 3.5 * self.spacer, self.y_center, vl[0], color='w',
                                            weight='bold',
                                            fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Far Left':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center - 5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.txt = self.ax.text(self.x_center - 5 * self.spacer, self.y_center, vl[0], color='w',
                                            weight='bold',
                                            fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Far Right':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center + 5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=1,
                                          edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.ax.text(self.x_center + 5 * self.spacer, self.y_center, vl[0], color='w',
                                 weight='bold',
                                 fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Lower-left':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center - 3.5 * self.spacer, self.y_center + 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=1, edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.ax.text(self.x_center - 3.5 * self.spacer,
                                 self.y_center + 1.6 * self.spacer, vl[0], color='w',
                                 weight='bold', fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Lower-right':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center + 3.5 * self.spacer, self.y_center + 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=1, edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.ax.text(self.x_center + 3.5 * self.spacer,
                                 self.y_center + 1.6 * self.spacer, vl[0], color='w',
                                 weight='bold', fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Upper-left':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center - 3.5 * self.spacer, self.y_center - 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=1, edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.ax.text(self.x_center - 3.5 * self.spacer,
                                 self.y_center - 1.6 * self.spacer, vl[0], color='w',
                                 weight='bold', fontsize='small', ha='center', va='center')

                if key[0] == 'AF Status Upper-right':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center + 3.5 * self.spacer, self.y_center - 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=1, edgecolor='limegreen', facecolor=norm(vl[0]), alpha=0.9))
                    self.ax.text(self.x_center + 3.5 * self.spacer,
                                 self.y_center - 1.6 * self.spacer, vl[0], color='w',
                                 weight='bold', fontsize='small', ha='center', va='center')

        if 'AF Point In Focus' in self.exif:
            afif = self.exif.get('AF Point In Focus')
            if afif == 'Center (vertical)':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c), self.rad, linewidth=2, edgecolor='y', facecolor='none',
                                   alpha=0.9))
            if afif == 'Center (horizontal)':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c), self.rad, linewidth=2, edgecolor='y', facecolor='none',
                                   alpha=0.9))
            if afif == 'Bottom (vertical)':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c + 2 * self.spacer), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none', alpha=0.9))
            if afif == 'Bottom (horizontal)':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c + 2 * self.spacer), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none', alpha=0.9))
            if afif == 'Top (vertical)':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c - 2 * self.spacer), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none', alpha=0.9))
            if afif == 'Top (horizontal)':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c - 2 * self.spacer), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none', alpha=0.9))
            if afif == 'Near Left':
                self.ax.add_patch(
                    patches.Circle((self.x_c - self.spacer, self.y_c), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none',
                                   alpha=0.9))
            if afif == 'Near Right':
                self.ax.add_patch(
                    patches.Circle((self.x_c + self.spacer, self.y_c), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none',
                                   alpha=0.9))
            if afif == 'Left':
                self.ax.add_patch(
                    patches.Circle((self.x_c - 3.5 * self.spacer, self.y_c), self.rad, linewidth=2,
                                   edgecolor='y',
                                   facecolor='none', alpha=0.9))
            if afif == 'Right':
                self.ax.add_patch(
                    patches.Circle((self.x_c + 3.5 * self.spacer, self.y_c), self.rad, linewidth=2,
                                   edgecolor='y',
                                   facecolor='none', alpha=0.9))
            if afif == 'Lower-middle':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c + self.spacer), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none',
                                   alpha=0.9))
            if afif == 'Upper-middle':
                self.ax.add_patch(
                    patches.Circle((self.x_c, self.y_c - self.spacer), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none',
                                   alpha=0.9))
            if afif == 'Lower-left':
                self.ax.add_patch(
                    patches.Circle((self.x_c - 3.5 * self.spacer, self.y_c + 1.6 * self.spacer), self.rad,
                                   linewidth=2,
                                   edgecolor='y', facecolor='none', alpha=0.9))
            if afif == 'Lower-right':
                self.ax.add_patch(
                    patches.Circle((self.x_c + 3.5 * self.spacer, self.y_c + 1.6 * self.spacer), self.rad,
                                   linewidth=2,
                                   edgecolor='y', facecolor='none', alpha=0.9))
            if afif == 'Upper-left':
                self.ax.add_patch(
                    patches.Circle((self.x_c - 3.5 * self.spacer, self.y_c - 1.6 * self.spacer), self.rad,
                                   linewidth=2,
                                   edgecolor='y', facecolor='none', alpha=0.9))
            if afif == 'Upper-right':
                self.ax.add_patch(
                    patches.Circle((self.x_c + 3.5 * self.spacer, self.y_c - 1.6 * self.spacer), self.rad,
                                   linewidth=2,
                                   edgecolor='y', facecolor='none', alpha=0.9))
            if afif == 'Far Left':
                self.ax.add_patch(
                    patches.Circle((self.x_c - 5 * self.spacer, self.y_c), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none', alpha=0.9))
            if afif == 'Far Right':
                self.ax.add_patch(
                    patches.Circle((self.x_c + 5 * self.spacer, self.y_c), self.rad, linewidth=2, edgecolor='y',
                                   facecolor='none', alpha=0.9))

        if 'AF Points Used' in self.exif:
            afp_used = (self.exif.get('AF Points Used')).split(', ')
            for i in range(0, len(afp_used)):

                if afp_used[i] == 'Center':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center), self.r_size, self.r_size, linewidth=2,
                                          edgecolor='r',
                                          facecolor='none', alpha=0.9))
                if afp_used[i] == 'Bottom':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center + 2 * self.spacer), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Top':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center - 2 * self.spacer), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Near Left':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center - self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Near Right':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center + self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Left':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center - 3.5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Right':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center + 3.5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Lower-middle':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center + self.spacer), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Upper-middle':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center, self.y_center - self.spacer), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Far Left':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center - 5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Far Right':
                    self.ax.add_patch(
                        patches.Rectangle((self.x_center + 5 * self.spacer, self.y_center), self.r_size,
                                          self.r_size, linewidth=2,
                                          edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Lower-left':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center - 3.5 * self.spacer, self.y_center + 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=2, edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Lower-right':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center + 3.5 * self.spacer, self.y_center + 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=2, edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Upper-left':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center - 3.5 * self.spacer, self.y_center - 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=2, edgecolor='r', facecolor='none', alpha=0.9))
                if afp_used[i] == 'Upper-right':
                    self.ax.add_patch(
                        patches.Rectangle(
                            (self.x_center + 3.5 * self.spacer, self.y_center - 1.6 * self.spacer), self.r_size,
                            self.r_size,
                            linewidth=2, edgecolor='r', facecolor='none', alpha=0.9))

        text = (f"{self.file_data}\n"
                f"15-point focus model detected ({self.exif.get('Camera Model Name')}). "
                f"Note: Number next to AF point represents in-focus estimation.\n"
                f"Less is better (i.e. 0 = in focus; 32768 = out of focus)"
                f"Focus Mode:{self.exif.get('Focus Mode')}\n")

        self.add_text(x=self.header_xy[0], y=self.header_xy[1], s=text, color='y',
                      weight='bold', fontsize='small', ha='left', va='top')

    def nineteen(self):
        cross_h, cross_v = None, None
        if self.exif.get('Camera Model Name') in ('SLT-A99', 'SLT-A99V'):
            self.r_size = 0.039 * self.xpixels / 1.5
            self.spacer = 0.047 * self.xpixels / 1.5
            self.rad = 0.03 * self.xpixels / 1.5

        for key in sorted(self.exif.items()):
            if key[0].startswith('AF Status'):

                vl = re.findall(r'\d+', key[1])
                if not vl:
                    vl.append('32768')
                if key[0] == 'AF Status Center Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Center Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))

                    x = self.x_center
                    y = self.y_center
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(s=cross)

                if key[0] == 'AF Status Bottom Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Bottom Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))

                    print(norm(cross), cross)
                    x, y = self.x_center, self.y_center + 2 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Top Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Top Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    x, y = self.x_center, self.y_center - 2 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Lower-middle':
                    x, y = self.x_center, self.y_center + self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Upper-middle':
                    x, y = self.x_center, self.y_center - self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Near Left':
                    x, y = self.x_center - self.spacer, self.y_center
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Near Right':
                    x, y = self.x_center + self.spacer, self.y_center
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Left Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Left Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))

                    x, y = self.x_center - 3.5 * self.spacer, self.y_center
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Right Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Right Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    x, y = self.x_center + 3.5 * self.spacer, self.y_center
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Lower-left Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Lower-left Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    x, y = self.x_center - 3.5 * self.spacer, self.y_center + 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Lower Far Left':
                    x, y = self.x_center - 4.5 * self.spacer, self.y_center + 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Upper-right Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Upper-right Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    x, y = self.x_center + 3.5 * self.spacer, self.y_center + 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Lower Far Right':
                    x, y = self.x_center + 4.5 * self.spacer, self.y_center + 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Upper-left Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Upper-left Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    x, y = self.x_center - 3.5 * self.spacer, self.y_center - 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Upper Far Left':
                    x, y = self.x_center - 4.5 * self.spacer, self.y_center - 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Upper-right Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Upper-right Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))
                    x, y = self.x_center + 3.5 * self.spacer, self.y_center - 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(cross))

                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Upper Far Right':
                    x, y = self.x_center + 4.5 * self.spacer, self.y_center - 1.6 * self.spacer
                    self.add_box(xy=(x, y), facecolor=norm(vl[0]))
                    self.add_box_text(x=x, y=y, s=vl[0])

                if key[0] == 'AF Status Far Left Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Far Left Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))

                    x, y = self.x_center - 5 * self.spacer, self.y_center

                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

                if key[0] == 'AF Status Far Right Horizontal':
                    cross_h = int(vl[0])
                if key[0] == 'AF Status Far Right Vertical':
                    cross_v = int(vl[0])
                    if cross_h < cross_v:
                        cross = cross_h
                    else:
                        cross = cross_v
                    cross = str(int(cross))

                    x, y = self.x_center + 5 * self.spacer, self.y_center

                    self.add_box(xy=(x, y), facecolor=norm(cross))
                    self.add_box_text(x=x, y=y, s=cross)

        # print("adding text")
        # text = (f"{self.file_data}\n"
        #            f"19-point focus model detected ({self.exif.get('Camera Model Name')}). "
        #            f"Note: Number next to AF point represents in-focus estimation.\n"
        #            f"Less is better (i.e. 0 = in focus; 32768 = out of focus)"
        #            f"Focus Mode:{self.exif.get('Focus Mode')}\n")

        # self.add_text(x=self.header_xy[0], y=self.header_xy[1], s=text, color='y',
        # weight='bold', fontsize='small', ha='left', va='top')

    def afpoints(self):
        vspacer, hspacer = None, None
        afp_used = (self.exif.get('AF Points Used')).split(', ')
        if self.exif.get('Camera Model Name') == 'ILCA-99M2':
            self.r_size = 0.020 * self.xpixels
            vspacer = 1.2 * self.r_size
            hspacer = 2.2 * self.r_size
        if self.exif.get('Camera Model Name') == 'ILCA-77M2':
            self.r_size = 0.020 * self.xpixels * 1.5
            vspacer = 1.2 * self.r_size
            hspacer = 2.2 * self.r_size

        # CENTER
        # E6
        e6 = dict(xy=(self.x_c - self.r_size / 2, self.y_c - self.r_size / 2),
                  facecolor='none', width=self.r_size, height=self.r_size)

        if 'E6' in afp_used:
            self.add_rectangle(e6, linewidth=2, edgecolor='limegreen', alpha=0.9)

        else:
            self.add_rectangle(e6, linewidth=2, edgecolor='w', alpha=0.3)

        # D6
        if 'D6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F6
        if 'F6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C6
        if 'C6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - 2 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - 2 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G6
        if 'G6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + 2 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + 2 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B6
        if 'B6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - 3 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - 3 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H6
        if 'H6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + 3 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + 3 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # A6
        if 'A6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - 4 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c - 4 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # I6
        if 'I6' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + 4 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2, self.y_c + 4 * vspacer - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E5
        if 'E5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D5
        if 'D5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F5
        if 'F5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C5
        if 'C5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G5
        if 'G5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B5
        if 'B5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H5
        if 'H5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # A5
        if 'A5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c - 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # I5
        if 'I5' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - hspacer, self.y_c + 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E7
        if 'E7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D7
        if 'D7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F7
        if 'F7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C7
        if 'C7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G7
        if 'G7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B7
        if 'B7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H7
        if 'H7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # A7
        if 'A7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c - 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # I7
        if 'I7' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + hspacer, self.y_c + 4 * vspacer - self.r_size / 2),
                    self.r_size,
                    self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # LEFT PART
        # E4
        if 'E4' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D4
        if 'D4' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F4
        if 'F4' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C4
        if 'C4' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G4
        if 'G4' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B4
        if 'B4' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H4
        if 'H4' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 2.8 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E3
        if 'E3' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D3
        if 'D3' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F3
        if 'F3' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C3
        if 'C3' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G3
        if 'G3' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B3
        if 'B3' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H3
        if 'H3' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 3.7 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E2
        if 'E2' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D2
        if 'D2' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F2
        if 'F2' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C2
        if 'C2' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G2
        if 'G2' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B2
        if 'B2' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H2
        if 'H2' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 4.6 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E1
        if 'E1' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D1
        if 'D1' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F1
        if 'F1' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C1
        if 'C1' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G1
        if 'G1' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 - 5.5 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # RIGHT PART
        # E8
        if 'E8' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D8
        if 'D8' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F8
        if 'F8' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C8
        if 'C8' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G8
        if 'G8' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B8
        if 'B8' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H8
        if 'H8' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 2.8 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E9
        if 'E9' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D9
        if 'D9' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F9
        if 'F9' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C9
        if 'C9' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G9
        if 'G9' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B9
        if 'B9' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H9
        if 'H9' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 3.7 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E10
        if 'E10' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D10
        if 'D10' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F10
        if 'F10' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C10
        if 'C10' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G10
        if 'G10' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # B10
        if 'B10' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c - 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # H10
        if 'H10' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 4.6 * hspacer, self.y_c + 3 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

        # E11
        if 'E11' in afp_used:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='limegreen', facecolor='none', alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle((self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c - self.r_size / 2),
                                  self.r_size, self.r_size,
                                  linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # D11
        if 'D11' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c - vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # F11
        if 'F11' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c + vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # C11
        if 'C11' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c - 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))
        # G11
        if 'G11' in afp_used:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='limegreen', facecolor='none',
                    alpha=0.9))
        else:
            self.ax.add_patch(
                patches.Rectangle(
                    (self.x_c - self.r_size / 2 + 5.5 * hspacer, self.y_c + 2 * vspacer - self.r_size / 2),
                    self.r_size, self.r_size, linewidth=2, edgecolor='w', facecolor='none', alpha=0.3))

    def facedetect(self):
        faces = self.exif.get('Faces Detected')
        faces = int(faces)

        if faces > 0:
            for i in range(1, 8):
                face_coord = self.exif.get(f'Face {i} Position')
                if face_coord:
                    try:

                        l = list(face_coord.split())
                        l = list(map(float, l))
                        self.add_rectangle(xy=(l[1], l[0]), width=l[2], height=l[3],
                                           linewidth=1, edgecolor='b', facecolor='none')

                        self.add_text(x=l[1], y=l[0], s=f'Face {i}', color='w', weight='bold',
                                      fontsize='small', ha='center', va='center')

                    except Exception as e:
                        print(e)

    def focal_plane_af(self):

        if self.exif.get('Focal Plane AF Points Used') != '(none)':
            if self.exif.get('Camera Model Name') in ('ILCE-6000', 'ILCE-5100'):
                self.foc = self.exif.get('Focal Plane AF Points Used')
                self.foc = [int(s) for s in re.findall(r'\d+', self.foc)]

                k = (-1)
                for j in range(1, 10):
                    for i in range(1, 12):
                        k = k + 1
                        if k in self.foc:
                            self.ax.add_patch(patches.Rectangle((i * (
                                    self.xpixels / 11) - self.xpixels / 11 / 2 - self.r_size / 4,
                                                                 self.ypixels / 9 * j - self.ypixels / 9 / 2 - self.r_size / 4),
                                                                self.r_size / 2, self.r_size / 2, linewidth=2,
                                                                edgecolor='lime',
                                                                facecolor='none', alpha=0.9))
                        else:
                            self.ax.add_patch(patches.Rectangle((i * (
                                    self.xpixels / 11) - self.xpixels / 11 / 2 - self.r_size / 4,
                                                                 self.ypixels / 9 * j - self.ypixels / 9 / 2 - self.r_size / 4),
                                                                self.r_size / 2, self.r_size / 2, linewidth=2,
                                                                edgecolor='w',
                                                                facecolor='none', alpha=0.3))
                    k = k + 10
                l = 10
                for j in range(1, 9):
                    for i in range(1, 11):
                        l = l + 1
                        if l in self.foc:
                            self.ax.add_patch(patches.Rectangle(
                                (i * (self.xpixels / 11) - self.r_size / 4, self.ypixels / 9 * j - self.r_size / 4),
                                self.r_size / 2, self.r_size / 2, linewidth=2, edgecolor='lime', facecolor='none',
                                alpha=0.9))
                        else:
                            self.ax.add_patch(patches.Rectangle(
                                (i * (self.xpixels / 11) - self.r_size / 4, self.ypixels / 9 * j - self.r_size / 4),
                                self.r_size / 2, self.r_size / 2, linewidth=2, edgecolor='w', facecolor='none',
                                alpha=0.3))
                    l = l + 11
            elif self.exif.get('Camera Model Name') in ('ILCE-7RM2'):
                self.foc = self.exif.get('Focal Plane AF Points Used')
                self.foc = [int(s) for s in re.findall(r'\d+', self.foc)]
                k = (-1)
                for j in range(1, 20):
                    for i in range(1, 22):
                        k = k + 1
                        if k in self.foc:
                            self.ax.add_patch(patches.Rectangle((i * (
                                    self.xpixels / (22 * 1.5)) + self.xpixels / 6 - self.r_size / 4,
                                                                 self.ypixels / (19 * 1.5) * j + self.ypixels / 7),
                                                                self.r_size / 4, self.r_size / 4, linewidth=2,
                                                                edgecolor='lime',
                                                                facecolor='none', alpha=0.9))
                        else:

                            x = i * (self.xpixels / (22 * 1.5)) + self.xpixels / 6 - self.r_size / 4
                            y = self.ypixels / (19 * 1.5) * j + self.ypixels / 7
                            width = self.r_size / 4
                            height = self.r_size / 4
                            self.add_rectangle(xy=(x, y), width=width, height=height, linewidth=2,
                                               edgecolor='w', facecolor='none', alpha=0.3)

            elif self.exif.get('Camera Model Name') in ('ILCE-7M2'):
                self.foc = self.exif.get('Focal Plane AF Points Used')
                self.foc = [int(s) for s in re.findall(r'\d+', self.foc)]
                k = (-1)
                for j in range(1, 10):
                    for i in range(1, 14):
                        k = k + 1
                        if k in self.foc:

                            x = i * (self.xpixels / (13 * 2.35)) + self.xpixels / 3.63 - self.r_size / 3
                            y = self.ypixels / (9 * 2.2) * j + self.ypixels / 4.24
                            width = self.r_size / 3
                            height = self.r_size / 3
                            self.add_rectangle(xy=(x, y), width=width, height=height, linewidth=2,
                                               edgecolor='lime', facecolor='none', alpha=0.9)

                        else:
                            x = i * (self.xpixels / (13 * 2.35)) + self.xpixels / 3.63 - self.r_size / 3
                            y = self.ypixels / (9 * 2.2) * j + self.ypixels / 4.24
                            width = self.r_size / 3
                            height = self.r_size / 3
                            self.add_rectangle(xy=(x, y), width=width, height=height,
                                               linewidth=2, edgecolor='w', facecolor='none', alpha=0.3)

            elif self.exif.get('Camera Model Name') in (
                    'ILCE-6300', 'ILCE-6500', 'ILCA-99M2', 'ILCA-77M2', 'ILCE-9', 'DSC-RX10M4', 'DSC-RX100M5',
                    'ILCE-7RM3',
                    'ILCE-7M3', 'DSC-RX100M6', 'ILCE-6400', 'ILCE-6600', 'ILCE-6100', 'DSC-RX0', 'DSC-RX0M2',
                    'MODEL-NAME',
                    'DSC-RX100M7', 'ILCE-7RM4'):
                self.foc = self.exif.get('Focal Plane AF Points Used')
                if int(self.foc):

                    r_size = list(self.exif.get('Focal Plane AF Point Area').split())

                    for i in range(1, int(self.foc) + 1):
                        width = self.xpixels * 0.039 / 2
                        height = self.xpixels * 0.039 / 2
                        afloc = list(self.exif.get('Focal Plane AF Point Location ' + str(i)).split())
                        # print(self.exif.get('Focal Plane AF Point Area'))

                        ## adding () to show whats done
                        x = ((self.xpixels * int(afloc[0])) / int(r_size[0])) - (width / 2)
                        y = ((self.ypixels * int(afloc[1])) / int(r_size[1])) - (height / 2)
                        print(f"x: {x} , y: {y}, width: {width}, height: {height}, "
                              f"xpixels: {self.xpixels}, ypixels:{self.ypixels}, r_size:{r_size}, afloc:{int(afloc[0])}")
                        # print(f'x=(({self.xpixels} * {int(afloc[0])}) / {int(self.r_size[0])}) - ({width} / 2={x})')
                        # print(f'y={self.ypixels} * {int(afloc[1])} / {int(self.r_size[1])} - {height} / 2 = {y}')
                        self.add_box(xy=(x, y), width=width, height=height, facecolor='none', alpha=0.8)
            else:
                self.foc = []
        else:
            self.foc = []

    def focus_location(self):
        focusp = self.exif.get('Focus Location')
        focusp = list(focusp.split())
        focusp = list(map(float, focusp))
        if self.exif.get('AF Area Mode') == 'Tracking' and self.exif.get(
                'AF Tracking') == 'Lock On AF' and self.exif.get(
            'Camera Model Name') in (
                'ILCE-6400', 'ILCE-6100', 'ILCE-6600', 'ILCE-9', 'ILCE-7RM4', 'ILCE-RX100M7'):

            self.add_rectangle(xy=(focusp[2] - 0.02 * self.xpixels, focusp[3] - 0.02 * self.xpixels),
                               width=0.04 * self.xpixels, height=0.04 * self.xpixels, linewidth=1,
                               edgecolor='lime', facecolor='none')

            self.add_rectangle(xy=(focusp[2] - 0.025 * self.xpixels, focusp[3] - 0.025 * self.xpixels),
                               width=0.05 * self.xpixels, height=0.05 * self.xpixels, linewidth=1,
                               edgecolor='lime', facecolor='none', linestyle='--')

        elif self.exif.get('AF Tracking') == 'Face tracking':
            self.add_circle(xy=(focusp[2], focusp[3]), radius=(0.01 * self.xpixels),
                            linewidth=1, edgecolor='lime', facecolor='none')
        else:
            self.add_circle(xy=(focusp[2], focusp[3]), radius=(0.01 * self.xpixels),
                            linewidth=2, edgecolor='y', facecolor='none')


class brakeout(messylogics, af):



    def add_box_text(self, **kwargs):
        return self.ax.text(x=kwargs.get("x", self.x_center), y=kwargs.get("y", self.y_center),
                            s=kwargs.get("s", "None"),
                            color=kwargs.get("color", "w"),
                            weight=kwargs.get("weight", "bold"),
                            fontsize=kwargs.get("fontsize", "small"),
                            ha=kwargs.get("ha", "center"),
                            va=kwargs.get("va", "center"))

    def add_box(self, **kwargs):
        self.ax.add_patch(patches.Rectangle(xy=kwargs.get("xy", (self.x_center, self.y_center)),
                                            width=kwargs.get("width", self.r_size),
                                            height=kwargs.get("height", self.r_size),
                                            linewidth=kwargs.get("linewidth", 1),
                                            edgecolor=kwargs.get("edgecolor", 'limegreen'),
                                            facecolor=kwargs.get("facecolor", None),
                                            alpha=kwargs.get("alpha", 0.5)
                                            )
                          )

    def add_rectangle(self, *args, **kwargs):
        # class matplotlib.patches.Rectangle(xy, width, height, angle=0.0, **kwargs)
        afspot = patches.Rectangle(*args, **kwargs)
        self.ax.add_patch(afspot)

    def add_circle(self, *args, **kwargs):
        # class matplotlib.patches.Circle(xy, radius=5, **kwargs)
        focuspoint = patches.Circle(*args, **kwargs)
        self.ax.add_patch(focuspoint)

    def add_text(self, **kwargs):
        self.ax.text(**kwargs)

    def base_data(self, im):
        self.exifdata = self.exifdata.stdout.splitlines()
        print(self.exifdata)
        for s in self.exifdata:

            data = s.split(':', 1)
            key = data[0].strip()
            val = data[1].strip()
            self.exif[key] = val

        print(self.exif)

        #### IF RAW opened, crop image to proper aspect ratio and resolution according to self.exif
        # (i.e. quick fix of Distortion correction data)
        if self.exif.get('Full Image Size'):
            fimsize = self.exif.get('Full Image Size').split("x")  # todo better
            if int(fimsize[1]) < self.ypixels or int(fimsize[0]) < self.xpixels:
                # debug print ("Crop needed! self.exif Height = ",int(exif.get('Sony Image Height'))
                # ,", self.ypixels = ",self.ypixels)

                self.xdiff = int(fimsize[0])
                self.ydiff = int(fimsize[1])
                self.startx = self.xpixels // 2 - (self.xdiff // 2)
                self.starty = self.ypixels // 2 - (self.ydiff // 2)
                im = im[self.starty:self.starty + self.ydiff, self.startx:self.startx + self.xdiff]
                self.ypixels, self.xpixels, _ = im.shape

            self.r_size = 0.039 * self.xpixels

            self.x_center = self.xpixels / 2 - self.r_size / 2
            self.y_center = self.ypixels / 2 - self.r_size / 2

            self.x_c = self.xpixels / 2
            self.y_c = self.ypixels / 2
            self.spacer = 0.047 * self.xpixels

            self.rad = 0.03 * self.xpixels
        self.header_xy = (0.01 * self.ypixels, 0.01 * self.xpixels)



class draw(brakeout):
    def __init__(self, ax, fig):
        self.ax = ax
        self.fig = fig
        self.x_c = None
        self.y_c = None
        self.r_size = None
        self.xpixels = None
        self.ypixels = None
        self.z_status = None
        self.flist = None
        self.filename = None
        self.pos = None
        self.oldf = None
        self.exif = dict()
        self.spacer = None
        self.rad = None
        self.exifdata = None

    def handle_close(self, event):
        self.fig.close()

    def ofile(self, event):

        self.flist = []
        if self.filename:
            self.oldf = self.filename

        self.filename = "/Users/faar/Documents/Src/priv/s_afv/src/{}".format(
            filename)  # tkFileDialog.askopenfilename(filetypes=[('JPG or RAW from Sony Camera', ('*.jpg','*.arw'))])
        if not self.filename:
            if not self.oldf:
                return
            self.filename = self.oldf
            for file in os.listdir(os.path.dirname(self.filename)):
                if file.endswith((".jpg", ".JPG", '.arw', '.ARW')):
                    self.flist.append(os.path.dirname(self.filename) + '/' + file)
            self.flist.sort()
            self.pos = self.flist.index(self.filename)

            return
        for file in os.listdir(os.path.dirname(self.filename)):
            if file.endswith((".jpg", ".JPG", '.arw', '.ARW')):
                self.flist.append(os.path.dirname(self.filename) + '/' + file)
        self.flist.sort()
        # flist.sort(key=len)
        self.pos = self.flist.index(self.filename)

        self.start()

    def save(self, event):
        sname = tkFileDialog.asksaveasfilename(filetypes=[('JPEG', '*.jpg')], defaultextension='.jpg')
        if not sname:
            return
        extent = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        wi = (extent.width * self.fig.dpi)
        self.fig.savefig(sname, dpi=(self.fig.dpi * (self.xpixels / wi)), bbox_inches=extent, pad_inches=0,
                         transparent=True,
                         frameon=False, format='jpg')
        subprocess.call(['exiftool', '-tagsFromFile', self.filename, sname, '-overwrite_original_in_place'], shell=True)

    def prevf(self, event):
        if self.pos:
            if self.pos == 0:
                self.pos = len(self.flist)
            self.pos = self.pos - 1
            self.filename = self.flist[self.pos]
            self.start()
        else:
            return

    def nextf(self, event):

        if self.pos:
            if self.pos == len(self.flist) - 1:
                self.pos = -1
            self.pos += 1
            self.filename = self.flist[self.pos]
            self.start()
        else:
            return

    def zoom(self, event):
        if self.z_status == 0:
            self.x_c = self.xpixels / 2
            self.y_c = self.ypixels / 2
            bbox = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
            width, height = bbox.width, bbox.height

            width *= self.fig.dpi
            height *= self.fig.dpi
            plt.axis([self.x_c - width / 2, self.x_c + width / 2, self.y_c + height / 2, self.y_c - height / 2])
            self.fig.canvas.draw()
            self.z_status = 1
        else:
            plt.axis([0, self.xpixels, self.ypixels, 0])
            self.fig.canvas.draw()
            self.z_status = 0

    def fix_text(self, text):
        text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()])
        print(text)
        return text







# Create figure and axes
fig = plt.figure()
ax = plt.subplot()
fig.canvas.set_window_title('AF Visualizer')
fig.subplots_adjust(left=0.02, bottom=0.08, right=0.98, top=0.98)
ax.axis('off')
ax.text(0.5, 0.5, 'Open file with OPEN... button', color='gray', weight='bold', fontsize='x-large', ha='center',
        va='center')
callback = draw(ax, fig)

obutton = plt.axes([0.01, 0.01, 0.1, 0.05])
pbutton = plt.axes([0.12, 0.01, 0.1, 0.05])
nbutton = plt.axes([0.23, 0.01, 0.1, 0.05])
sbutton = plt.axes([0.34, 0.01, 0.1, 0.05])
zbutton = plt.axes([0.45, 0.01, 0.1, 0.05])

fopen = Button(obutton, 'Open...')
fopen.on_clicked(callback.ofile)

prevp = Button(pbutton, 'Previous')
prevp.on_clicked(callback.prevf)

nextp = Button(nbutton, 'Next')
nextp.on_clicked(callback.nextf)

save = Button(sbutton, 'Save')
save.on_clicked(callback.save)

zoom = Button(zbutton, '1:1/Fit')
zoom.on_clicked(callback.zoom)

fig.canvas.mpl_connect('close_event', callback.handle_close)

plt.show()

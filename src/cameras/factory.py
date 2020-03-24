from abc import ABC, abstractmethod


class Camera(ABC):

    @abstractmethod
    def exposure(self):
        pass

    @abstractmethod
    def make(self):
        pass

    @abstractmethod
    def model(self):
        pass

    @abstractmethod
    def software(self):
        pass

    @abstractmethod
    def lens(self):
        pass

    @abstractmethod
    def megapixels(self):
        pass

class Exposure:
    def __init__(self, **kwargs):
        self._shutterspeed = kwargs.get('shutterspeed', None)
        self._iso = int(kwargs.get('iso', None))
        self._aperture = float(kwargs.get('aperture', None))
        self._focal_length = int(kwargs.get('focal_length', None))

    @property
    def shutterspeed(self):
        return self._shutterspeed

    @property
    def iso(self):
        return self._iso

    @property
    def aperture(self):
        return self._aperture

    @property
    def focal_length(self):
        """
        Does not have with exposure to do, but is needed for ssr check
        """
        return self._focal_length

    @property
    def ssr(self):
        """ shutter speed rule, helps to determine if image that is out of
        focus may have been causes by camera shake due to slow shutter

        Not really exposure, but does not fit anywhere else right now
        """

        s = self._shutterspeed.split("/")
        speed = int(s[1])

        if self.focal_length > speed:
            return "poor"
        elif speed < (self.focal_length * 2):
            return "good"
        elif speed > (2 * self.focal_length):
            return "great"
        else:
            return "unknown"
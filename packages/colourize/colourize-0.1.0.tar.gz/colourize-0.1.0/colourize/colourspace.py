"""Colourspace with metadata required to perform conversion.

Name for the ``colour-science`` conversion graph and channels.
"""
import warnings


class Colourspace():
    _two_ch = ['CIE UCS uv', 'CIE Luv uv']

    _three_ch = ['sRGB', 'CAM02SCD', 'CAM02LCD', 'CAM02UCS', 'CIECAM02 JMh',
                 'Scene-Referred RGB', 'IPT', 'hdr IPT', 'CMY', 'CIE LAB',
                 'hdr CIELab', 'CIE XYZ', 'Hunter Rdab', 'YCbCr', 'YcCbcCrc',
                 'ICtCp', 'CIE UCS', 'CIE LCHab', 'JzAzBz', 'HED', 'HSV',
                 'CIE xyY', 'OSA UCS', 'HSL', 'CIE UVW', 'Hunter LAB',
                 'CIE Luv', 'Munsell Colour']

    _four_ch = ['CMYK', 'Prismatic']

    _warn_non_fatal = ['HSV', 'CIE xyY', 'OSA UCS', 'HSL', 'CMYK', 'Prismatic']

    _fatal_nan = ['CIE UCS uv', 'CIE Luv uv', 'CIE UVW', 'Hunter LAB',
                  'CIE Luv']

    _fatal_scaling = ['Munsell Colour']

    def __init__(self, name, channels=None):
        self.colour = name
        self.std_name = name.replace(' ', '-').lower()
        if not channels:
            self.channels = self._ch_from_name()
        else:
            self.channels = channels

        if self.colour in self._warn_non_fatal:
            warnings.warn("Colourspace {} raises conversion errors \
                          from sRGB".format(self.colour))
        if self.colour in self._fatal_nan:
            warnings.warn("Colourspace {} conversion from sRGB \
                          produces NANs".format(self.colour))
        if self.colour in self._fatal_scaling:
            warnings.warn("Colourspace {} conversion from sRGB \
                          fails scaling".format(self.colour))

    def __str__(self):
        return self.colour

    def __eq__(self, other):
        return self.std_name == other.std_name

    def _ch_from_name(self):
        if self.colour in self._two_ch:
            return 2
        elif self.colour in self._three_ch:
            return 3
        elif self.colour in self._four_ch:
            return 4
        else:
            raise ValueError("Colourspace {} is not implemented.", self.colour)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    COLOURSPACES = [Colourspace('sRGB'),
                    Colourspace('CAM02SCD'),
                    Colourspace('CAM02LCD'),
                    Colourspace('CAM02UCS'),
                    Colourspace('CIECAM02 JMh'),
                    Colourspace('Scene-Referred RGB'),
                    Colourspace('IPT'),
                    Colourspace('hdr IPT'),
                    Colourspace('CMY'),
                    Colourspace('CIE LAB'),
                    Colourspace('hdr CIELab'),
                    Colourspace('CIE XYZ'),
                    Colourspace('Hunter Rdab'),
                    Colourspace('YCbCr'),
                    Colourspace('YcCbcCrc'),
                    Colourspace('ICtCp'),
                    Colourspace('CIE UCS'),
                    Colourspace('CIE LCHab'),
                    Colourspace('JzAzBz'),
                    Colourspace('HED'),              # Scikit-Image
                    Colourspace('HSV'),              # Non-Fatal Errors
                    Colourspace('CIE xyY'),          # Non-Fatal Errors
                    Colourspace('OSA UCS'),          # Non-Fatal Errors
                    Colourspace('HSL'),              # Non-Fatal Errors
                    Colourspace('CMYK'),             # Non-Fatal Errors
                    Colourspace('Prismatic')]        # Non-Fatal Errors

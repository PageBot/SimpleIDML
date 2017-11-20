#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
import os
import sys
from simple_idml.indesign import indesign
from simple_idml.commands import InDesignSoapCommand


class InDesignSaveAsCommand(InDesignSoapCommand):
    description = """SOAP call to a InDesignServer to save a file in (an)other format(s).

        Export PDF parameters
        '''''''''''''''''''''

        o Boolean parameters just need to be present to be set on:

            - colorBars, optimizePDF, cropMarks, pageInformationMarks,
                registrationMarks,


        o String parameters:

            You can call a predifined preset (.joboptions file) with
            pdfExportPresetName:

            - pdfExportPresetName: [Press Quality], ...

            Or the the following parameters:

            - acrobatCompatibility: 4, 5, 6, 7 or 8
            - colorSpace: CMYK, iGry, rCMY, rRGB, cRGB or unFc
            - colorProfile (output > color > destination) and
                (output > PDF/X > profile): Generic CMYK Profile, ...
            - flattenerPresetName: [High resolution print], ...
            - standartsCompliance: 1A2001, 1A2003, 32002, 32003 or 42010
            - bleedTop, bleedBottom, bleedInside, bleedOutside: (float value)
            - pageMarksOffset: [0 to 72]
            - colorBitmapSampling: subSample, downSample or bicubicDownSample
            - colorBitmapQuality: minimum, low, medium, high, maximum, 4bits or 8bits
            - colorBitmapCompression: auto, jpeg, zip, jpeg2000 or autoJpeg2000
            - colorBitmapSamplingDPI: [9 to 2400]
            - grayscaleBitmapSampling: subSample, downSample or bicubicDownSample
            - grayscaleBitmapQuality: minimum, low, medium, high, maximum, 4bits or 8bits
            - grayscaleBitmapCompression: auto, jpeg, zip, jpeg2000 or autoJpeg2000
            - grayscaleBitmapSamplingDPI: [9 to 2400]
            - monochromeBitmapSampling: subSample, downSample or bicubicDownSample
            - monochromeBitmapCompression: CCIT3, CCIT4, zip, RLE
            - monochromeBitmapSamplingDPI: [9 to 2400] """

    def __init__(self):
        super(InDesignSaveAsCommand, self).__init__()
        self.parser.add_argument('source', metavar='SOURCE', type=file)
        self.parser.add_argument('destinations', metavar='DESTINATIONS', help="file1|opt1=a,opt2=b;file2|opt1=c")

    def parse_options(self):
        encoding = locale.getpreferredencoding()
        for i, a in enumerate(sys.argv):
            sys.argv[i] = unicode(a.decode(encoding))
        self.args = self.parser.parse_args()

    def execute(self):
        super(InDesignSaveAsCommand, self).execute()
        destinations = self.args.destinations.split(";")
        formats = map(self.parse_destination_arg, destinations)
        responses = indesign.save_as(self.args.source, formats, self.args.url, self.args.client_workdir,
                                     self.args.server_workdir, self.args.server_path_style,
                                     not self.args.no_clean_workdir, self.ftp_params)
        map(self.save_as, responses, destinations)

    def parse_destination_arg(self, arg):
        try:
            dest, params = arg.split("|")
        except ValueError:
            dest = arg
            params = {}
        else:
            params = dict([keyval.split("=") for keyval in params.split(",")])

        return {
            "fmt": os.path.splitext(dest)[1].replace(".", ""),
            "params": params,
        }

    def save_as(self, response, dst):
        with open(dst.split("|")[0], mode="w+") as fobj:
            fobj.write(response)


def main():
    command = InDesignSaveAsCommand()
    command.execute()


if __name__ == "__main__":
    main()

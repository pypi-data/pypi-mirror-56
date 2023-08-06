#!/usr/bin/env python3
# -*- coding: utf-8 -*-
PROG_VERSION = u"Time-stamp: <2019-11-23 16:11:23 vk>"


# TODO:
# * add -i (interactive) where user gets asked if renaming should be done (per file)
# * fix parts marked with «FIXXME»


# ===================================================================== ##
#  You might not want to modify anything below this line if you do not  ##
#  know, what you are doing :-)                                         ##
# ===================================================================== ##

import re
import sys
import os
import os.path
import time
import logging
from optparse import OptionParser
import colorama
import datetime  # for calculating duration of chunks
import json  # to parse JSON meta-data files

try:
    from fuzzywuzzy import fuzz  # for fuzzy comparison of strings
except ImportError:
    print("Could not find Python module \"fuzzywuzzy\".\nPlease install it, e.g., with \"sudo pip install fuzzywuzzy\".")
    sys.exit(1)

try:
    import PyPDF2
except ImportError:
    print("Could not find Python module \"PyPDF2\".\nPlease install it, e.g., with \"sudo pip install PyPDF2\".")
    sys.exit(1)

PROG_VERSION_DATE = PROG_VERSION[13:23]
INVOCATION_TIME = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

USAGE = "\n\
    guessfilename [<options>] <list of files>\n\
\n\
This little Python script tries to rename files according to pre-defined rules.\n\
\n\
It does this with several methods: first, the current file name is analyzed and\n\
any ISO date/timestamp and filetags are re-used. Secondly, if the parsing of the\n\
file name did not lead to any new file name, the content of the file is analyzed.\n\
\n\
You have to adapt the rules in the Python script to meet your requirements.\n\
The default rule-set follows the filename convention described on\n\
http://karl-voit.at/managing-digital-photographs/\n\
\n\
\n\
:copyright: (c) by Karl Voit\n\
:license: GPL v3 or any later version\n\
:URL: https://github.com/novoid/guess-filename.py\n\
:bugreports: via github or <tools@Karl-Voit.at>\n\
:version: " + PROG_VERSION_DATE + "\n"

ERROR_DIR = 'guess-filename_fails'
SUCCESS_DIR = 'guess-filename_success'

parser = OptionParser(usage=USAGE)

parser.add_option("-d", "--dryrun", dest="dryrun", action="store_true",
                  help="enable dryrun mode: just simulate what would happen, do not modify files")

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="enable verbose mode")

parser.add_option("-q", "--quiet", dest="quiet", action="store_true",
                  help="enable quiet mode")

parser.add_option("--version", dest="version", action="store_true",
                  help="display version and exit")

(options, args) = parser.parse_args()


def handle_logging():
    """Log handling and configuration"""

    if options.verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    elif options.quiet:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.ERROR, format=FORMAT)
    else:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def error_exit(errorcode, text):
    """exits with return value of errorcode and prints to stderr"""

    sys.stdout.flush()
    logging.error(text)

    sys.exit(errorcode)


class FileSizePlausibilityException(Exception):
    """
    Exception for file sizes being to small according to their duration and quality indicator
    """

    def __init__(self, message):
        self.value = message

    def __str__(self):
        return repr(self.value)


class GuessFilename(object):
    """
    Contains methods of the guess filename domain
    """

    FILENAME_TAG_SEPARATOR = ' -- '
    BETWEEN_TAG_SEPARATOR = ' '

    # file names containing tags matches following regular expression
    # ( (date(time)?)?(--date(time)?)? )? filename (tags)? (extension)?
    DAY_REGEX = '[12]\d{3}-?[01]\d-?[0123]\d'  # note: I made the dashes between optional to match simpler format as well
    TIME_REGEX = 'T[012]\d.[012345]\d(.[012345]\d)?'
    TIME_FUZZY_REGEX = '([012]\d)[-._:]?([012345]\d)([-._:]?([012345]\d))?'  # a bit less restrictive than TIME_REGEX

    DAYTIME_REGEX = '(' + DAY_REGEX + '(' + TIME_REGEX + ')?)'
    DAYTIME_DURATION_REGEX = DAYTIME_REGEX + '(--?' + DAYTIME_REGEX + ')?'

    ISO_NAME_TAGS_EXTENSION_REGEX = re.compile('((' + DAYTIME_DURATION_REGEX + ')[ -_])?(.+?)(' + FILENAME_TAG_SEPARATOR + '((\w+[' + BETWEEN_TAG_SEPARATOR + ']?)+))?(\.(\w+))?$', re.UNICODE)
    DAYTIME_DURATION_INDEX = 2
    NAME_INDEX = 10
    TAGS_INDEX = 12
    EXTENSION_INDEX = 15

    RAW_EURO_CHARGE_REGEX = '(\d+([,.]\d+)?)[-_ ]?(EUR|€)'
    EURO_CHARGE_REGEX = re.compile('^(.+[-_ ])?' + RAW_EURO_CHARGE_REGEX + '([-_ .].+)?$', re.UNICODE)
    EURO_CHARGE_INDEX = 2

    ANDROID_SCREENSHOT_REGEX = re.compile('Screenshot_([12]\d{3})-?([01]\d)-?([0123]\d)' + '-?' +
                                          '([012]\d)([012345]\d)(([012345]\d))?' + '(.*)?.(png|jpg)', re.UNICODE)
    ANDROID_SCREENSHOT_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', 4, '.', 5, '.', 7, 8, ' -- screenshots android.', 9]

    # Firefox_Screenshot_2018-05-03T20-07-14.972Z.png
    EASY_SCREENSHOT_REGEX = re.compile('Firefox_Screenshot_(' + DAY_REGEX + ')T' + TIME_FUZZY_REGEX + '\.\d{3}Z(.*).png')
    EASY_SCREENSHOT_INDEXGROUPS = [1, 'T', 2, '.', 3, '.', 5, ' Firefox - -- screenshots.png']

    TIMESTAMP_DELIMITERS = '[.;:-]?'
    DATESTAMP_REGEX = '([12]\d{3})' + TIMESTAMP_DELIMITERS + '([01]\d)' + TIMESTAMP_DELIMITERS + '([0123]\d)'
    TIMESTAMP_REGEX = '([012]\d)' + TIMESTAMP_DELIMITERS + '([012345]\d)(' + TIMESTAMP_DELIMITERS + '([012345]\d))?'

    OSMTRACKS_REGEX = re.compile(DATESTAMP_REGEX + 'T?' + TIMESTAMP_REGEX + '(_.*)?.gpx', re.UNICODE)
    OSMTRACKS_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', 4, '.', 5, ['.', 7], 8, '.gpx']

    SIGNAL_REGEX = re.compile('signal-(attachment-)?' + DATESTAMP_REGEX + '-' + TIMESTAMP_REGEX + '(.+)?(\..+)', re.UNICODE)

    IMG_REGEX = re.compile('IMG_' + DATESTAMP_REGEX + '_' + TIMESTAMP_REGEX + '(_Bokeh)?(.+)?.jpg', re.UNICODE)
    IMG_INDEXGROUPS_NORMAL = [1, '-', 2, '-', 3, 'T', 4, '.', 5, ['.', 7], 9, '.jpg']
    IMG_INDEXGROUPS_BOKEH = [1, '-', 2, '-', 3, 'T', 4, '.', 5, ['.', 7], ' Bokeh', 9, '.jpg']
    VID_REGEX = re.compile('VID_' + DATESTAMP_REGEX + '_' + TIMESTAMP_REGEX + '(.+)?.mp4', re.UNICODE)
    VID_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', 4, '.', 5, ['.', 7], 8, '.mp4']

    # OLD # # MediathekView: Settings > modify Set > Targetfilename: "%DT%d h%i %s %t - %T - %N.mp4" (limited to 120 characters)
    # OLD # # results in files like:
    # OLD # #   20161227T201500 h115421 ORF Das Sacher. In bester Gesellschaft 1.mp4
    # OLD # #   20161227T193000 l119684 ORF ZIB 1 - Auswirkungen der _Panama-Papers_ - 2016-12-27_1930_tl_02_ZIB-1_Auswirkungen-de__.mp4
    # OLD # MEDIATHEKVIEW_SIMPLE_REGEX = re.compile(DATESTAMP_REGEX + 'T?' + TIMESTAMP_REGEX +
    # OLD #                                         '(.+?)( - [12]\d{3}' + TIMESTAMP_DELIMITERS + '[01]\d' + TIMESTAMP_DELIMITERS +
    # OLD #                                         '[0123]\d_.+)?.mp4', re.UNICODE)
    # OLD # MEDIATHEKVIEW_SIMPLE_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', 4, '.', 5, ['.', 7], 8, '.mp4']

    # MediathekView: Settings > modify Set > Targetfilename: "%DT%d %s - %t - %T -ORIGINAL- %N.mp4" (without any limitation of the maximum numbers of characters)
    # results in files like:
    #   20180510T090000 ORF - ZIB - Signation -ORIGINAL- 2018-05-10_0900_tl_02_ZIB-9-00_Signation__13976423__o__1368225677__s14297692_2__WEB03HD_09000305P_09001400P_Q4A.mp4
    #   20180510T090000 ORF - ZIB - Weitere Signale der Entspannung -ORIGINAL- 2018-05-10_0900_tl_02_ZIB-9-00_Weitere-Signale__13976423__o__5968792755__s14297694_4__WEB03HD_09011813P_09020710P_Q4A.mp4
    #   20180521T193000 ORF - ZIB 1 - Parlament bereitet sich auf EU-Vorsitz vor -ORIGINAL- 2018-05-21_1930_tl_02_ZIB-1_Parlament-berei__13977453__o__277886215b__s14303762_2__WEB03HD_19350304P_19371319P_Q4A.mp4
    #   20180522T220000 ORF - Willkommen Österreich mit Stermann & Grissemann - Beachvolleyball-Duo Clemens Doppler und Alexander Horst -ORIGINAL- 2018-05-22_2200_l__13977514__o__1745__s14352_2__BCK1HD_22394018P_22.mp4
    #    -ORIGINAL- 2018-05-22_2200_l__13977514__o__1745__s14352_2__BCK1HD_22394018P_22.mp4

    # SHORT_REGEX: if MediathekView is NOT able to generate the full length file name because
    #              of file name length restrictions, this RegEx is a fall-back in order to
    #              recognize the situation.
    MEDIATHEKVIEW_SHORT_REGEX_STRING = DATESTAMP_REGEX + 'T?' + TIMESTAMP_REGEX + \
                                       ' (.+) - (.+) - (.+) -ORIGINAL(hd|low)?- '  # e.g., "20180510T090000 ORF - ZIB - Signation -ORIGINAL- "
    MEDIATHEKVIEW_SHORT_REGEX = re.compile(MEDIATHEKVIEW_SHORT_REGEX_STRING + '(.+).mp4')

    # MediathekView was able to generate the full length file name including
    # the full length original file name which DOES NOT contain the detailed begin- and
    # end-timestamps at the end of the file name which still ends
    # with the quality indicator Q4A or Q8C when used with the ORF sender file format.
    #
    # example: 20180608T193000 ORF - Österreich Heute HD 10min - Das Magazin - Österreich Heute - Das Magazin -ORIGINAL- 13979231_0007_Q8C.mp4
    MEDIATHEKVIEW_LONG_WITHOUT_DETAILED_TIMESTAMPS_REGEX = re.compile(MEDIATHEKVIEW_SHORT_REGEX_STRING + '.+_(Q4A|Q6A|Q8C).mp4')

    # Original ORF TV Mediathek download file names as a fall-back for
    # raw download using wget or curl: context menu > "Film-URL
    # kopieren"
    #
    # examples:
    #   2018-06-14_2105_sd_02_Am-Schauplatz_-_Alles für die Katz-_____13979879__o__1907287074__s14316407_7__WEB03HD_21050604P_21533212P_Q8C.mp4
    #   2018-06-14_2155_sd_06_Kottan-ermittelt - Wien Mitte_____13979903__o__1460660672__s14316392_2__ORF3HD_21570716P_23260915P_Q8C.mp4
    #   2018-06-14_2330_sd_06_Sommerkabarett - Lukas Resetarits: Schmäh (1 von 2)_____13979992__o__1310584704__s14316464_4__ORF3HD_23301620P_00302415P_Q8C.mp4
    MEDIATHEKVIEW_RAW_DATETIME = DATESTAMP_REGEX + '_' + TIMESTAMP_REGEX  # e.g., "2018-06-14_2105"
    MEDIATHEKVIEW_RAW_TITLE = '_[a-z]{2}_\d{2}_(.+)'  # e.g., "_sd_02_Am-Schauplatz_-_Alles für die Katz"
    MEDIATHEKVIEW_RAW_NUMBERS = '_+\d+__o__.+_'  # e.g., "_____13979879__o__1907287074__s14316407_7__WEB03HD_"
    MEDIATHEKVIEW_RAW_ENDING = TIMESTAMP_REGEX + '\d\dP_' + TIMESTAMP_REGEX + '\d\dP_(Q4A|Q6A|Q8C).mp4'  # e.g., "21050604P_21533212P_Q8C.mp4"
    MEDIATHEKVIEW_RAW_REGEX_STRING = MEDIATHEKVIEW_RAW_DATETIME + MEDIATHEKVIEW_RAW_TITLE + \
                                     MEDIATHEKVIEW_RAW_NUMBERS + MEDIATHEKVIEW_RAW_ENDING

    # URL has format like: http://apasfpd.sf.apa.at/cms-worldwide/online/7db1010b02753288e65ff61d5e1dff58/1528531468/2018-06-08_2140_tl_01_Was-gibt-es-Neu_Promifrage-gest__13979244__o__1391278651__s14313058_8__BCK1HD_22050122P_22091314P_Q4A.mp4
    # but with varying quality indicator: Q4A (low), Q6A (high), Q8C (HD)
    # which gets parsed like:
    #   http://apasfpd.sf.apa.at/cms-worldwide/online/      → required
    #   7db1010b02753288e65ff61d5e1dff58/1528531468
    #   /2018-06-08_2140_tl_                             → required
    #   01_Was-gibt-es-Neu_Promifrage-gest__13979244__o__1391278651__s14313058_8__BCK1HD
    #   _22050122P_22091314P_Q4A.mp4                     → required
    # 2019-09-21: Regex seems to have changed to something matching:
    #   https://apasfiis.sf.apa.at/ipad/cms-worldwide/2019-09-20_2200_tl_02_ZIB-2_Wetter__14026467__o__698276635d__s14562567_7__ORF2HD_22241720P_22245804P_Q4A.mp4/playlist.m3u8
    #   which gets parsed like:
    #   https://apasfiis.sf.apa.at/ipad/cms-worldwide/
    #   2019-09-20_2200_tl_          2019-09-30: instead "_tl_" there could be "_sd_"
    #   02_ZIB-2_Wetter__14026467__o__698276635d__s14562567_7__ORF2HD
    #   _22241720P_22245804P_
    #   Q4A.mp4/playlist.m3u8
    FILM_URL_REGEX = re.compile('https?://apasfiis.sf.apa.at/(ipad/)?cms-.+/' +
                                DATESTAMP_REGEX + '_' + TIMESTAMP_REGEX + '_(tl|sd)_' +  # e.g., 2019-09-20_2200_tl_
                                '.+' +  # e.g., 02_ZIB-2_Wetter__14026467__o__698276635d__s14562567_7__ORF2HD
                                '_' + TIMESTAMP_REGEX + '\d\dP_' + TIMESTAMP_REGEX + '\d\dP_' +  # e.g., _22241720P_22245804P_
                                '(Q4A|Q6A|Q8C).mp4/playlist.m3u8')  # e.g., Q4A.mp4/playlist.m3u8
    FILM_URL_EXAMPLE = 'https://apasfiis.sf.apa.at/cms-worldwide/2019-09-20_2200_tl_02_ZIB-2_Wetter__14026467__o__698276635d__s14562567_7__ORF2HD_22241720P_22245804P_Q4A.mp4/playlist.m3u8'
    FILM_URL_REGEX_MISMATCH_HELP_TEXT = 'You did not enter a valid Film-URL which looks like: \n' + FILM_URL_EXAMPLE + '\n' + \
                                        'matching the hard-coded regular expression: \n' + str(FILM_URL_REGEX).replace('re.compile(', '') + '\''

    # MediathekView was able to generate the full length file name including
    # the full length original file name which contains the detailed begin- and
    # end-timestamps at the end of the file name which ends
    # with the quality indicator Q4A or Q8C when used with the ORF sender file format.
    # examples:
    #   20180510T090000 ORF - ZIB - Signation -ORIGINAL- 2018-05-10_0900_tl_02_ZIB-9-00_Signation__13976423__o__1368225677__s14297692_2__WEB03HD_09000305P_09001400P_Q4A.mp4
    #   20190902T220000 ORF - ZIB 2 - Bericht über versteckte ÖVP-Wahlkampfkosten -ORIGINALlow- 2019-09-02_2200_tl_02_ZIB-2_Bericht-ueber-v__14024705__o__71528285d6__s14552793_3__ORF2HD_22033714P_22074303P_Q4A.mp4
    MEDIATHEKVIEW_LONG_WITH_DETAILED_TIMESTAMPS_REGEX = re.compile(MEDIATHEKVIEW_SHORT_REGEX_STRING +
                                                                   '.+__o__([a-z0-9]+)__s([a-z0-9]+)_' +   # e.g., "2018-05-10_0900_tl_02_ZIB-9-00_Signation__13976423__o__1368225677__s14297692"
                                                                   '(.+_(' + TIMESTAMP_REGEX + ').+P_(' + TIMESTAMP_REGEX + ').+P_)' +  # OPTIONAL: time-stamps of chunks: "_2__WEB03HD_09000305P_09001400P"
                                                                   '(Q4A|Q8C).mp4', re.UNICODE)  # "Q4A.mp4" for lowquality or "Q8C.mp4" for highquality

    # C112345678901EUR20150930001.pdf -> 2015-09-30 Bank Austria Kontoauszug 2017-001 12345678901.pdf
    BANKAUSTRIA_BANK_STATEMENT_REGEX = re.compile('^C1(\d{11})EUR(\d{4})(\d{2})(\d{2})(\d{3}).pdf$', re.UNICODE)
    BANKAUSTRIA_BANK_STATEMENT_INDEXGROUPS = [2, '-', 3, '-', 4, ' Bank Austria Kontoauszug ', 2, '-', 5, ' ', 1, '.pdf']

    # 2017-11-05T10.56.11_IKS-00000000512345678901234567890.csv -> 2017-11-05T10.56.11 Bank Austria Umsatzliste IKS-00000000512345678901234567890.csv
    BANKAUSTRIA_BANK_TRANSACTIONS_REGEX = re.compile('^' + DAYTIME_REGEX + '_IKS-(\d{29}).csv$', re.UNICODE)
    BANKAUSTRIA_BANK_TRANSACTIONS_INDEXGROUPS = [1, ' Bank Austria Umsatzliste IKS-', 4, '.csv']

    RECORDER_REGEX = re.compile('rec_([12]\d{3})([01]\d)([0123]\d)-([012]\d)([012345]\d)(.+)?.(wav|mp3)')

    # modet_2018-03-27_16-10.mkv
    # modet_2018-03-27_17-44-1.mkv
    MODET_REGEX = re.compile('modet_(' + DAY_REGEX + ')_' + TIME_FUZZY_REGEX + '(.*).mkv')

    # Screenshot_2017-11-29_10-32-12.png
    # Screenshot_2017-11-07_07-52-59 my description.png
    SCREENSHOT1_REGEX = re.compile('Screenshot_(' + DAY_REGEX + ')_' + TIME_FUZZY_REGEX + '(.*).png')

    # 2017-12-07_09-23_Thu Went for a walk .gpx
    OSMTRACK_REGEX = re.compile('(' + DAY_REGEX + ')_' + TIME_FUZZY_REGEX + '_(\w{3})( )?(.*).gpx')

    logger = None
    config = None

    def __init__(self, config, logger):
        self.logger = logger
        self.config = config


    def derive_new_filename_from_old_filename(self, oldfilename):
        """
        Analyses the old filename and returns a new one if feasible.
        If not, False is returned instead.

        @param oldfilename: string containing one file name
        @param return: False or new filename
        """

        logging.debug("derive_new_filename_from_old_filename called")
        datetimestr, basefilename, tags, extension = self.split_filename_entities(oldfilename)

        # Android screenshots:
        # Screenshot_2013-03-05-08-14-09.png -> 2013-03-05T08.14.09 -- android screenshots.png
        regex_match = re.match(self.ANDROID_SCREENSHOT_REGEX, oldfilename)
        if regex_match:
            return self.build_string_via_indexgroups(regex_match, self.ANDROID_SCREENSHOT_INDEXGROUPS)

        # C110014365208EUR20150930001.pdf -> 2015-09-30 Bank Austria Kontoauszug 2017-001 10014365208.pdf
        regex_match = re.match(self.BANKAUSTRIA_BANK_STATEMENT_REGEX, oldfilename)
        if regex_match:
            return self.build_string_via_indexgroups(regex_match, self.BANKAUSTRIA_BANK_STATEMENT_INDEXGROUPS)

        # 2017-11-05T10.56.11_IKS-00000000512345678901234567890.csv -> 2017-11-05T10.56.11 Bank Austria Umsatzliste IKS-00000000512345678901234567890.csv
        regex_match = re.match(self.BANKAUSTRIA_BANK_TRANSACTIONS_REGEX, oldfilename)
        if regex_match:
            return self.build_string_via_indexgroups(regex_match, self.BANKAUSTRIA_BANK_TRANSACTIONS_INDEXGROUPS)

        # MediathekView: Settings > modify Set > Targetfilename: "%DT%d %s %t - %T -ORIGINAL- %N.mp4" (without any limitation of the maximum numbers of characters)
        # results in files like:
        # with the detailed start- and end-time-stamp information of the chunks:
        #   20180510T090000 ORF - ZIB - Signation -ORIGINAL- 2018-05-10_0900_tl_02_ZIB-9-00_Signation__13976423__o__1368225677__s14297692_2__WEB03HD_09000305P_09001400P_Q4A.mp4
        #      regex_match.groups() == ('2018', '05', '10', '09', '00', '00', '00', 'ORF', 'ZIB', 'Signation', '1368225677', '14297692', '2__WEB03HD_09000305P_09001400P_', '090003', '09', '00', '03', '03', '090014', '09', '00', '14', '14', 'Q4A')
        #      -> 2018-05-10T09.00.03 ORF - ZIB - Signation -- lowquality.mp4
        #   20180510T090000 ORF - ZIB - Weitere Signale der Entspannung -ORIGINAL- 2018-05-10_0900_tl_02_ZIB-9-00_Weitere-Signale__13976423__o__5968792755__s14297694_4__WEB03HD_09011813P_09020710P_Q4A.mp4
        #      -> 2018-05-10T09.01.18 ORF - ZIB - Weitere Signale der Entspannung -- lowquality.mp4
        # without the optional time-stamp:
        #   20180520T201500 ORF - Tatort - Tatort_ Aus der Tiefe der Zeit -ORIGINAL- 2018-05-20_2015_in_02_Tatort--Aus-der_____13977411__o__1151703583__s14303062_Q8C.mp4
        #      ('2018', '05', '20', '20', '15', '00', '00', 'ORF', 'Tatort', 'Tatort_ Aus der Tiefe der Zeit', '1151703583', '14303062', None, None, None, None, None, None, None, None, None, None, None, 'Q8C')
        #      -> 2018-05-20T20.15.00 ORF - Tatort - Tatort  Aus der Tiefe der Zeit -- highquality.mp4
        #
        # MEDIATHEKVIEW_LONG_WITH_DETAILED_TIMESTAMPS_REGEX:
        #             MediathekView was able to generate the full length file name including
        #             the full length original file name at the end of the file name which ends
        #             with the quality indicator Q4A or Q8C when used with the ORF sender file format.
        #
        regex_match = re.match(self.MEDIATHEKVIEW_LONG_WITH_DETAILED_TIMESTAMPS_REGEX, oldfilename)
        if regex_match:

            logging.debug('Filename did contain detailed start- and end-timestamps. Using the full-blown time-stamp '
                          + 'information of the chunk itself: MEDIATHEKVIEW_LONG_WITH_DETAILED_TIMESTAMPS_REGEX')

            qualityindicator = regex_match.group(len(regex_match.groups())).upper()
            qualitytag = self.translate_ORF_quality_string_to_tag(qualityindicator)
            start_hrs = regex_match.group(16)
            start_min = regex_match.group(17)
            start_sec = regex_match.group(18)
            end_hrs = regex_match.group(21)
            end_min = regex_match.group(22)
            end_sec = regex_match.group(23)
            self.warn_if_ORF_file_seems_to_small_according_to_duration_and_quality_indicator(oldfilename, qualityindicator,
                                                                                             start_hrs, start_min, start_sec,
                                                                                             end_hrs, end_min, end_sec)

            if regex_match.group(13):
                # the file name contained the optional chunk time-stamp(s)
                MEDIATHEKVIEW_LONG_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', 16, '.', 17, '.', 18, ' ', 8, ' - ', 9, ' - ', 10, ' -- ', qualitytag, '.mp4']
            else:
                # the file name did NOT contain the optional chunk time-stamp(s), so we have to use the main time-stamp
                MEDIATHEKVIEW_LONG_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', 4, '.', 5, '.', 6, ' ', 8, ' - ', 9, ' - ', 10, ' -- ', qualitytag, '.mp4']
            return self.build_string_via_indexgroups(regex_match, MEDIATHEKVIEW_LONG_INDEXGROUPS).replace('_', ' ')

        # MEDIATHEKVIEW_RAW_REGEX_STRING:
        #             MediathekView ORF raw file name
        #
        regex_match = re.match(self.MEDIATHEKVIEW_RAW_REGEX_STRING, oldfilename)
        if regex_match:

            logging.debug('Filename looks like ORF raw file name: MEDIATHEKVIEW_RAW_REGEX_STRING')

            qualityindicator = regex_match.group(len(regex_match.groups())).upper()
            qualitytag = self.translate_ORF_quality_string_to_tag(qualityindicator)
            start_hrs = regex_match.group(9)
            start_min = regex_match.group(10)
            start_sec = regex_match.group(11)
            end_hrs = regex_match.group(13)
            end_min = regex_match.group(14)
            end_sec = regex_match.group(15)
            self.warn_if_ORF_file_seems_to_small_according_to_duration_and_quality_indicator(oldfilename, qualityindicator,
                                                                                             start_hrs, start_min, start_sec,
                                                                                             end_hrs, end_min, end_sec)
            # transform ...
            # 'Am-Schauplatz_-_Alles f\xc3\xbcr die Katz-____'
            # ... into ...
            # 'Am Schauplatz - Alles f\xc3\xbcr die Katz'
            title = regex_match.group(8).replace('-',' ').replace('_ _',' - ').replace('   ',' - ').replace('_','').strip()
            MEDIATHEKVIEW_RAW_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', start_hrs, '.', start_min, '.', start_sec, ' ', title, ' -- ', qualitytag, '.mp4']
            return self.build_string_via_indexgroups(regex_match, MEDIATHEKVIEW_RAW_INDEXGROUPS)

        # MEDIATHEKVIEW_LONG_WITHOUT_DETAILED_TIMESTAMPS_REGEX:
        # MediathekView was able to generate the full length file name including
        # the full length original file name which DOES NOT contain the detailed begin- and
        # end-timestamps at the end of the file name which still ends
        # with the quality indicator Q4A or Q8C when used with the ORF sender file format.
        #
        # example: 20180608T193000 ORF - Österreich Heute HD 10min - Das Magazin - Österreich Heute - Das Magazin -ORIGINAL- 13979231_0007_Q8C.mp4
        regex_match = re.match(self.MEDIATHEKVIEW_LONG_WITHOUT_DETAILED_TIMESTAMPS_REGEX, oldfilename)
        if regex_match:
            logging.debug('Filename did not contain detailed start- and end-timestamps. Using the time-stamp '
                          + 'of the chunk itself as a fall-back: MEDIATHEKVIEW_LONG_WITHOUT_DETAILED_TIMESTAMPS_REGEX')
            qualitytag = self.translate_ORF_quality_string_to_tag(regex_match.group(len(regex_match.groups())).upper())
            MEDIATHEKVIEW_LONG_INDEXGROUPS = [1, '-', 2, '-', 3, 'T', 4, '.', 5, '.', 6, ' ', 8, ' - ', 9, ' - ', 10, ' -- ', qualitytag, '.mp4']
            return self.build_string_via_indexgroups(regex_match, MEDIATHEKVIEW_LONG_INDEXGROUPS).replace('_', ' ')

        # SHORT_REGEX: if MediathekView is NOT able to generate the full length file name because
        #              of file name length restrictions, this RegEx is a fall-back in order to
        #              recognize the situation. This is clearly visible due to the missing closing
        #              quality strings: Q4A Q6A Q8C
        # This is a fall-back mechanism which requires INTERACTIVE correction: user gets asked to
        # enter the original file URL: MediathekView > context menu of a chunk > "Film-URL kopieren"
        # With this URL, guessfilename is able to extract the original time-stamps that were missing
        # in the SHORT_REGEX.
        #
        # test it manually with following data: (no unit test because of interactive input)
        # filename "20180608T214000 ORF - Was gibt es Neues? - Promifrage gestellt von Helmut Bohatsch_ Wie vergewisserte sich der Bischof von New York 1877, dass das erste Tonaufnahmegerät kein Teufelswerk ist? -ORIGINAL- 2018-06-08_2140_tl_01_Was-gibt-es-Neu_Promifr.mp4"
        # Low quality URL:
        # http://apasfpd.apa.at/cms-worldwide/online/7db1010b02753288e65ff61d5e1dff58/1528531468/2018-06-08_2140_tl_01_Was-gibt-es-Neu_Promifrage-gest__13979244__o__1391278651__s14313058_8__BCK1HD_22050122P_22091314P_Q4A.mp4
        # High quality URL:
        # http://apasfpd.apa.at/cms-worldwide/online/549c11b7cf10c9a232361003d78e5335/1528531468/2018-06-08_2140_tl_01_Was-gibt-es-Neu_Promifrage-gest__13979244__o__1391278651__s14313058_8__BCK1HD_22050122P_22091314P_Q6A.mp4
        # HD URL:
        # http://apasfpd.apa.at/cms-worldwide/online/6ade5772382b0833525870b4a290692c/1528531468/2018-06-08_2140_tl_01_Was-gibt-es-Neu_Promifrage-gest__13979244__o__1391278651__s14313058_8__BCK1HD_22050122P_22091314P_Q8C.mp4
        regex_match = re.match(self.MEDIATHEKVIEW_SHORT_REGEX, oldfilename)
        if regex_match:

            logging.debug('Filename did not contain detailed start- and end-timestamps and no quality indicators. Using the time-stamp '
                          + 'of the "Film-URL" as a fall-back: MEDIATHEKVIEW_SHORT_REGEX + FILM_URL_REGEX')

            if regex_match.group(12) == 'playlist.m3u8' and regex_match.group(11):
                # We got this simple case of failing to get "original filename" from MediathekView download source:
                # '20181028T201400 ORF - Tatort - Tatort_ Blut -ORIGINALhd- playlist.m3u8.mp4'
                # There is NO original filename containing the starting time :-(
                # (see unit tests for details)

                # "lowquality" or "highquality" or "UNKNOWNQUALITY"
                qualitytag = self.translate_ORF_quality_string_to_tag(regex_match.group(11).upper())

                return self.build_string_via_indexgroups(regex_match, [1, '-', 2, '-', 3, 'T', 4, '.', 5, '.', 7, ' ', 8, ' - ', 9, ' - ', 10, ' -- ', qualitytag, '.mp4'])

            else:
                # we got the ability to derive starting time from "original filename"
                logging.warn('I recognized a MediathekView file which has a cut-off time-stamp because ' +
                             'of file name length restrictions.\nYou can fix it manually:')

                url_valid = False
                while not url_valid:

                    film_url = input("\nPlease enter: MediathekView > context menu of the " +
                                     "corresponding chunk > \"Film-URL kopieren\":\n")

                    # URL has format like: http://apasfpd.apa.at/cms-worldwide/online/7db1010b02753288e65ff61d5e1dff58/1528531468/2018-06-08_2140_tl_01_Was-gibt-es-Neu_Promifrage-gest__13979244__o__1391278651__s14313058_8__BCK1HD_22050122P_22091314P_Q4A.mp4
                    # but with varying quality indicator: Q4A (low), Q6A (high), Q8C (HD)
                    film_regex_match = re.match(self.FILM_URL_REGEX, film_url)

                    if not film_regex_match:
                        print()
                        logging.warn(self.FILM_URL_REGEX_MISMATCH_HELP_TEXT)
                        logging.debug('entered film_url:\n' + film_url)
                    elif regex_match.groups()[:5] != film_regex_match.groups()[1:6]:
                        logging.debug('plausibility check fails: date and time of the chunks differ: \nselected regex_match.groups is   "' +
                                      str(regex_match.groups()[:5]) + '" which does not match\nselected film_regex_match.groups "' +
                                      str(film_regex_match.groups()[1:6]) + '". Maybe adapt the potentially changed index group numbers due to changed RegEx?')
                        logging.warn('Sorry, there is a mismatch of the date and time contained between the filename (' +
                                     self.build_string_via_indexgroups(regex_match, [1, '-', 2, '-', 3, 'T', 4, '.', 5]) +
                                     ') and the URL pasted (' +
                                     self.build_string_via_indexgroups(film_regex_match, [1, '-', 2, '-', 3, 'T', 4, '.', 5]) +
                                     '). Please try again with the correct URL ...')
                    else:
                        url_valid = True

                # "lowquality" or "highquality" or "UNKNOWNQUALITY"
                qualitytag = self.translate_ORF_quality_string_to_tag(film_regex_match.group(len(film_regex_match.groups())).upper())

                # e.g., "2018-06-08T"
                datestamp = self.build_string_via_indexgroups(regex_match, [1, '-', 2, '-', 3, 'T'])

                # e.g., "22.05.01 "
                timestamp = self.build_string_via_indexgroups(film_regex_match, [10, '.', 11, '.', 12, ' '])

                # e.g., "ORF - Was gibt es Neues? - Promifrage gestellt von Helmut Bohatsch_ Wie vergewisserte sich der Bischof von New York 1877, dass das erste Tonaufnahmegerät kein Teufelswerk ist? -- lowquality.mp4"
                description = self.build_string_via_indexgroups(regex_match, [8, ' - ', 9, ' - ', 10, ' -- ', qualitytag, '.mp4'])

                # combining them all to one final filename:
                return datestamp + timestamp + description

        # OLD # # MediathekView: Settings > modify Set > Targetfilename: "%DT%d h%i %s %t - %T - %N.mp4"
        # OLD # # results in files like:
        # OLD # #   20161227T201500 h115421 ORF Das Sacher. In bester Gesellschaft 1.mp4
        # OLD # #     -> 2016-12-27T20.15.00 h115421 ORF Das Sacher. In bester Gesellschaft 1.mp4
        # OLD # #   20161227T193000 l119684 ORF ZIB 1 - Auswirkungen der _Panama-Papers_ - 2016-12-27_1930_tl_02_ZIB-1_Auswirkungen-de__.mp4
        # OLD # #     -> 2016-12-27T19.30.00 l119684 ORF ZIB 1 - Auswirkungen der _Panama-Papers_.mp4
        # OLD # regex_match = re.match(self.MEDIATHEKVIEW_SIMPLE_REGEX, oldfilename)
        # OLD # if regex_match:
        # OLD #     if 'Tatort' in oldfilename and os.stat(oldfilename).st_size < 2000000000 and not options.quiet:
        # OLD #         print('       →  ' + colorama.Style.BRIGHT + colorama.Fore.RED + 'WARNING: Tatort file seems to be too small (download aborted?): ' + oldfilename + colorama.Style.RESET_ALL)
        # OLD #     return self.build_string_via_indexgroups(regex_match, self.MEDIATHEKVIEW_SIMPLE_INDEXGROUPS).replace('_', ' ')

        # Android OSMTracker GPS track files:
        # 2015-05-27T09;00;15_foo_bar.gpx -> 2015-05-27T09.00.15 foo bar.gpx
        regex_match = re.match(self.OSMTRACKS_REGEX, oldfilename)
        if regex_match:
            return self.build_string_via_indexgroups(regex_match, self.OSMTRACKS_INDEXGROUPS).replace('_', ' ')

        # digital camera images: IMG_20161014_214404 foo bar.jpg -> 2016-10-14T21.44.04 foo bar.jpg  OR
        regex_match = re.match(self.IMG_REGEX, oldfilename)
        if regex_match:
            if regex_match.group(8) == '_Bokeh':
                return self.build_string_via_indexgroups(regex_match, self.IMG_INDEXGROUPS_BOKEH)
            else:
                return self.build_string_via_indexgroups(regex_match, self.IMG_INDEXGROUPS_NORMAL)
        #                        VID_20170105_173104.mp4         -> 2017-01-05T17.31.04.mp4
        regex_match = re.match(self.VID_REGEX, oldfilename)
        if regex_match:
            return self.build_string_via_indexgroups(regex_match, self.VID_INDEXGROUPS)

        # 2018-04-01:
        # signal-2018-03-08-102332.jpg → 2018-03-08T10.23.32.jpg
        # signal-2018-03-08-102332 foo bar.jpg → 2018-03-08T10.23.32 foo bar.jpg
        # signal-attachment-2019-11-23-090716_001.jpeg -> 2019-11-23T09.07.16_001.jpeg
        regex_match = re.match(self.SIGNAL_REGEX, oldfilename)
        if regex_match:
            if regex_match.group(9):
                result = self.build_string_via_indexgroups(regex_match, [2, '-', 3, '-', 4, 'T', 5, '.', 6, '.', 7, 9, 10])
            else:
                result = self.build_string_via_indexgroups(regex_match, [2, '-', 3, '-', 4, 'T', 5, '.', 6, '.', 7, '.jpg'])
            return result

        # 2018-03-27:
        # modet_2018-03-27_16-10.mkv
        # modet_2018-03-27_17-44-1.mkv
        regex_match = re.match(self.MODET_REGEX, oldfilename)
        if regex_match:
            result = self.build_string_via_indexgroups(regex_match, [1, 'T', 2, '.', 3, ' modet ', 6, '.mkv'])
            return result


        # 2017-11-30:
        # rec_20171129-0902 A nice recording .wav -> 2017-11-29T09.02 A nice recording.wav
        # rec_20171129-0902 A nice recording.wav  -> 2017-11-29T09.02 A nice recording.wav
        # rec_20171129-0902.wav -> 2017-11-29T09.02.wav
        # rec_20171129-0902.mp3 -> 2017-11-29T09.02.mp3
        regex_match = re.match(self.RECORDER_REGEX, oldfilename)
        if regex_match:
            result = self.build_string_via_indexgroups(regex_match, [1, '-', 2, '-', 3, 'T', 4, '.', 5])
            if regex_match.group(6):
                result += ' ' + regex_match.group(6).strip()
            return result + '.' + regex_match.group(7)

        # 2019-04-01 oekostrom AG - Teilbetragsrechnung Stromverbrauch 54 EUR -- scan bill.pdf
        if 'teilbetragsrechnung' in oldfilename.lower() and \
           'oekostrom' in oldfilename.lower() and \
           datetimestr and self.has_euro_charge(oldfilename):
            return datetimestr + \
                " oekostrom AG - Teilbetragsrechnung Stromverbrauch " + \
                self.get_euro_charge(oldfilename) + \
                "€ -- " + ' '.join(self.adding_tags(tags, ['scan', 'bill'])) + \
                ".pdf"

        # 2015-11-24 Rechnung A1 Festnetz-Internet 12,34€ -- scan bill.pdf
        if self.contains_one_of(oldfilename, [" A1 ", " a1 "]) and self.has_euro_charge(oldfilename) and datetimestr:
            return datetimestr + \
                " A1 Festnetz-Internet " + self.get_euro_charge(oldfilename) + \
                "€ -- " + ' '.join(self.adding_tags(tags, ['scan', 'bill'])) + \
                ".pdf"

        # 2016-01-19--2016-02-12 benutzter GVB 10er Block -- scan transportation graz.pdf
        if self.contains_one_of(oldfilename, ["10er"]) and datetimestr:
            return datetimestr + \
                " benutzter GVB 10er Block" + \
                " -- " + ' '.join(self.adding_tags(tags, ['scan', 'transportation', 'graz'])) + \
                ".pdf"

        # 2016-01-19 bill foobar baz 12,12EUR.pdf -> 2016-01-19 foobar baz 12,12€ -- scan bill.pdf
        if 'bill' in oldfilename and datetimestr and self.has_euro_charge(oldfilename):
            return datetimestr + ' ' + \
                basefilename.replace(' bill', ' ').replace('bill ', ' ').replace('  ', ' ').replace('EUR', '€').strip() + \
                " -- " + ' '.join(self.adding_tags(tags, ['scan', 'bill'])) + \
                ".pdf"

        # 2015-04-30 FH St.Poelten - Abrechnungsbeleg 12,34 EUR - Honorar -- scan fhstp.pdf
        if self.contains_all_of(oldfilename, [" FH ", "Abrechnungsbeleg"]) and self.has_euro_charge(oldfilename) and datetimestr:
            return datetimestr + \
                " FH St.Poelten - Abrechnungsbeleg " + self.get_euro_charge(oldfilename) + \
                "€ Honorar -- " + ' '.join(self.adding_tags(tags, ['scan', 'fhstp'])) + \
                ".pdf"

        # 2016-02-26 Gehaltszettel Februar 12,34 EUR -- scan infonova.pdf
        if self.contains_all_of(oldfilename, ["Gehalt", "infonova"]) and self.has_euro_charge(oldfilename) and datetimestr:
            return datetimestr + \
                " Gehaltszettel " + self.get_euro_charge(oldfilename) + \
                "€ -- " + ' '.join(self.adding_tags(tags, ['scan', 'infonova'])) + \
                ".pdf"

        # 2012-05-26T22.25.12_IMAG0861 Rage Ergebnis - MITSPIELER -- games.jpg
        if self.contains_one_of(basefilename, ["Hive", "Rage", "Stratego"]) and \
           extension.lower() == 'jpg' and not self.has_euro_charge(oldfilename):
            return datetimestr + basefilename + \
                " - Ergebnis -- games" + \
                ".jpg"

        # 2015-03-11 VBV Kontoinformation 123 EUR -- scan finance infonova.pdf
        if self.contains_all_of(oldfilename, ["VBV", "Kontoinformation"]) and self.has_euro_charge(oldfilename) and datetimestr:
            return datetimestr + \
                " VBV Kontoinformation " + self.get_euro_charge(oldfilename) + \
                "€ -- " + ' '.join(self.adding_tags(tags, ['scan', 'finance', 'infonova'])) + \
                ".pdf"

        # 2015-03-11 Verbrauchsablesung Wasser - Holding Graz -- scan bwg.pdf
        if self.contains_all_of(oldfilename, ["Verbrauchsablesung", "Wasser"]) and datetimestr:
            return datetimestr + \
                " Verbrauchsablesung Wasser - Holding Graz -- " + \
                ' '.join(self.adding_tags(tags, ['scan', 'bwg'])) + \
                ".pdf"

        # 2017-09-23 Hipster-PDA file: 2017-08-16-2017-09-23 Hipster-PDA vollgeschrieben -- scan notes.(png|pdf)
        if datetimestr and self.contains_one_of(oldfilename, ["hipster", "Hipster"]):
            return datetimestr + ' Hipster-PDA vollgeschrieben -- scan notes.' + extension

        # 2018-05-05: Files generated by "Easy Screenshot" (Firefox add-on)
        # Firefox_Screenshot_2018-05-03T20-07-14.972Z.png
        regex_match = re.match(self.EASY_SCREENSHOT_REGEX, oldfilename)
        if regex_match:
            return self.build_string_via_indexgroups(regex_match, self.EASY_SCREENSHOT_INDEXGROUPS)

        # 2017-12-02: Files from screenshots from xfce-tool "Screenshot"
        # example: Screenshot_2017-11-07_07-52-59 my description.png
        regex_match = re.match(self.SCREENSHOT1_REGEX, oldfilename)
        if regex_match:
            if regex_match.group(6):
                # there is a description with a leading space after the time
                my_description = regex_match.group(6)
            else:
                my_description = ''
            return self.build_string_via_indexgroups(regex_match, [1, 'T', 2, '.', 3, '.', 5, my_description, ' -- screenshots.png'])

        # 2017-12-07_09-23_Thu Went for a walk .gpx
        regex_match = re.match(self.OSMTRACK_REGEX, oldfilename)
        if regex_match:
            if regex_match.group(8):
                description = regex_match.group(8).strip()
                return self.build_string_via_indexgroups(regex_match, [1, 'T', 2, '.', 3, ' ', description, '.gpx'])
            else:
                return self.build_string_via_indexgroups(regex_match, [1, 'T', 2, '.', 3, '.gpx'])

        # 2019-05-24: this is a workaround until PDF file decryption in PyPDF2 is fixed for parsing the content id:2019-05-24-guessfilename-salary
        if extension.upper() == "PDF" and self.config.SALARY_STARTSTRING in oldfilename and datetimestr:
            # print out password to stdout in order to give the user a
            # hint when he wants to open the PDF in a PDF viewer
            print(' ' * 7 + colorama.Style.DIM + '→  PDF file password: ' + self.config.SALARY_PDF_PASSWORD +
                  colorama.Style.RESET_ALL)
            return datetimestr + ' ' + self.config.SALARY_DESCRIPTION + ' MONTH - SALARY' + \
                '€ -- detego private.pdf'

        # 2019-10-10: '2019-10-10 a file exported by Boox Max 2-Exported.pdf' or
        #             '2019-10-10 a file exported by Boox Max 2 -- notes-Exported.pdf' become
        #         ->  '2019-10-10 a file exported by Boox Max 2 -- notes.pdf'
        if extension.upper() == "PDF" and oldfilename.upper().endswith('-EXPORTED.PDF'):
            if self.contains_all_of(oldfilename, [" -- ", " notes"]):
                # FIXXME: assumption is that "notes" is within the
                #         filetags and not anywhere else:
                # '2019-10-10 a file exported by Boox Max 2 -- notes-Exported.pdf'
                return oldfilename[:-13] + '.pdf'
            else:
                if ' -- ' in oldfilename:
                    # filetags found but not containing "notes":
                    # '2019-10-10 a file exported by Boox Max 2 -- draft-Exported.pdf'
                    return oldfilename[:-13] + ' notes.pdf'
                else:
                    # no filetags found so far:
                    # '2019-10-10 a file exported by Boox Max 2-Exported.pdf'
                    return oldfilename[:-13] + ' -- notes.pdf'

        # FIXXME: more cases!

        return False  # no new filename found

    def derive_new_filename_from_content(self, dirname, basename):
        """
        Analyses the content of basename and returns a new file name if feasible.
        If not, False is returned instead.

        @param dirname: string containing the directory of file within basename
        @param basename: string containing one file name
        @param return: False or new filename
        """

        filename = os.path.join(dirname, basename)
        assert os.path.isfile(filename)
        #logging.debug("derive_new_filename_from_content(self, \"%s\", \"%s\") called" % (dirname, basename))

        datetimestr, basefilename, tags, extension = self.split_filename_entities(basename)

        if extension.lower() != 'pdf':
            logging.debug("File is not a PDF file and thus can't be parsed by this script: %s" % filename)
            return False

        try:
            pdffile = PyPDF2.PdfFileReader(open(filename, "rb"))

            # if PDF is encryped, try password stored in config file
            # or quit this function if decryption is not successful
            if pdffile.isEncrypted:
                returncode = pdffile.decrypt(self.config.SALARY_PDF_PASSWORD)
                if returncode < 1:
                    logging.error('PDF file is encrypted and could NOT be decrypted using ' +
                                  'config.SALARY_PDF_PASSWORD. Skipping content analysis.')
                    return False
                else:
                    logging.debug('PDF file is encrypted and could be decrypted using ' +
                                  'config.SALARY_PDF_PASSWORD. Return code = ' + str(returncode))

            # use first and second page of content only:
            if pdffile.getNumPages() > 1:
                content = pdffile.pages[0].extractText() + pdffile.pages[1].extractText()
            elif pdffile.getNumPages() == 1:
                content = pdffile.pages[0].extractText()
            else:
                logging.error('Could not determine number of pages of PDF content! (skipping content analysis)')
                return False
        except:
            logging.error('Could not read PDF file content. Skipping its content.')
            return False

        if len(content) == 0:
            logging.info('Could read PDF file content but it is empty (skipping content analysis)')
            return False

        # Salary - NOTE: this is highly specific to the PDF file
        # structure of the author's salary processing software.
        # Therefore, this most likely does not work for your salary
        # PDF file.
        if extension.upper() == "PDF" and self.config.SALARY_STARTSTRING in filename:
            #content = content.replace('\n', '')  # there is a '\n' after each character
            # 2019-05-24: new file format for salary PDF can not be parsed by PyPDF2: id:2019-05-24-guessfilename-salary
            ##   File "/home/vk/bin/guessfilename", line 1055, in derive_new_filename_from_content
            ##     returncode = pdffile.decrypt(self.config.SALARY_PDF_PASSWORD)
            ##   File "/usr/lib/python3/dist-packages/PyPDF2/pdf.py", line 1987, in decrypt
            ##     return self._decrypt(password)
            ##   File "/usr/lib/python3/dist-packages/PyPDF2/pdf.py", line 1996, in _decrypt
            ##     raise NotImplementedError("only algorithm code 1 and 2 are supported")
            ## NotImplementedError: only algorithm code 1 and 2 are supported
            ##
            ## producer of PDF file: "wPDF4 by WPCubed GmbH" "PDF v. 1.7"
            ## might relate to: https://github.com/mstamy2/PyPDF2/issues/378

            try:
                # should parse starting sequence of
                # "^.LOHN/GEHALTSABRECHNUNG JÄNNER 2018Klien..." and
                # return "Jaenner"
                month_of_salary = re.match(r'.LOHN.*/.*GEHALTSABRECHNUNG (.+) .+', content).group(1).capitalize().replace('ä', 'ae')
            except:
                logging.error('derive_new_filename_from_content(' + filename + '): I recognized pattern ' +
                              'for salary file but content format for extracting month must have changed.')
                month_of_salary = 'FIXXME'
            try:
                # should extract "2.345,67" from following sequence
                # ".+SZAbzüge1.234,56Netto2.345,67IBAN:.+"
                net_salary = re.match(r'.+Netto(\d\.\d{3},\d{2})IBAN.+', content).group(1)
            except:
                logging.error('derive_new_filename_from_content(' + filename + '): I recognized pattern ' +
                              'for salary file but content format for extracting net salary must have changed.')
                net_salary = 'FIXXME'
            # print out password to stdout in order to give the user a
            # hint when he wants to open the PDF in a PDF viewer
            print(' ' * 7 + colorama.Style.DIM + '→  PDF file password: ' + self.config.SALARY_PDF_PASSWORD +
                  colorama.Style.RESET_ALL)
            return datetimestr + ' ' + self.config.SALARY_DESCRIPTION + ' ' + month_of_salary + ' - ' + \
                net_salary + '€ -- detego private.pdf'

        # 2010-06-08 easybank - neue TAN-Liste -- scan private.pdf
        if self.fuzzy_contains_all_of(content, ["Transaktionsnummern (TANs)", "Ihre TAN-Liste in Verlust geraten"]) and \
           datetimestr:
            return datetimestr + \
                " easybank - neue TAN-Liste -- " + \
                ' '.join(self.adding_tags(tags, ['scan', 'private'])) + \
                ".pdf"

        # 2015-11-20 Kirchenbeitrag 12,34 EUR -- scan taxes bill.pdf
        if self.fuzzy_contains_all_of(content, ["4294-0208", "AT086000000007042401"]) and \
           datetimestr:
            floatstr = self.get_euro_charge_from_context_or_basename(content, "Offen", "Zahlungen", basename)
            return datetimestr + \
                " Kirchenbeitrag " + floatstr + "€ -- " + \
                ' '.join(self.adding_tags(tags, ['scan', 'taxes', 'bill'])) + \
                ".pdf"

        # 2015-11-24 Generali Erhoehung Dynamikklausel - Praemie nun 12,34 - Polizze 12345 -- scan bill.pdf
        if self.config and self.config.GENERALI1_POLIZZE_NUMBER in content and \
           self.fuzzy_contains_all_of(content, ["ImHinblickaufdievereinbarteDynamikklauseltritteineWertsteigerunginKraft",
                                                "IhreangepasstePrämiebeträgtdahermonatlich",
                                                "AT44ZZZ00000002054"]) and datetimestr:
            floatstr = self.get_euro_charge_from_context_or_basename(content,
                                                                     "IndiesemBetragistauchdiegesetzlicheVersicherungssteuerenthalten.EUR",
                                                                     "Wird",
                                                                     basename)
            return datetimestr + \
                " Generali Erhoehung Dynamikklausel - Praemie nun " + floatstr + \
                "€ - Polizze " + self.config.GENERALI1_POLIZZE_NUMBER + " -- " + \
                ' '.join(self.adding_tags(tags, ['scan', 'bill'])) + \
                ".pdf"

        # 2015-11-30 Merkur Lebensversicherung 123456 - Praemienzahlungsaufforderung 12,34€ -- scan bill.pdf
        if self.config and self.config.MERKUR_GESUNDHEITSVORSORGE_NUMBER in content and \
           self.fuzzy_contains_all_of(content, ["Prämienvorschreibung",
                                                self.config.MERKUR_GESUNDHEITSVORSORGE_ZAHLUNGSREFERENZ]) and datetimestr:
            floatstr = self.get_euro_charge_from_context_or_basename(content,
                                                                     "EUR",
                                                                     "Gesundheit ist ein kostbares Gut",
                                                                     basename)
            return datetimestr + \
                " Merkur Lebensversicherung " + self.config.MERKUR_GESUNDHEITSVORSORGE_NUMBER + \
                " - Praemienzahlungsaufforderung " + floatstr + \
                "€ -- " + \
                ' '.join(self.adding_tags(tags, ['scan', 'bill'])) + \
                ".pdf"

        # 2016-02-22 BANK - Darlehnen - Kontomitteilung -- scan taxes.pdf
        if self.config and self.fuzzy_contains_all_of(content, [self.config.LOAN_INSTITUTE, self.config.LOAN_ID]) and datetimestr:
            return datetimestr + \
                " " + self.config.LOAN_INSTITUTE + " - Darlehnen - Kontomitteilung -- " + \
                ' '.join(self.adding_tags(tags, ['scan', 'taxes'])) + \
                ".pdf"

        # 2015-11-24 Rechnung A1 Festnetz-Internet 12,34€ -- scan bill.pdf
        if self.config and self.fuzzy_contains_all_of(content, [self.config.PROVIDER_CONTRACT, self.config.PROVIDER_CUE]) and datetimestr:
            floatstr = self.get_euro_charge_from_context_or_basename(content,
                                                                     "\u2022",
                                                                     "Bei Online Zahlungen geben Sie",
                                                                     basename)
            return datetimestr + \
                " A1 Festnetz-Internet " + floatstr + \
                "€ -- " + ' '.join(self.adding_tags(tags, ['scan', 'bill'])) + \
                ".pdf"

        # FIXXME: more file documents

        return False

    def derive_new_filename_from_json_metadata(self, dirname, basename, json_metadata_file):
        """
        Analyses the content of a JSON metadata file which shares the same basename with the extension '.info.json' and returns a new file name if feasible.
        If not, False is returned instead.

        For example, youtube-dl retrieves such files from sources like YouTube with 'youtube-dl --write-info-json $URL'

        @param dirname: string containing the directory of file within basename
        @param basename: string containing one file name
        @param json_metadata_file: string containing file name for the JSON metadata file
        @param return: False or new filename
        """

        json_data=open(os.path.join(dirname, json_metadata_file))
        data = json.load(json_data)

        if "upload_date" in data.keys() and \
           "extractor" in data.keys() and \
           "display_id" in data.keys() and \
           "ext" in data.keys() and \
           "fulltitle" in data.keys():

            if data['upload_date'] and len(data['upload_date']) == 8 and \
               data["extractor_key"] and data["extractor_key"] == "Youtube":
                logging.debug('derive_new_filename_from_json_metadata: found all ' +
                              'required meta data for YouTube download file style')
                # example from unit tests: "2007-09-13 youtube - The Star7 PDA Prototype - Ahg8OBYixL0.mp4"
                return data['upload_date'][:4] + '-' + data['upload_date'][4:6] + '-' + data['upload_date'][6:] + ' ' + data["extractor"] + ' - ' + data["fulltitle"] + ' - ' + data["display_id"] + '.' + data["ext"]
            else:
                logging.debug('derive_new_filename_from_json_metadata: found all required meta data ' +
                              'for YouTube download file style but upload_date or extractor_key do ' +
                              'not match expected format')

        if "extractor_key" in data.keys() and \
           "fulltitle" in data.keys() and \
           "url" in data.keys() and \
           "ext" in data.keys():
            if data["extractor_key"] == "ORFTVthek":
                logging.debug('derive_new_filename_from_json_metadata: found all ' +
                              'required meta data for ORF TVthek download file style')
                # example from unit tests: "2019-10-17T16.59.07 ORF - ZIB 17 00 - Durchbruch bei Brexit-Verhandlungen -- highquality.mp4"

                # data['url'] == 'https://apasfiis.sf.apa.at/cms-worldwide_nas/_definst_/nas/cms-worldwide/online/2019-10-17_1700_tl_02_ZIB-17-00_Durchbruch-bei-__14029194__o__9751208575__s14577219_9__ORF2BHD_16590721P_17000309P_Q8C.mp4/chunklist.m3u8'
                # data['url'].split('/') == ['https:', '', 'apasfiis.sf.apa.at', 'cms-worldwide_nas', '_definst_', 'nas', 'cms-worldwide', 'online', '2019-10-17_1700_tl_02_ZIB-17-00_Durchbruch-bei-__14029194__o__9751208575__s14577219_9__ORF2BHD_16590721P_17000309P_Q8C.mp4', 'chunklist.m3u8']
                # data['url'].split('/')[-2:-1][0] == '2019-10-17_1700_tl_02_ZIB-17-00_Durchbruch-bei-__14029194__o__9751208575__s14577219_9__ORF2BHD_16590721P_17000309P_Q8C.mp4'

                # match.groups() == ('2019', '10', '17', '17', '00', None, None, 'ZIB-17-00_Durchbruch-bei-_', '16', '59', '07', '07', '17', '00', '03', '03', 'Q8C')

                # JSON:
                # "extractor_key": "ORFTVthek",
                # "fulltitle": "Durchbruch bei Brexit-Verhandlungen",
                # "url": "https://apasfiis.sf.apa.at/cms-worldwide_nas/_definst_/nas/cms-worldwide/online/
                #    2019-10-17_1700_tl_02_ZIB-17-00_Durchbruch-bei-__14029194__o__9751208575__s14577219_9__ORF2BHD_16590721P_17000309P_Q8C.mp4/chunklist.m3u8",
                # "ext": "mp4",

                match = re.match(self.MEDIATHEKVIEW_RAW_REGEX_STRING, data['url'].split('/')[-2:-1][0])
                qualityindicator = self.translate_ORF_quality_string_to_tag(match.group(17))  # e.g., 'Q8C'
                return self.build_string_via_indexgroups(match, [1, '-', 2, '-', 3, 'T', 9, '.', 10, '.', 11, ' ORF - ']) + \
                    match.group(8).split('_')[0].replace('-', ' ') + ' - ' + data['fulltitle'] + ' -- ' + qualityindicator + '.' + data['ext']

            else:
                logging.debug('derive_new_filename_from_json_metadata: found all required meta data ' +
                              'for ORF TVthek download file style but extractor_key does ' +
                              'not match expected format')

        else:
            logging.debug('derive_new_filename_from_json_metadata: do not ' +
                          'understand this type of JSON meta data')
            return False

        json_data.close()

    def handle_file(self, oldfilename, dryrun):
        """
        @param oldfilename: string containing one file name
        @param dryrun: boolean which defines if files should be changed (False) or not (True)
        @param return: error value or new filename
        """

        assert oldfilename.__class__ == str or \
            oldfilename.__class__ == str
        if dryrun:
            assert dryrun.__class__ == bool

        if os.path.isdir(oldfilename):
            logging.debug("handle_file: Skipping directory \"%s\" because this tool only renames file names." % oldfilename)
            return
        elif not os.path.isfile(oldfilename):
            logging.debug("handle_file: file type error in folder [%s]: file type: is file? %s  -  is dir? %s  -  is mount? %s" %
                          (os.getcwd(), str(os.path.isfile(oldfilename)), str(os.path.isdir(oldfilename)), str(os.path.islink(oldfilename))))
            logging.error("Skipping \"%s\" because this tool only renames existing file names." % oldfilename)
            return

        print('\n   ' + colorama.Style.BRIGHT + oldfilename + colorama.Style.RESET_ALL + '  ...')
        dirname = os.path.abspath(os.path.dirname(oldfilename))
        logging.debug("————→ dirname  [%s]" % dirname)
        basename = os.path.basename(oldfilename)
        logging.debug("————→ basename [%s]" % basename)

        newfilename = self.derive_new_filename_from_old_filename(basename)
        if newfilename:
            logging.debug("handle_file: derive_new_filename_from_old_filename returned new filename: %s" % newfilename)
        else:
            logging.debug("handle_file: derive_new_filename_from_old_filename could not derive a new filename for %s" % basename)

        if not newfilename:
            if os.path.splitext(basename)[1].lower() == '.pdf':
                newfilename = self.derive_new_filename_from_content(dirname, basename)
                logging.debug("handle_file: derive_new_filename_from_content returned new filename: %s" % newfilename)
            else:
                logging.debug("handle_file: file extension is not PDF and therefore I skip analyzing file content")

        if not newfilename:
            json_metadata_file = os.path.join(dirname, os.path.splitext(basename)[0] + '.info.json')
            if os.path.isfile(json_metadata_file):
                logging.debug("handle_file: found a json metadata file: %s   … parsing it …" % json_metadata_file)
                newfilename = self.derive_new_filename_from_json_metadata(dirname, basename, json_metadata_file)
                logging.debug("handle_file: derive_new_filename_from_json_metadata returned new filename: %s" % newfilename)
            else:
                logging.debug("handle_file: No json metadata file found")

        if newfilename:
            self.rename_file(dirname, basename, newfilename, dryrun)
            move_to_success_dir(dirname, newfilename)
            return newfilename
        else:
            logging.warning("I failed to derive new filename: not enough cues in file name or PDF file content")
            move_to_error_dir(dirname, basename)
            return False

    def adding_tags(self, tagarray, newtags):
        """
        Returns unique array of tags containing the newtag.

        @param tagarray: a array of unicode strings containing tags
        @param newtag: a array of unicode strings containing tags
        @param return: a array of unicode strings containing tags
        """

        assert tagarray.__class__ == list
        assert newtags.__class__ == list

        resulting_tags = tagarray

        for tag in newtags:
            if tag not in tagarray:
                resulting_tags.append(tag)

        return resulting_tags

    def split_filename_entities(self, filename):
        """
        Takes a filename of format ( (date(time)?)?(--date(time)?)? )? filename (tags)? (extension)?
        and returns a set of (date/time/duration, filename, array of tags, extension).
        """

        # FIXXME: return directory as well!

        assert(type(filename) == str or type(filename) == str)
        assert(len(filename) > 0)

        components = re.match(self.ISO_NAME_TAGS_EXTENSION_REGEX, filename)

        assert(components)

        if components.group(self.TAGS_INDEX):
            tags = components.group(self.TAGS_INDEX).split(' ')
        else:
            tags = []
        return components.group(self.DAYTIME_DURATION_INDEX), \
            components.group(self.NAME_INDEX), \
            tags, \
            components.group(self.EXTENSION_INDEX)

    def contains_one_of(self, string, entries):
        """
        Returns true, if the string contains one of the strings within entries array
        """

        assert(type(string) == str or type(string) == str)
        assert(type(entries) == list)
        assert(len(string) > 0)
        assert(len(entries) > 0)

        for entry in entries:
            if entry in string:
                return True

        return False

    def contains_all_of(self, string, entries):
        """
        Returns true, if the string contains all of the strings within entries array
        """

        assert(type(string) == str or type(string) == str)
        assert(type(entries) == list)
        assert(len(string) > 0)
        assert(len(entries) > 0)

        for entry in entries:
            if entry not in string:
                return False

        return True

    def fuzzy_contains_one_of(self, string, entries):
        """
        Returns true, if the string contains a similar one of the strings within entries array
        """

        assert(type(string) == str or type(string) == str)
        assert(type(entries) == list)
        assert(len(string) > 0)
        assert(len(entries) > 0)

        for entry in entries:
            similarity = fuzz.partial_ratio(string, entry)
            if similarity > 64:
                # logging.debug(u"MATCH   fuzzy_contains_one_of(%s, %s) == %i" % (string, str(entry), similarity))
                return True
            else:
                # logging.debug(u"¬ MATCH fuzzy_contains_one_of(%s, %s) == %i" % (string, str(entry), similarity))
                pass

        return False

    def fuzzy_contains_all_of(self, string, entries):
        """
        Returns true, if the string contains all similar ones of the strings within the entries array
        """

        assert(type(string) == str or type(string) == str)
        assert(type(entries) == list)
        assert(len(string) > 0)
        assert(len(entries) > 0)

        for entry in entries:
            assert(type(entry) == str or type(entry) == str)
            # logging.debug(u"fuzzy_contains_all_of(%s..., %s...) ... " % (string[:30], str(entry[:30])))
            if entry not in string:
                # if entry is found in string (exactly), try with fuzzy search:

                similarity = fuzz.partial_ratio(string, entry)
                if similarity > 64:
                    # logging.debug(u"MATCH   fuzzy_contains_all_of(%s..., %s) == %i" % (string[:30], str(entry), similarity))
                    pass
                else:
                    # logging.debug(u"¬ MATCH fuzzy_contains_all_of(%s..., %s) == %i" % (string[:30], str(entry), similarity))
                    return False

        return True

    def has_euro_charge(self, string):
        """
        Returns true, if the single-line string contains a number with a €-currency
        """

        assert(type(string) == str or type(string) == str)
        assert(len(string) > 0)

        components = re.match(self.EURO_CHARGE_REGEX, string)

        if components:
            return True
        else:
            return False

    def get_euro_charge(self, string):
        """
        Returns the first included €-currency within single-line "string" or False
        """

        assert(type(string) == str or type(string) == str)
        assert(len(string) > 0)

        components = re.match(self.EURO_CHARGE_REGEX, string)

        if components:
            return components.group(self.EURO_CHARGE_INDEX)
        else:
            return False

    def get_euro_charge_from_context_or_basename(self, string, before, after, basename):
        """
        Returns the included €-currency which is between before and after
        strings or within the basename or return 'FIXXME'
        """

        charge = self.get_euro_charge_from_context(string, before, after)
        if not charge:
            charge = self.get_euro_charge(basename)
            if not charge:
                return 'FIXXME'

        return charge

    def get_euro_charge_from_context(self, string, before, after):
        """
        Returns the included €-currency which is between before and after strings or False
        """

        assert(type(string) == str or type(string) == str)
        assert(type(before) == str or type(before) == str)
        assert(type(after) == str or type(after) == str)
        assert(len(string) > 0)

        context_range = '5'  # range of characters where before/after is valid

        # for testing: re.search(".*" + before + r"\D{0,6}(\d{1,6}[,.]\d{2})\D{0,6}" + after + ".*", string).groups()
        components = re.search(".*" + before + r"\D{0," + context_range + "}((\d{1,6})[,.](\d{2}))\D{0," + context_range + "}" + after + ".*", string)

        if components:
            floatstring = components.group(2) + ',' + components.group(3)
            # logging.debug("get_euro_charge_from_context extracted float: [%s]" % floatstring)
            return floatstring
        else:
            logging.warning("Sorry, I was not able to extract a charge for this file, please fix manually")
            logging.debug("get_euro_charge_from_context was not able to extract a float: between [%s] and [%s] within [%s]" % (before, after, string[:30] + "..."))
            return False

    def rename_file(self, dirname, oldbasename, newbasename, dryrun=False, quiet=False):
        """
        Renames a file from oldbasename to newbasename in dirname.

        Only simulates result if dryrun is True.

        @param dirname: string containing the directory of the file
        @param oldbasename: string containing the old file name (basename)
        @param newbasename: string containing the new file name (basename)
        @param dryrun: boolean which defines if files should be changed (False) or not (True)
        """

        if oldbasename == newbasename:
            logging.info("Old filename is same as new filename: skipping file")
            return False

        oldfile = os.path.join(dirname, oldbasename)
        newfile = os.path.join(dirname, newbasename)

        if not os.path.isfile(oldfile):
            logging.error("file to rename does not exist: [%s]" % oldfile)
            return False

        if os.path.isfile(newfile):
            logging.error("file can't be renamed since new file name already exists: [%s]" % newfile)
            return False

        if not quiet:
            print('       →  ' + colorama.Style.BRIGHT + colorama.Fore.GREEN + newbasename + colorama.Style.RESET_ALL)
        logging.debug(" renaming \"%s\"" % oldfile)
        logging.debug("      ⤷   \"%s\"" % newfile)
        if not dryrun:
            os.rename(oldfile, newfile)
        return True

    def build_string_via_indexgroups(self, regex_match, indexgroups):
        """This function takes a regex_match object and concatenates its
        groups. It does this by traversing the list of indexgroups. If
        the list item is an integer, the corresponding
        regex_match.group() is appended to the result string. If the
        list item is a string, the string is appended to the result
        string.

        When a list item is a list, its elements are appended as well as
        long as all list items exist.

        match-groups that are in the indexgroups but are None are ignored.

        @param regex_match: a regex match object from re.match(REGEX, STRING)
        @param indexgroups: list of strings and integers like [1, '-', 2, '-', 3, 'T', 4, '.', 5, ' foo .png']
        @param return: string containing the concatenated string

        """

        if not regex_match:
            logging.error('no re.match object found; please check before calling build_string_via_indexgroups()')
            return "ERROR"

        def append_element(string, indexgroups):
            result = string
            for element in indexgroups:
                if type(element) == str:
                    result += element
                    # print 'DEBUG: result after element [' + str(element)  + '] =  [' + str(result) + ']'
                elif type(element) == int:
                    potential_element = regex_match.group(element)
                    # ignore None matches
                    if potential_element:
                        result += regex_match.group(element)
                        # print 'DEBUG: result after element [' + str(element)  + '] =  [' + str(result) + ']'
                    else:
                        # print 'DEBUG: match-group element ' + str(element) + ' is None'
                        pass
                elif type(element) == list:
                    # recursive: if a list element is a list, process if all elements exists:
                    # print 'DEBUG: found list item = ' + str(element)
                    # print 'DEBUG:   result before = [' + str(result) + ']'
                    all_found = True
                    for listelement in element:
                        if type(listelement) == int and (regex_match.group(listelement) is None or
                                                         len(regex_match.group(listelement)) < 1):
                            all_found = False
                    if all_found:
                        result = append_element(result, element)
                        # print 'DEBUG:   result after =  [' + str(result) + ']'
                    else:
                        pass
                        # print 'DEBUG:   result after =  [' + str(result) + ']' + \
                        #    '   -> not changed because one or more elements of sub-list were not found'
            return result

        logging.debug('build_string_via_indexgroups: FILENAME: ' + str(regex_match.group(0)))
        logging.debug('build_string_via_indexgroups: GROUPS: ' + str(regex_match.groups()))
        result = append_element('', indexgroups)
        logging.debug('build_string_via_indexgroups: RESULT:   ' + result)
        return result

    def NumToMonth(self, month):

        months = ['Dezember', 'Jaenner', 'Februar', 'Maerz', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
        return months[month]

    def translate_ORF_quality_string_to_tag(self, quality_string):
        """
        Returns a filetag which is derived from a key string. The key strings are defined
        by the file names of the ORF company offering its download file names.
        """

        if quality_string == 'Q4A' or quality_string == 'LOW':
            return 'lowquality'
        elif quality_string == 'Q6A' or quality_string == 'Q8C' or quality_string == 'HD':
            return 'highquality'
        else:
            return 'UNKNOWNQUALITY'

    def get_file_size(self, filename):
        """
        A simple wrapper to determine file sizes.

        For some hard-coded file names, a hard-coded file size is returned. This enables
        unit-testing for file sizes that do not exist in the file system.
        """

        # these are the hard-coded sizes for unit test cases:
        if filename in ['20180510T090000 ORF - ZIB - Signation -ORIGINAL- 2018-05-10_0900_tl_02_ZIB-9-00_Signation__13976423__o__1368225677__s14297692_2__WEB03HD_09000305P_09001400P_Q4A.mp4',
                        '20180510T090000 ORF - ZIB - Weitere Signale der Entspannung -ORIGINAL- 2018-05-10_0900_tl_02_ZIB-9-00_Weitere-Signale__13976423__o__5968792755__s14297694_4__WEB03HD_09011813P_09020710P_Q4A.mp4',
                        '20180520T201500 ORF - Tatort - Tatort_ Aus der Tiefe der Zeit -ORIGINAL- 2018-05-20_2015_in_02_Tatort--Aus-der_____13977411__o__1151703583__s14303062_Q8C.mp4',
                        '20180521T193000 ORF - ZIB 1 - Parlament bereitet sich auf EU-Vorsitz vor -ORIGINAL- 2018-05-21_1930_tl_02_ZIB-1_Parlament-berei__13977453__o__277886215b__s14303762_2__WEB03HD_19350304P_19371319P_Q4A.mp4',
                        '20180608T193000 ORF - Österreich Heute - Das Magazin - Österreich Heute - Das Magazin -ORIGINAL- 13979231_0007_Q8C.mp4',
                        '20190902T220000 ORF - ZIB 2 - Bericht über versteckte ÖVP-Wahlkampfkosten -ORIGINALlow- 2019-09-02_2200_tl_02_ZIB-2_Bericht-ueber-v__14024705__o__71528285d6__s14552793_3__ORF2HD_22033714P_22074303P_Q4A.mp4',
                        '20190902T220000 ORF - ZIB 2 - Hinweis _ Verabschiedung -ORIGINALlow- 2019-09-02_2200_tl_02_ZIB-2_Hinweis---Verab__14024705__o__857007705d__s14552799_9__ORF2HD_22285706P_22300818P_Q4A.mp4']:
            # don't care about file sizes, return a high number that is abote the expected minimum in any case:
            return 99999999
        elif filename == '20180608T170000 ORF - ZIB 17_00 - size okay -ORIGINAL- 2018-06-08_1700_tl__13979222__o__1892278656__s14313181_1__WEB03HD_17020613P_17024324P_Q4A.mp4':
            return 5017289  # from an actual downloaded file
        elif filename == '20180608T170000 ORF - ZIB 17_00 - size not okay -ORIGINAL- 2018-06-08_1700_tl__13979222__o__1892278656__s14313181_1__WEB03HD_17020613P_17024324P_Q4A.mp4':
            return 4217289  # manually reduced size from the value of an actual downloaded file
        elif filename == '20180608T170000 ORF - ZIB 17_00 - size okay -ORIGINAL- 2018-06-08_1700_tl__13979222__o__1892278656__s14313181_1__WEB03HD_17020613P_17024324P_Q8C.mp4':
            return 15847932  # from an actual downloaded file
        elif filename == '20180608T170000 ORF - ZIB 17_00 - size not okay -ORIGINAL- 2018-06-08_1700_tl__13979222__o__1892278656__s14313181_1__WEB03HD_17020613P_17024324P_Q8C.mp4':
            return 14050000  # manually reduced size from the value of an actual downloaded file
        elif filename == '20180610T000000 ORF - Kleinkunst - Kleinkunst_ Cordoba - Das Rückspiel (2_2) -ORIGINAL- 2018-06-10_0000_sd_06_Kleinkunst--Cor_____13979381__o__1483927235__s14313621_1__ORF3HD_23592020P_00593103P_Q8C.mp4':
            return 1506829698  # from actual file
        elif filename == '2018-06-14_2105_sd_02_Am-Schauplatz_-_Alles für die Katz-_____13979879__o__1907287074__s14316407_7__WEB03HD_21050604P_21533212P_Q8C.mp4':
            return 1214980782  # from actual file
        elif filename == '2018-06-14_2155_sd_06_Kottan-ermittelt - Wien Mitte_____13979903__o__1460660672__s14316392_2__ORF3HD_21570716P_23260915P_Q8C.mp4':
            return 2231522252  # from actual file
        elif filename == '2018-06-14_2330_sd_06_Sommerkabarett - Lukas Resetarits: Schmäh (1 von 2)_____13979992__o__1310584704__s14316464_4__ORF3HD_23301620P_00302415P_Q8C.mp4':
            return 1506983474  # from actual file

        try:
            return os.stat(filename).st_size
        except OSError:
            error_exit(10, 'get_file_size(): Could not get file size of: ' + filename)

    def warn_if_ORF_file_seems_to_small_according_to_duration_and_quality_indicator(self, oldfilename, qualityindicator,
                                                                                    start_hrs, start_min, start_sec,
                                                                                    end_hrs, end_min, end_sec):
        """
        Launches a warning if the expected size differs from the actual file size.

        Expected size is derived from the detailed time-stamp information
        and tests with a ten minute file:

        | Quality Indicator       | file size | bytes per second |
        |-------------------------+-----------+------------------|
        | Q8C = HD                | 240429907 |           400717 |
        | Q6A = high quality      | 150198346 |           250331 |
        | Q4A = low quality       |  74992178 |           124987 |
        """

        #FIXXME: 2019-08-26: disabled: correct from exception to warning #
        #FIXXME: 2019-09-03: assigned tests also disabled because this function never raises the expected exception
        return

        TOLERANCE_FACTOR = 0.95  # To cover edge cases where a reduced file size is feasible

        file_size = self.get_file_size(oldfilename)

        day_of_end = 1
        if int(end_hrs) < int(start_hrs):
            logging.debug('end hours is less than begin hours, adding a day-change for calculating duration')
            day_of_end = 2

        end = datetime.datetime(1980, 5, day_of_end, int(end_hrs), int(end_min), int(end_sec))
        start = datetime.datetime(1980, 5, 1, int(start_hrs), int(start_min), int(start_sec))
        duration = end - start
        duration_in_seconds = duration.seconds
        assert(duration_in_seconds > 0)

        if qualityindicator == 'Q8C':
            minimum_expected_file_size = 400000 * duration_in_seconds * TOLERANCE_FACTOR
        elif qualityindicator == 'Q6A':
            minimum_expected_file_size = 250000 * duration_in_seconds * TOLERANCE_FACTOR
        elif qualityindicator == 'Q4A':
            minimum_expected_file_size = 125000 * duration_in_seconds * TOLERANCE_FACTOR
        else:
            logging.warn('Unknown quality indicator prevents file size check: ' + qualityindicator)
            return

        ## additional check for minimum duration because small videos often produced wrong error messages:
        if duration_in_seconds > 120 and file_size < minimum_expected_file_size:
            print('\n       →  ' + colorama.Style.BRIGHT + colorama.Fore.RED +
                  'ERROR: file size seems to be too small for the given duration ' +
                  'and quality indicator found (download aborted?): \n' +
                  ' ' * 10 + 'file size:             ' + "{:,}".format(file_size) + ' Bytes\n' +
                  ' ' * 10 + 'expected minimum size: ' + "{:,}".format(minimum_expected_file_size) + ' Bytes\n' +
                  ' ' * 10 + 'duration:  ' + str('%.1f' % (duration_in_seconds/60)) + ' minutes\n' +
                  ' ' * 10 + 'quality:   ' + qualityindicator + '\n' +
                  ' ' * 10 + 'file name: ' + oldfilename + colorama.Style.RESET_ALL + '\n')
            raise(FileSizePlausibilityException('file size is not plausible (too small)'))
        else:
            logging.debug('warn_if_ORF_file_seems_to_small_according_to_duration_and_quality_indicator: ' +
                          'file size (' + "{:,}".format(file_size) +
                          ') is plausible compared to expected minimum (' +
                          "{:,}".format(minimum_expected_file_size) +
                          ')')


def move_to_success_dir(dirname, newfilename):
    """
    Moves a file to SUCCESS_DIR
    """
    if os.path.isdir(SUCCESS_DIR):
        logging.debug('using hidden feature: if a folder named \"' + SUCCESS_DIR +
                      '\" exists, move renamed files into it')
        os.rename(os.path.join(dirname, newfilename), os.path.join(dirname, SUCCESS_DIR,
                                                                   newfilename))
        logging.info('moved file to sub-directory "' + SUCCESS_DIR + '"')


def move_to_error_dir(dirname, basename):
    """
    Moves a file to SUCCESS_DIR
    """
    if os.path.isdir(ERROR_DIR):
        logging.debug('using hidden feature: if a folder named \"' + ERROR_DIR +
                      '\" exists, move failed files into it')
        os.rename(os.path.join(dirname, basename),
                  os.path.join(dirname, ERROR_DIR, basename))
        logging.info('moved file to sub-directory "' + ERROR_DIR + '"')


def main():
    """Main function"""

    if options.version:
        print(os.path.basename(sys.argv[0]) + " version " + PROG_VERSION_DATE)
        sys.exit(0)

    handle_logging()
    colorama.init()  # use Colorama to make Termcolor work on Windows too

    if options.verbose and options.quiet:
        error_exit(1, "Options \"--verbose\" and \"--quiet\" found. " +
                   "This does not make any sense, you silly fool :-)")

    if options.dryrun:
        logging.debug("DRYRUN active, not changing any files")
    logging.debug("extracting list of files ...")

    files = args

    logging.debug("%s filenames found: [%s]" % (str(len(files)), '], ['.join(files)))

    CONFIGDIR = os.path.join(os.path.expanduser("~"), ".config/guessfilename")
    sys.path.insert(0, CONFIGDIR)  # add CONFIGDIR to Python path in order to find config file
    try:
        import guessfilenameconfig
    except ImportError:
        logging.warning("Could not find \"guessfilenameconfig.py\" in directory \"" + CONFIGDIR +
                        "\".\nPlease take a look at \"guessfilenameconfig-TEMPLATE.py\", " +
                        "copy it, and configure accordingly.\nAs long as there is no file " +
                        "found, you can not use containing private settings")
        guessfilenameconfig = False

    guess_filename = GuessFilename(guessfilenameconfig, logging.getLogger())

    if len(args) < 1:
        error_exit(5, "Please add at least one file name as argument")

    filenames_could_not_be_found = 0
    logging.debug("iterating over files ...\n" + "=" * 80)
    for filename in files:
        if filename.__class__ == str:
            filename = str(filename)
        try:
            if not guess_filename.handle_file(filename, options.dryrun):
                filenames_could_not_be_found += 1
        except FileSizePlausibilityException:
            error_exit(99, 'An exception occurred. Aborting further file processing.')

    if not options.quiet:
        # add empty line for better screen output readability
        print()

    if filenames_could_not_be_found == 0:
        logging.debug('successfully finished.')
    else:
        logging.debug("finished with %i filename(s) that could not be derived" % filenames_could_not_be_found)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

# END OF FILE #################################################################

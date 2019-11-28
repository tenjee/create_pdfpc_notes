#!/usr/bin/env python

'''
Script to parse through a latex beamer presentation file and extract the \note{} content into a file for use as notes when presenting
'''

import re
import os
import os.path
import sys

frame_sequence = re.compile(r"\\begin\{frame\}.*?\\end\{frame\}", re.MULTILINE | re.DOTALL | re.IGNORECASE)
note_sequence = re.compile(r"\\note(?:<.*?>)?\{(?P<note>.*?)\}", re.MULTILINE | re.DOTALL | re.IGNORECASE)




def _parse_buffer(buff):
    '''
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex
    '''
    pass

def main(args):

    out_buffer = ''
    out_buffer += '[font_size]\n18\n[notes]\n'

    fname, fextension = os.path.splitext(args.infile)
    if not '.tex' in fextension:
        print("\n\ninput file must be a .tex file")
        sys.exit(2)
    else:
        outfile = "{}.pdfpc".format(fname)

    if not os.path.isfile(args.infile):
        print("\n\ninvalid input file specification")
        sys.exit(1)

    frame_number = 0
    with open(args.infile) as f:
        file_contents = f.read()

        slide_number = 0
        for m in re.finditer(frame_sequence,file_contents):
            notes_in_page = False
            slide_number += 1
            frame_number += 1
            for n in re.finditer(note_sequence, m.group(0)):
                if not notes_in_page:
                    out_buffer += "### {}".format(slide_number)
                else:
                    out_buffer += "\n===============\n"
                notes_in_page = True
                out_buffer += "{}".format(n.group('note'))
#            if not notes_in_page:
#                slide_number += 1
#    print(out_buffer)

    with open(outfile,'w') as outf:
        outf.write(out_buffer)






if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--infile", action="store", required=True,
                        dest="infile", help="The beamer tex file to read")
    args = parser.parse_args()

    main(args)


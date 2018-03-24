#
import CalimaStarUtils
import sys
import gzip

if __name__ == "__main__":
    # raw_text = gzip.open(sys.argv[1],'r').readlines()
    # cleaned_txt = open(sys.argv[1]+'.cln','w')
    # for line in raw_text:
    #     # print(line)
    #     line = line.decode(encoding='UTF-8')
    #     cleaned_txt.write(CalimaStarUtils.clean_line(line))
    # cleaned_txt.close()
    # print('Cleaning lines finished ...')
    # CalimaStarUtils.clean_utf8('clean-utf8-map', sys.argv[1]+'.cln', sys.argv[1]+'.clnUTF8')
    # print('CleanUTF8 finished ...')
    # CalimaStarUtils.encode_file('utf8','bw',sys.argv[1]+'.clnUTF8')
    # print('Encoding finished ...')


    raw_text = open(sys.argv[1],'r').readlines()
    cleaned_txt = open(sys.argv[1]+'.cln','w')
    for line in raw_text:
        # print(line)
        # line = line.decode(encoding='UTF-8')
        cleaned_txt.write(CalimaStarUtils.clean_line(line))
    cleaned_txt.close()
    CalimaStarUtils.encode_file('utf8', 'bw', sys.argv[1]+'.cln')

import sys

def encode(input_enc, output_enc, word):
    encoding_values = ['utf8', 'bw', 'sbw']
    mode = input_enc + '_' + output_enc

    utf8 = u'\u0621\u0622\u0623\u0624\u0625\u0626\u0627\u0628\u0629\u062A\u062B\u062C\u062D\u062E\u062F\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063A\u0640\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u0649\u064A\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0670\u0671'
    bw = "'|>&<}AbptvjHxd*rzs$SDTZEg_fqklmnhwYyFNKaui~o`{"
    sbw = "CMOWIQAbptvjHxdVrzscSDTZEg_fqklmnhwYyFNKauiXoeL"


    if mode == 'utf8_bw':
        utf8_bw = str.maketrans(utf8, bw)
        return word.translate(utf8_bw)
    elif mode == 'utf8_sbw':
        utf8_sbw = str.maketrans(utf8, sbw)
        return word.translate(utf8_sbw)
    
    elif mode == 'bw_utf8':
        bw_utf8 = str.maketrans(bw, utf8)
        return word.translate(bw_utf8)
    elif mode == 'bw_sbw':
        bw_sbw = str.maketrans(bw, sbw)
        return word.translate(bw_sbw)
    
    elif mode == 'sbw_utf8':
        sbw_utf8 = str.maketrans(sbw, utf8)
        return word.translate(sbw_utf8)
    elif mode == 'sbw_bw':
        sbw_bw = str.maketrans(sbw, bw)
        return word.translate(sbw_bw)
    
    else:
        if input_enc not in encoding_values:
            print('Input encoding ' + input_enc + ' is not valid.')
        if output_enc not in encoding_values:
            print('Output encoding ' + output_enc + ' is not valid.')
        sys.exit(2)


def encode_file(input_enc, output_enc, input_file):
    try:
        text_file = open(input_file, 'r').read()
        out_text = open(input_file + '.' + output_enc, 'w')
        out_text.write(encode(input_enc, output_enc, text_file))
        out_text.close()
    except IOError as err:
        print("File cannot be opened!")
        sys.exit(2)


if __name__ == "__main__":
    encode_file('utf8', 'bw', 'example.txt')
    
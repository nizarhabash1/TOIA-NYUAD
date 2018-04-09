# -*- coding: utf-8 -*-
import sys
import re

# diacritics = FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN, TATWEEL, DAGGER ALIF
diac_utf8 = re.compile("[\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0640\u0670]")
diac_bw = re.compile("[aiuo~`FKN_]")
diac_sbw = re.compile("[aiuoXeFKN_]")
diac_hsb = re.compile("[aiu.~áãũĩ_]")


def encode(input_enc, output_enc, word):

    if input_enc == output_enc:
        return word

    encoding_values = ['utf8', 'bw', 'sbw', 'hsb']
    mode = input_enc + '_' + output_enc

    utf8 = u'\u0621\u0622\u0623\u0624\u0625\u0626\u0627\u0628\u0629\u062A\u062B\u062C\u062D\u062E\u062F\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063A\u0640\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u0649\u064A\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0670\u0671'
    bw = "'|>&<}AbptvjHxd*rzs$SDTZEg_fqklmnhwYyFNKaui~o`{"
    sbw = "CMOWIQAbptvjHxdVrzscSDTZEg_fqklmnhwYyFNKauiXoeL"
    hsb = "'ĀÂŵӐŷAbħtθjHxdðrzsšSDTĎςɣ_fqklmnhwýyãũĩaui~.áÄ"
    arabtex = ["'", "'A", "'", "U'", "'i", "'i", 'A', 'b', 'T', 't', '_t', 'j', '.h', 'x', 'd', '_d', 'r',
               'z', 's', '^s', '.s', '.d', '.t', '.z', '`', '.g', '--', 'f', 'q', 'k', 'l', 'm', 'n', 'h', 'w',
               'Y', 'y', 'aN', 'uN', 'iN', 'a', 'u', 'i', 'xx', '"', '_a', '"']

    if mode == 'utf8_bw':
        utf8_bw = str.maketrans(utf8, bw)
        return word.translate(utf8_bw)
    elif mode == 'utf8_sbw':
        utf8_sbw = str.maketrans(utf8, sbw)
        return word.translate(utf8_sbw)
    elif mode == 'utf8_hsb':
        utf8_hsb = str.maketrans(utf8, hsb)
        return word.translate(utf8_hsb)
    elif mode == 'bw_utf8':
        bw_utf8 = str.maketrans(bw, utf8)
        return word.translate(bw_utf8)
    elif mode == 'bw_sbw':
        bw_sbw = str.maketrans(bw, sbw)
        return word.translate(bw_sbw)
    elif mode == 'bw_hsb':
        bw_hsb = str.maketrans(bw, hsb)
        return word.translate(bw_hsb)
    elif mode == 'sbw_utf8':
        sbw_utf8 = str.maketrans(sbw, utf8)
        return word.translate(sbw_utf8)
    elif mode == 'sbw_bw':
        sbw_bw = str.maketrans(sbw, bw)
        return word.translate(sbw_bw)
    elif mode == 'sbw_hsb':
        sbw_hsb = str.maketrans(sbw, hsb)
        return word.translate(sbw_hsb)
    elif mode == 'hsb_utf8':
        hsb_utf8 = str.maketrans(hsb, utf8)
        return word.translate(hsb_utf8)
    elif mode == 'hsb_bw':
        hsb_bw = str.maketrans(hsb, bw)
        return word.translate(hsb_bw)
    elif mode == 'hsb_sbw':
        hsb_sbw = str.maketrans(hsb, sbw)
        return word.translate(hsb_sbw)

    elif mode == 'utf8_arabtex':
        utf8_list = list(utf8)
        char_list = list(word)
        output = ''
        for char in char_list:
            if char in utf8_list:
                if arabtex[utf8_list.index(char)] == 'xx':
                    output = output + output[-1]
                else:
                    output = output + arabtex[utf8_list.index(char)]
            else:
                output = output + char
        return output
    elif mode == 'bw_arabtex':
        bw_list = list(bw)
        char_list = list(word)
        output = ''
        for char in char_list:
            if char in bw_list:
                if arabtex[bw_list.index(char)] == 'xx':
                    output = output + output[-1]
                else:
                    output = output + arabtex[bw_list.index(char)]
            else:
                output = output + char
        return output
    elif mode == 'sbw_arabtex':
        sbw_list = list(sbw)
        char_list = list(word)
        output = ''
        for char in char_list:
            if char in sbw_list:
                if arabtex[sbw_list.index(char)] == 'xx':
                    output = output + output[-1]
                else:
                    output = output + arabtex[sbw_list.index(char)]
            else:
                output = output + char
        return output
    elif mode == 'hsb_arabtex':
        hsb_list = list(hsb)
        char_list = list(word)
        output = ''
        for char in char_list:
            if char in hsb_list:
                if arabtex[hsb_list.index(char)] == 'xx':
                    output = output + output[-1]
                else:
                    output = output + arabtex[hsb_list.index(char)]
            else:
                output = output + char
        return output
    else:
        if input_enc not in encoding_values:
            print('Input encoding ' + input_enc + ' is not valid.')
        if output_enc not in encoding_values and output_enc != 'arabtex':
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


# apply different rewrite rules on words including:
# the addition of $dp after sun letters
# removing of ftHp after Alf followed with the suffix tA or tA mrbwTp
# changing non-hamzated starting Alf to Alf hmzp wSl
# removing pluses
# adding ftHp before Alf and Alf mqSwrY
# modifying the orthography of tnwyn ftH before or after Alf
def rewrite_rules(word):
    word = re.sub(r'^((wa|fa)?(bi|ka)?Al)\+([tvd*rzs$SDTZln])', r'\1\4~', word)
    word = re.sub(r'^((wa|fa)?lil)\+([tvd*rzs$SDTZln])', r'\1\3~', word)
    word = re.sub(r'A\+a([pt])', r'A\1', word)
    word = re.sub(r'{', r'A', word)
    word = re.sub(r'\+', r'', word)

    return word


# return a string with all the features in feature_order list, ordered, and separated by spaces
def printer(analysis, output_encoding, feature_order, tokenization):
    output_string = ''

    if 'diac' in analysis:
        analysis['diac'] = encode('bw', output_encoding, analysis['diac'])
    if 'stem' in analysis:
        analysis['stem'] = encode('bw', output_encoding, analysis['stem'])
    if 'lex' in analysis:
        lemma_toks = re.split('([_-])', analysis['lex'])
        lemma_stripped = encode('bw', output_encoding, lemma_toks[0].rstrip())
        analysis['lex'] = lemma_stripped + ''.join(lemma_toks[1:])

    if 'bw' in analysis:
        bw_encoded = ''
        bw_toks = analysis['bw'].split('+')
        bw_tok = bw_toks[0]
        if not bw_tok:
            pass
        else:
            morpheme = encode('bw', output_encoding, bw_tok.split('/')[0])
            bw = bw_tok.split('/')[1]
            bw_encoded = morpheme + '/' + bw


        for bw_tok in bw_toks[1:]:
            if not bw_tok:
                pass
            else:
                morpheme = encode('bw', output_encoding, bw_tok.split('/')[0])
                bw = bw_tok.split('/')[1]

                bw_encoded = bw_encoded + '+' + morpheme + '/' + bw

        if len(bw_encoded.split("+")) < 3:
            bw_encoded = bw_encoded + "+"

        analysis['bw'] = bw_encoded

    for order in feature_order:
        if order in analysis:
            # todo: test with extended db
            if (order == 'seg' or order == 'tok') and order in tokenization:
                for type in tokenization[order]:
                    output_string = output_string + order + '_' + type + analysis[order + '_' + type] + ' '
            else:
                output_string = output_string + order + ":" + analysis[order] + " "

    return output_string.rstrip()


# return the word without the diacritics (aiuo~`FKN_)
def dediac(diac_word, encoding):
    if encoding == 'bw':
        return re.sub(diac_bw, r'', diac_word)
    elif encoding == 'utf8':
        return re.sub(diac_utf8, r'', diac_word)
    elif encoding == 'safebw':
        return re.sub(diac_sbw, r'', diac_word)
    elif encoding == 'hsb':
        return re.sub(diac_hsb, r'', diac_word)


def normalize(match_word, normalization):
    for char in normalization:
        orig = re.compile(re.escape(char))
        match_word = re.sub(orig, normalization[char], match_word)
    return match_word


def clean_line(input_text):
    processed_line = []
    processed_line.extend(list(filter(None, re.split(r"(\.|,|\'|`|\"|!|/|\\|\?|-|\(|\)|;|:|،|٫|؟|…|‘|’)", input_text))))
    return " ".join(processed_line)


def generate_lmm(lemma, encoding):
    lemma_toks = re.split('([_-])', lemma)
    lemma_stripped = dediac(lemma, encoding)
    lemma = lemma_stripped + ''.join(lemma_toks[1:])
    return lemma


def clean_utf8(map_file, input_file, output_file):
    try:
        map_reader = open(map_file, 'r')
    except IOError as err:
        print("MAP file is not found!")
        sys.exit(2)
    try:
        input_text = open(input_file, 'r').readlines()
        output = open(output_file, 'w')
    except IOError as err:
        print("Input file is not found!")
        sys.exit(2)

    # hash the map
    utf8_map = {}
    lines = map_reader.readlines()
    for line in lines:
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
        else:
            elements = re.split('\t+', line)
            char = elements[0]
            action = elements[1]
            # comment = elements[2]

            if re.search(r'^(u....)$',char) is not None:
                char = char + '-' + char
            if re.search(r'^u(....)-u(....)$', char) is not None:
                start = int(re.search(r'^u(....)-u(....)$', char).group(1), 16)
                end = int(re.search(r'^u(....)-u(....)$', char).group(2), 16)
                if end < start:
                    print("Error: Wrong range: " + char + " start = " + start + " end = " + end)
                    sys.exit(2)
                for i in range(start, end+1, 1):
                    if action == 'OK':
                        print(chr(i) + "\t" + chr(i))
                        utf8_map[chr(i)] = chr(i)
                    elif action == 'DEL':
                        print(chr(i) + "\t" + "DEL")
                        utf8_map[chr(i)] = ''
                    elif action == 'SPC':
                        print(chr(i) + "\t" + "SPC")
                        utf8_map[chr(i)] = ' '
                    elif action.startswith('u'):
                        value = ''
                        uni_chars = action.split('u')
                        for uni_char in uni_chars:
                            if uni_char:
                                value = value + chr(int(uni_char, 16))
                        print(chr(i) + "\t" + value)
                        utf8_map[chr(i)] = value
                    else:
                        print(chr(i) + "\t" + action)
                        utf8_map[chr(i)] = action
            else:
                if action == 'OK':
                    utf8_map[char] = char
                elif action == 'DEL':
                    utf8_map[char] = ''
                elif action == 'SPC':
                    utf8_map[char] = ' '
                elif action.startswith('u'):
                    value = ''
                    uni_chars = action.split('u')
                    for uni_char in uni_chars:
                        value = value + chr(int(uni_char, 16))
                    utf8_map[char] = value
                else:
                    utf8_map[char] = action

    # covfefe
    output_string = ''
    for line in input_text:
        new_line = ''
        for char in line:
            if not isinstance(char, str) and 'INVALID' in utf8_map:
                new_line = new_line + (utf8_map['INVALID'])
            else:
                if char in utf8_map:
                    new_line = new_line + (utf8_map[char])
                else:
                    if 'ELSE' in utf8_map:
                        new_line = new_line + (utf8_map['ELSE'])
        output_string = output_string + new_line.strip() + "\n"

    output_string = re.sub(r' +', r' ', output_string)
    output_string = output_string.rstrip()
    output.write(output_string)

    output.close()


if __name__ == "__main__":
    # encode_file('utf8', 'hsb', 'example.txt')

    # print(encode('utf8', 'bw', 'يُنْفِقُ الْخَلِيجِيُّونَ أَمْوَالًا طَائِلَةً عَلَى الْعُطُورِ، وَخَاصَّةً الشَّرْقِيَّةَ مِنْهَا الَّتِي تُعَدُّ أَغْلَى عُطُورِ الْعَالَمِ. '))
    # print(encode('utf8', 'arabtex', 'يُنْفِقُ الْخَلِيجِيُّونَ أَمْوَالًا طَائِلَةً عَلَى الْعُطُورِ، وَخَاصَّةً الشَّرْقِيَّةَ مِنْهَا الَّتِي تُعَدُّ أَغْلَى عُطُورِ الْعَالَمِ. '))

    # print(dediac('يُنْفِقُ الْخَلِيجِيُّونَ أَمْوَالًا طَائِلَةً عَلَى الْعُطُورِ، وَخَاصَّةً الشَّرْقِيَّةَ مِنْهَا الَّتِي تُعَدُّ أَغْلَى عُطُورِ الْعَالَمِ. ', 'utf8'))
    clean_utf8('clean-utf8-map', 'cleanUtf8.test.txt', 'cleanUtf8.test.txt.cln')

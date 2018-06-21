import sys
import pickle
import re
import xml.etree.ElementTree as ET
import io
import os
import CalimaStarUtils
import inspect
from collections import deque

# the hash of the define values from the db file - used to store valid values for each feature
define_hash = {}
# the hash of the default values from the db file - used to store the default values for every feature for every pos
default_hash = {}
# the hash of the bakcoff values from the db file - used to store the stemcats that will be considered for every backoff
# option
backoff_hash = {}

# the hash of the prefixes from the db file - used to store the lookup value of the prefix and a list of all its
# possible features
prefix_hash = {}
# the hash of the suffixes from the db file - used to store the lookup value of the suffix and a list of all its
# possible features
suffix_hash = {}
# the hash of the stems from the db file - used to store the lookup value of the stem and a list of all its
# possible features
stem_hash = {}

# the hash of the stems from the db file - used to store the lemma value and a list of all its possible features
lemma_hash = {}
# the hash of the prefixes form the db file - used to store the prefix cat value and a list of all its possible features
prefix_cat_hash = {}
# the hash of the suffixes form the db file - used to store the suffix cat value and a list of all its possible features
suffix_cat_hash = {}

# the hash of the stem-prefix compatibility - indexed by stem
stem_prefix_compatibility_hash = {}
# the hash of the stem-suffix compatibility - indexed by stem
stem_suffix_compatibility_hash = {}

# the hash of the prefix-stem compatibility (AB Table) - indexed by prefix-stem - value is always None
prefix_stem_compatibility = {}
# the hash of the stem-suffix compatibility (BC Table) - indexed by stem-suffix - value is always None
stem_suffix_compatibility = {}
# the hash of the prefix-suffix compatibility (AC Table) - indexed by prefix-suffix - value is always None
prefix_suffix_compatibility = {}

# the list of features that will not be taken into consideration when generating words in the generate and reinflect
# functions
features_not_for_generation = ['diac', 'lex', 'bw', 'gloss', 'source', 'stem', 'stemcat', 'lmm', 'dediac', 'caphi', 'catib6', 'ud', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok', 'd2tok', 'atbtok', 'd3tok', 'root', 'pattern', 'freq', 'POS_prob']
# the list of features that will not be taken into consideration when generating words in the reinflect function when a
# proclitic or enclitic is given
special_case_features_not_for_generation = ["stt", "cas", "mod"]

# the length of the longest prefix
MAXPRELEN = 0
# the length of the longest suffix
MAXSUFLEN = 0

# memoization hash for analysis
analysis_memo_hash = {}
# memoization hash for generation
generation_memo_hash = {}
# memoization hash for reinflection
reinflection_memo_hash = {}

# features which should be concatinated when generating analysis
concatinating_features = ['diac', 'bw', 'gloss', 'pattern', 'caphi', 'catib6', 'ud', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok', 'd2tok', 'atbtok', 'd3tok']
# features which will be overwritten in suffix > prefix > stem order when generating analyses
overwritten_features = ['lex', 'pos', 'prc3', 'prc2', 'prc1', 'prc0', 'per', 'asp', 'vox', 'mod', 'gen', 'num', 'stt',
                        'cas', 'enc0', 'rat', 'form_gen', 'form_num']
# features which will be automatically generated after the analysis is generating analysis
generated_features = ['stem', 'stemcat', 'lmm', 'dediac', 'source', 'root', 'freq']

# the possible tags to be used in the configuration file
configuration_tag_values = ['encoding', 'extended_alpha', 'clean_up_doc', 'feature_order', 'output_match',
                            'normalization', 'analysis_order', 'tokenization', 'spelling_variants', 'memoization',
                            'backoff']
# the possible values for encoding
encoding_values = ['bw', 'safebw', 'utf8', 'hsb', 'arabtex']
# the possible values for features
feature_values = ['diac', 'lex', 'root', 'bw', 'pattern', 'pos', 'gloss', 'prc3', 'prc2', 'prc1', 'prc0', 'per', 'asp',
                  'vox', 'mod', 'gen', 'num', 'stt', 'cas', 'enc0', 'rat', 'source', 'stem', 'stemcat', 'lmm',
                  'dediac', 'caphi', 'freq','POS_prob', 'form_gen', 'form_num', 'catib6', 'ud', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok', 'd2tok', 'atbtok', 'd3tok']
# the possible values for matching options
output_match_values = ['diac_match', 'orthographic_match']
# the possible values for diac_match
diac_match_values = ['full', 'partial', 'none']
# the possible values for orthographic_match
orthographic_match_values = ['full', 'normalized', 'none']
# xml special chars mappings
xml_special_char_values = {'&lt;': '<', '&#60;': '<', '&gt;': '>', '&#62;': '>', '&#38;': '&', '&#39;': "'",
                           '&#34;': '"'}
# the possible values for analysis_order
analysis_order_values = ['random', 'alphabetical', 'diac', 'frequency']
# the possible values for tokenization choices
tok_type_values = ['seg', 'tok']
# the possible values for tokenization schemes
tok_scheme_values = ['ST', 'ON', 'D1', 'D2', 'D3', 'WA', 'TB', 'S1', 'S2', 'MR', 'LEM', 'ENX']
# the possible values for tnwyn_ftH
tnwyn_ftH_values = ['FA', 'AF']

# the expected encoding of the input, default is bw
input_encoding = 'bw'
# the expected encoding of the output, default is bw
output_encoding = 'bw'
# boolean for including extended alphabet values (J, V, P, G), default is False
extended_alpha = False
# boolean for cleaning the document (ST tokenization)
clean_up_doc = False
# the features and order in which they will be printed in the output file
feature_order = ['diac', 'lex', 'root', 'bw', 'pattern', 'pos', 'gloss', 'prc3', 'prc2', 'prc1', 'prc0', 'per', 'asp',
                 'vox', 'mod', 'gen', 'num', 'form_gen', 'form_num', 'stt', 'cas', 'enc0', 'rat', 'source', 'stem', 'stemcat', 'lmm',
                 'dediac', 'caphi', 'freq', 'catib6', 'ud', 'd3seg', 'atbseg', 'd2seg', 'd1seg', 'd1tok', 'd2tok', 'atbtok', 'd3tok']
# the extent of diac_match for generating and sorting output
diac_match = 'none'
# the extent of ortho_match for generating and sorting output
orthographic_match = 'none'
# the hash of the characters that need to be normalized
normalization = {}
normalization_re = {}
# the order in which the analyses will be sorted for display purposes
analysis_order = 'random'
# the hash in which the tokenization options and schemes will be saved - key: tokenization option, value: list of
# tokenization schemes
tokenization = {}
# the way tnwyn ftH will be displayed
tnwyn_ftH = 'AF'
# boolean for enforcing a ftHp before every Alf and Alf mqSwrY
ftHp_Alf = False
# boolean for enabling memoization
memoization = True

# characters that are not part of the bw scheme
non_bw = "BCceGIJLMOPQRUVWX"
# charachters that are not part of the safe bw scheme
non_extended_bw = "BCceILMOQRUWX"

# alphabaetical order
# bw
bw_alpha_order = " '|>&<}AbptvjHxd*rzs$SDTZEg_fqklmnhwYyFNKaui~o`{"
# safe bw
sbw_alpha_order = " CMOWIQAbptvjHxdVrzscSDTZEg_fqklmnhwYyFNKauiXoeL"
# hsb
hsb_alpha_order = " 'ĀÂŵӐŷAbħtθjHxdðrzsšSDTĎςɣ_fqklmnhwýyãũĩaui~.áÄ"
# arabtex
arabtex_alpha_order = [" ", "'", "'A", "'", "U'", "'i", "'i", 'A', 'b', 'T', 't', '_t', 'j', '.h', 'x', 'd', '_d', 'r',
                       'z', 's', '^s', '.s', '.d', '.t', '.z', '`', '.g', '--', 'f', 'q', 'k', 'l', 'm', 'n', 'h', 'w',
                       'Y', 'y', 'aN', 'uN', 'iN', 'a', 'u', 'i', 'xx', '"', '_a', '"']
# utf8 alphabetical order is not provided because they are ordered sequentially. The order of the alphabet in the
# previous lists follows that of the ordering of the Arabic alphabet in utf8 encoding

# Backoff mode values and variable
backoff_values = ['NONE', 'NOAN_ALL', 'ADD_ALL', 'NOAN_PROP', 'ADD_PROP']
backoff = 'NONE'

verbose = False

verboseprint = print if verbose else lambda *a, **k:None

# A hash for the BW POS probability unigram model 
POS_prob_hash = {}

diac_pattern = re.compile("^(\s|[aiuo~`FKN])*$")  # to match words containing only diacs
digit_pattern = re.compile("\d+")
punct_pattern = re.compile("^\s*[\-=\"_:#@!?^/()\[\]%;\\\+.,]+\s*$")

analyze_with_backoff_re = re.compile(r'NOAN')

FA_re = re.compile("FA")
FY_re = re.compile("FY")
AF_re = re.compile("AF")
YF_re = re.compile("YF")

split_lemma = re.compile('([_-])')

# read the config file, and save the variables as needed
def read_config(config_file):
    '''
    The function parses a configuration file in xml format, and assigns the values to the appropriate variables
    :param config_file: the path to the configuration file
    :return: nothing
    '''
    global input_encoding
    global output_encoding
    global extended_alpha
    global clean_up_doc
    global feature_order
    global diac_match
    global orthographic_match
    global normalization
    global normalization_re
    global analysis_order
    global tokenization
    global tnwyn_ftH
    global ftHp_Alf
    global memoization
    global backoff
    global POS_prob_hash

    tree = ET.parse(os.path.abspath(config_file))
    root = tree.getroot()
    for child in root:
        tag = child.tag
        attrib = child.attrib

        if tag not in configuration_tag_values:
            print('Config file error. Tag ' + tag + ' is not recognized!')
            sys.exit(2)

        if tag == 'encoding':
            source = attrib['source'].lower()
            value = attrib['value'].lower()
            if value not in encoding_values:
                print("WARNING: 'encoding' value is invalid. Default encoding 'bw' will be assumed.")
            else:
                if source == 'input':
                    input_encoding = value
                elif source == 'output':
                    output_encoding = value
                else:
                    print("Encoding 'source' is invalid!")
                    sys.exit(2)
        elif tag == 'extended_alpha':
            value = attrib['value'].lower()
            if value == 'true':
                extended_alpha = True
            elif value == 'false':
                extended_alpha = False
            else:
                print("WARNING: 'extended_alpha' value can be 'True' or 'False' only."
                      " Default value 'False' will be assumed.")
        elif tag == 'clean_up_doc':
            value = attrib['value'].lower()
            if value == 'true':
                clean_up_doc = True
            elif value == 'false':
                clean_up_doc = False
            else:
                print("WARNING: 'clean_up_doc' value can be 'True' or 'False' only."
                      " Default value 'False' will be assumed.")
        elif tag == 'feature_order':
            feat_order = {}
            for grand_child in child:
                order = grand_child.attrib['order']
                try:
                    int(order)
                except ValueError as err:
                    print("'feature' order is not an integer. Feature will be ignored")
                    continue
                value = grand_child.attrib['value']
                if value not in feature_values:
                    print("'feature' value is not valid. Feature will be ignored")
                    continue
                feat_order[int(order)] = value
            orders = sorted(feat_order.keys())
            feature_order = []
            for order in orders:
                feature_order.append(feat_order[order])
            if 'POS_prob' in feature_order:
                POS_text = open('clitic_only_bw_POS.lm', 'r').readlines()
                POS_prob_hash = {}
                for POS_line in POS_text:
                    POS = POS_line.rstrip().split('\t')[1]
                    freq = POS_line.rstrip().split('\t')[0]
                    POS_prob_hash[POS] = freq
            print()
        elif tag == 'output_match':
            for grand_child in child:
                type = grand_child.attrib['type']
                if type in output_match_values:
                    if type == 'diac_match':
                        value = grand_child.attrib['value'].lower()
                        if value not in diac_match_values:
                            print("WARNING: 'diac_match' value is invalid. Default value 'no_match' will be assumed.")
                        else:
                            diac_match = value
                    elif type == 'orthographic_match':
                        value = grand_child.attrib['value'].lower()
                        if value not in orthographic_match_values:
                            print("WARNING: 'orthographic_match' value is invalid. Default value 'no_match' will be "
                                  "assumed.")
                        else:
                            orthographic_match = value
        elif tag == 'normalization':
            normalization = {}
            for grand_child in child:
                original = grand_child.attrib['original']
                normalized = grand_child.attrib['normalized']
                if original in xml_special_char_values:
                    original = xml_special_char_values[original]
                normalization[original] = normalized
            normalization_re = CalimaStarUtils.gen_normalize_re(normalization)
        elif tag == 'analysis_order':
            value = attrib['value'].lower()
            if value not in analysis_order_values:
                print("WARNING: 'analysis_order' value is invalid. Default value 'random' will be assumed.")
            else:
                analysis_order = value
        elif tag == 'tokenization':
            tokenization = {}
            for grand_child in child:
                tok_type = grand_child.attrib['type'].lower()
                tok_scheme = grand_child.attrib['scheme'].upper()
                if tok_type in tok_type_values and tok_scheme in tok_scheme_values:
                    if tok_type in tokenization and tok_scheme not in tokenization[tok_type]:
                        tokenization[tok_type].append(tok_scheme)
                    else:
                        tokenization[tok_type] = []
                        tokenization[tok_type].append(tok_scheme)
        elif tag == 'spelling_variants':
            for grand_child in child:
                type = grand_child.attrib['type']
                value = grand_child.attrib['value']
                if type == 'tnwyn_ftH':
                    if value in tnwyn_ftH_values:
                        tnwyn_ftH = value
                    else:
                        print("WARNING: 'tnwyn_ftH' value is invalid. Default value 'AF' will be assumed.")
                elif type == 'ftHp_Alf':
                    if value.lower() == 'true':
                        ftHp_Alf = True
                    elif value.lower() == 'false':
                        ftHp_Alf = False
                    else:
                        print("WARNING: 'ftHp_Alf' value can be 'True' or 'False' only. Default value 'False'"
                              " will be assumed.")
        elif tag == 'memoization':
            value = attrib['value']
            if value.lower() == 'true':
                memoization = True
            elif value.lower() == 'false':
                memoization = False
            else:
                print("WARNING: 'memoization' value can be 'True' or 'False' only. Default value 'True'"
                      " will be assumed.")
        elif tag == 'backoff':
            value = attrib['value'].upper()
            if value in backoff_values:
                backoff = value
            else:
                print("WARNING: 'backoff' value is invalid. Default value 'NONE' will be assumed.")
    # print(feat_order)

# initialize from a db file
# no need to previously install db prior to this initialize
def initialize_from_file(database, mode):
    global define_hash
    global default_hash
    global backoff_hash

    global prefix_hash
    global suffix_hash
    global stem_hash

    global lemma_hash
    global prefix_cat_hash
    global suffix_cat_hash

    global stem_prefix_compatibility_hash
    global stem_suffix_compatibility_hash

    global prefix_stem_compatibility
    global stem_suffix_compatibility
    global prefix_suffix_compatibility

    global MAXSUFLEN
    global MAXPRELEN

    try:
        db_file = open(database, 'r')
    except IOError as error:
        print(error)
        print("database cannot be opened\n")
        sys.exit(2)

    line = db_file.readline()
    while "DEFAULT" not in line:
        if line.startswith("#"):
            line = db_file.readline().strip()

        elements = line.split(" ")
        key = elements[1]
        define_hash[key] = []
        for value in elements[2:]:
            feature_value = value.split(":")[1]
            define_hash[key].append(feature_value)
        line = db_file.readline().strip()

    while "ORDER" not in line:
        if line.startswith("#"):
            line = db_file.readline().strip()

        elements = line.split(" ")
        key = elements[1].split(":")[1]
        default_hash[key] = {}
        for element in elements[2:]:
            element_key = element.split(":")[0]
            element_value = element.split(":")[1]
            default_hash[key][element_key] = element_value
        line = db_file.readline().strip()

    while "STEMBACKOFF" not in line:
        line = db_file.readline()

    while "PREFIX" not in line:
        if line.startswith("#"):
            line = db_file.readline().strip()

        elements = line.split(" ")
        key = elements[1]
        backoff_hash[key] = []
        for element in elements[2:]:
            backoff_hash[key].append(element)
        line = db_file.readline().strip()


    while "SUFFIX" not in line:
        if line.startswith("#"):
            line = db_file.readline()

        elements = line.split("\t")

        if mode == 'analyze' or mode == 'reinflect':
            key = elements[0]

            if len(elements) == 2:
                temp_list = (elements[1], {})
                if key in prefix_hash:
                    prefix_hash[key].append(temp_list)
                else:
                    prefix_hash[key] = [temp_list]
            else:
                temp_list = (elements[1], __get_features_hash(elements[2]))
                if key in prefix_hash:
                    prefix_hash[key].append(temp_list)
                else:
                    prefix_hash[key] = [temp_list]

        # todo: rewrite the code to fix the structure of prefix_cat_hash
        if mode == 'generate' or mode == 'reinflect':
            key = elements[1]

            if len(elements) == 2:
                # if key in prefix_hash:
                #     temp_list = []
                #     temp_list.append(' ')
                #     prefix_cat_hash[key].append(temp_list)
                # else:
                #     prefix_cat_hash[key] = []
                #     temp_list = []
                #     temp_list.append(' ')
                #     prefix_cat_hash[key].append(temp_list)
                temp_list = ()
                if key in prefix_hash:
                    prefix_cat_hash[key].append(temp_list)
                else:
                    prefix_cat_hash[key] = [temp_list]
            else:
                # if key in prefix_cat_hash:
                #     for element in elements[2:]:
                #         if element not in prefix_cat_hash[key]:
                #             prefix_cat_hash[key].append(elements[2:])
                # else:
                #     prefix_cat_hash[key] = []
                #     prefix_cat_hash[key].append(elements[2:])
                temp_list = (__get_features_hash(elements[2]))
                if key in prefix_cat_hash:
                    for element in elements[2:]:
                        if element not in prefix_cat_hash[key]:
                            prefix_cat_hash[key].append(temp_list)
                else:
                    prefix_cat_hash[key] = [temp_list]
                    

        line = db_file.readline()

    while "STEM" not in line:
        if line.startswith("#"):
            line = db_file.readline()

        elements = line.split("\t")
        if mode == 'analyze' or mode == 'reinflect':
            key = elements[0]

            if len(elements) == 2:
                temp_list = (elements[1], {})
                if key in suffix_hash:
                    suffix_hash[key].append(temp_list)
                else:
                    suffix_hash[key] = [temp_list]
            else:
                temp_list = (elements[1], __get_features_hash(elements[2]))
                if key in suffix_hash:
                    suffix_hash[key].append(temp_list)
                else:
                    suffix_hash[key] = [temp_list]

        # todo: rewrite the code to fix the structure of suffix_cat_hash
        if mode == 'generate' or mode == 'reinflect':
            key = elements[1]

            if len(elements) == 2:
                # if key in suffix_cat_hash:
                #     temp_list = []
                #     temp_list.append(' ')
                #     suffix_cat_hash[key].append(temp_list)
                # else:
                #     suffix_cat_hash[key] = []
                #     temp_list = []
                #     temp_list.append(' ')
                #     suffix_cat_hash[key].append(temp_list)
                temp_list = ()
                if key in suffix_cat_hash:
                    suffix_cat_hash[key].append(temp_list)
                else:
                    suffix_cat_hash[key] = [temp_list]
            else:
                # if key in suffix_cat_hash:
                #     for element in elements[2:]:
                #         if element not in suffix_cat_hash[key]:
                #             suffix_cat_hash[key].append(elements[2:])
                # else:
                #     suffix_cat_hash[key] = []
                #     suffix_cat_hash[key].append(elements[2:])
                temp_list = (__get_features_hash(elements[2]))
                if key in suffix_cat_hash:
                    for element in elements[2:]:
                        if element not in suffix_cat_hash[key]:
                            suffix_cat_hash[key].append(temp_list)
                else:
                    suffix_cat_hash[key] = [temp_list]

        line = db_file.readline()

    while "TABLE AB" not in line:
        if line.startswith("#"):
            line = db_file.readline()
            pass
        elements = line.split("\t")

        if mode == 'analyze' or mode == 'reinflect':
            key = elements[0]
            temp_list = (elements[1], __get_features_hash(elements[2]))
            if key in stem_hash:
                stem_hash[key].append(temp_list)
            else:
                stem_hash[key] = [temp_list]

        if mode == 'generate' or mode == 'reinflect':
            feature_toks = elements[2].split(' ')
            key = feature_toks[1].split(":")[1]
            key = re.split('[_-]', key)[0]
            if key in lemma_hash:
                if element not in lemma_hash[key]:
                    lemma_hash[key].append(elements[2] + " " + "stemcat:" + elements[1])
            else:
                lemma_hash[key] = []
                lemma_hash[key].append(elements[2] + " " + "stemcat:" + elements[1])

        line = db_file.readline()

    while "TABLE BC" not in line:
        if line.startswith("#"):
            line = db_file.readline()

        if mode == 'analyze' or mode == 'reinflect':
            prefix_stem_compatibility[line.rstrip()] = None

        if mode == 'generate' or mode == 'reinflect':
            elements = line.split(" ")
            key = elements[1].rstrip()
            value = elements[0]
            if key in stem_prefix_compatibility_hash:
                stem_prefix_compatibility_hash[key].append(value)
            else:
                temp_list = []
                temp_list.append(value)
                stem_prefix_compatibility_hash[key] = temp_list

        line = db_file.readline()
    while "TABLE AC" not in line:
        if line.startswith("#"):
            line = db_file.readline()

        if mode == 'analyze' or mode == 'reinflect':
            stem_suffix_compatibility[line.rstrip()] = None

        if mode == 'generate' or mode == 'reinflect':
            elements = line.split(" ")
            key = elements[0]
            value = elements[1].rstrip()
            # temp_list = (value)
            if key in stem_suffix_compatibility_hash:
                stem_suffix_compatibility_hash[key].append(value)
            else:
                temp_list = []
                temp_list.append(value)
                stem_suffix_compatibility_hash[key] = temp_list

        line = db_file.readline()
    
    while line:
        if line.startswith("#"):
            line = db_file.readline()

        prefix_suffix_compatibility[line.rstrip()] = None

        line = db_file.readline()

    if mode == 'analyze' or mode == 'reinflect':
        prefix_keys = list(prefix_hash.keys())
        MAXPRELEN = len(max(prefix_keys, key=len))

        suffix_keys = list(suffix_hash.keys())
        MAXSUFLEN = len(max(suffix_keys, key=len))


# initialize the database from pickles
# dbInstall.py should have been run at least once before this initialize function is called
def initialize_from_hash(database, mode):
    global define_hash
    global default_hash
    global backoff_hash

    global prefix_hash
    global suffix_hash
    global stem_hash

    global lemma_hash
    global prefix_cat_hash
    global suffix_cat_hash

    global stem_prefix_compatibility_hash
    global stem_suffix_compatibility_hash

    global prefix_stem_compatibility
    global stem_suffix_compatibility
    global prefix_suffix_compatibility

    global MAXSUFLEN
    global MAXPRELEN

    try:
        define_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "define_hash.pk"), "rb"))
        default_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "default_hash.pk"), "rb"))
        prefix_suffix_compatibility = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "prefix_suffix_compatibility.pk"), "rb"))

        if mode == 'analyze' or mode == 'reinflect':
            backoff_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "backoff_hash.pk"), "rb"))
            prefix_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "prefix_hash.pk"), "rb"))
            suffix_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "suffix_hash.pk"), "rb"))
            stem_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "stem_hash.pk"), "rb"))
            prefix_stem_compatibility = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "prefix_stem_compatibility.pk"), "rb"))
            stem_suffix_compatibility = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "stem_suffix_compatibility.pk"), "rb"))

            prefix_keys = list(prefix_hash.keys())
            MAXPRELEN = len(max(prefix_keys, key=len))

            suffix_keys = list(suffix_hash.keys())
            MAXSUFLEN = len(max(suffix_keys, key=len))

        if mode == 'generate' or mode == 'reinflect':
            lemma_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "lemma_hash.pk"), "rb"))
            prefix_cat_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "prefix_cat_hash.pk"), "rb"))
            suffix_cat_hash = pickle.load(open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "suffix_cat_hash.pk"), "rb"))
            stem_suffix_compatibility_hash = pickle.load(
                open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "stem_suffix_compatibility_hash.pk"), "rb"))
            stem_prefix_compatibility_hash = pickle.load(
                open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", database, "stem_prefix_compatibility_hash.pk"), "rb"))
    except FileNotFoundError as err:
        print("One or more pickle files do not exist. Please run dbInstall again.")


# generate all the possible analyses of a given word
def analyze_word(input_word, v):
    global analysis_memo_hash
    verbose = v

    if clean_up_doc:
        clean_words = CalimaStarUtils.clean_line(input_word).split()
        all_analyses = []
        if len(clean_words) > 1:
            for clean_word in clean_words:
                all_analyses.append("#WORD: " + CalimaStarUtils.encode(input_encoding, output_encoding, clean_word))
                all_analyses.extend(analyze_word(clean_word, v))
                all_analyses.append("")
            return all_analyses

    word = CalimaStarUtils.encode(input_encoding, 'bw', input_word)

    if memoization:
        if word in analysis_memo_hash:
            return analysis_memo_hash[word]

    analyses = deque()

    if word is None or word is '':
        # print('{} - No word!!!!'.format(input_word))
        return None

    elif (not extended_alpha and any(x in word for x in non_bw)) or (
                extended_alpha and any(x in word for x in non_extended_bw)) or diac_pattern.search(word) is not None:
        default_analysis = default_hash["noun"]
        default_analysis["diac"] = word
        default_analysis["lex"] = word + "_0"
        default_analysis["bw"] = word + "/FOREIGN"
        default_analysis["gloss"] = word
        default_analysis["source"] = "foreign"
        analyses.append(CalimaStarUtils.printer(default_analysis, output_encoding, feature_order, tokenization))
        # analyses.append(default_analysis)
        return analyses

    elif digit_pattern.search(word) is not None:
        default_analysis = default_hash["digit"]
        default_analysis["diac"] = word
        default_analysis["lex"] = word + "_0"
        default_analysis["bw"] = word + "/PUNC"
        default_analysis["gloss"] = word
        default_analysis["source"] = "punc"
        analyses.append(CalimaStarUtils.printer(default_analysis, output_encoding, feature_order, tokenization))
        # analyses.append(default_analysis)
        return analyses

    elif punct_pattern.search(word) is not None:
        default_analysis = default_hash["punc"]
        default_analysis["diac"] = word
        default_analysis["lex"] = word + "_0"
        default_analysis["bw"] = word + "/NOUN_NUM"
        default_analysis["gloss"] = word
        default_analysis["source"] = "digit"
        analyses.append(CalimaStarUtils.printer(default_analysis, output_encoding, feature_order, tokenization))
        # analyses.append(default_analysis)
        return analyses

    match_word = word
    match_word = CalimaStarUtils.dediac(match_word, input_encoding)

    unvoc_word = match_word

    match_word = CalimaStarUtils.normalize(match_word, normalization, normalization_re)

    segmentations = __segment(match_word)

    for segmentation in segmentations:
        tokens = segmentation.split("\t")
        prefix = tokens[0]
        stem = tokens[1]
        suffix = tokens[2]

        if stem in stem_hash:
            for stem_value in stem_hash[stem]:
                stem_cat = stem_value[0]
                stem_analysis = stem_value[1]

                for prefix_value in prefix_hash[prefix]:
                    prefix_cat = prefix_value[0]
                    prefix_analysis = prefix_value[1]

                    prefix_stem_cat = prefix_cat + ' ' + stem_cat
                    if prefix_stem_cat in prefix_stem_compatibility:
                        for suffix_value in suffix_hash[suffix]:
                            suffix_cat = suffix_value[0]
                            suffix_analysis = suffix_value[1]

                            stem_suffix_cat = stem_cat + ' ' + suffix_cat
                            if stem_suffix_cat in stem_suffix_compatibility:
                                prefix_suffix_cat = prefix_cat + ' ' + suffix_cat
                                if prefix_suffix_cat in prefix_suffix_compatibility:
                                    combined_analyses_hash = __merge_features(prefix_analysis, stem_analysis,
                                                                              suffix_analysis)

                                    unvoc_str = CalimaStarUtils.dediac(combined_analyses_hash["diac"], input_encoding)

                                    if unvoc_str != unvoc_word:
                                        combined_analyses_hash["source"] = "spvar"

                                    combined_analyses_hash["stem"] = stem_analysis['diac']
                                    combined_analyses_hash["stemcat"] = stem_cat

                                    if __valid_analysis(combined_analyses_hash['diac'], word):
                                        # SALAM: add the POS prob
                                        if "POS_prob" in feature_order:
                                            # TODO: create the below funtion
                                            BW_semi_lex = CalimaStarUtils.get_BW_semi_lex(combined_analyses_hash["bw"])
                                            if BW_semi_lex in POS_prob_hash:
                                                combined_analyses_hash["POS_prob"] = POS_prob_hash[BW_semi_lex]
                                            else:
                                                combined_analyses_hash["POS_prob"] = "-99"
                                        analyses.append(CalimaStarUtils.printer(combined_analyses_hash, output_encoding,
                                                                                feature_order, tokenization))
                                        # analyses.append(combined_analyses_hash)
    if 'ADD' in backoff:
        backoff_analyses = __analyze_with_backoff(segmentations, word)
        for analysis in backoff_analyses:
            analyses.append(analysis)
    elif 'NOAN' in backoff and not analyses:
        analyses = __analyze_with_backoff(segmentations, word)

    if memoization:
        analysis_memo_hash[word] = analyses

    return __sort(analyses, word)
    # return analyses

# def write_to_file(analysis, output_encoding, output_file, feature_order, tokenization):

#     if 'diac' in analysis:
#         analysis['diac'] = CalimaStarUtils.encode('bw', output_encoding, analysis['diac'])
#     if 'stem' in analysis:
#         analysis['stem'] = CalimaStarUtils.encode('bw', output_encoding, analysis['stem'])
#     if 'lex' in analysis:
#         lemma_toks = split_lemma.split(analysis['lex'])
#         lemma_stripped = CalimaStarUtils.encode('bw', output_encoding, lemma_toks[0].rstrip())
#         analysis['lex'] = lemma_stripped + ''.join(lemma_toks[1:])

#     if 'bw' in analysis:
#         bw_encoded = ''
#         bw_toks = analysis['bw'].split('+')
#         bw_tok = bw_toks[0]
#         if bw_tok:
#             morpheme = CalimaStarUtils.encode('bw', output_encoding, bw_tok.split('/')[0])
#             bw = bw_tok.split('/')[1]
#             bw_encoded = morpheme + '/' + bw


#         for bw_tok in bw_toks[1:]:
#             if bw_tok:
#                 morpheme = CalimaStarUtils.encode('bw', output_encoding, bw_tok.split('/')[0])
#                 bw = bw_tok.split('/')[1]
#                 bw_encoded = bw_encoded + '+' + morpheme + '/' + bw

#         if len(bw_encoded.split("+")) < 3:
#             bw_encoded = bw_encoded + "+"

#         analysis['bw'] = bw_encoded

#     buff = io.StringIO()
#     output_string = ''

#     for order in feature_order:
#         if order in analysis:
#             # todo: test with extended db
#             if (order == 'seg' or order == 'tok') and order in tokenization:
#                 for ttype in tokenization[order]:
#                     # buff.write(order)
#                     # buff.write('_')
#                     # buff.write(ttype)
#                     # buff.write(analysis['{}_{} '.format(order, ttype)])
#                     output_string = output_string + order + '_' + ttype + analysis[order + '_' + ttype] + ' '
#             else:
#                 # buff.write(order)
#                 # buff.write(':')
#                 # buff.write(analysis[order])
#                 # buff.write(' ')
#                 output_string = output_string + order + ":" + analysis[order] + " "

#     # buff.write('\n')
#     output_string += '\n'

#     output_file.write(output_string)

# read a file of words, and generate all possible analyses for every word in the file
# output is written directly in a file
def analyze_file(input_file, output_path, v):
    verbose = v
    line = input_file.readline()

    output_path = open(output_path, 'w')

    for line in input_file:
        if clean_up_doc:
            line = CalimaStarUtils.clean_line(line)
        # print("Line {}".format(linenum))
        words = line.strip().split()
        for word in words:
            analyses = analyze_word(word, v)
            output_path.write("#WORD: " + CalimaStarUtils.encode(input_encoding, output_encoding, word) + "\n")
            # sys.stdout.write("#WORD: " + CalimaStarUtils.encode(input_encoding, output_encoding, word) + "\n")
            # output_path.write('#WORD: {}\n'.format(CalimaStarUtils.encode(input_encoding, output_encoding, word)))
            if analyses:
                for analysis in analyses:
                    # write_to_file(analysis, output_encoding, output_path, feature_order, tokenization)
                    output_path.write(analysis + "\n")
                    # sys.stdout.write(analysis + "\n")
                    # output_path.write("{}\n".format(analysis))
            else:
                output_path.write("NO_ANALYSIS\n")
                # sys.stdout.write("NO_ANALYSIS\n")
            # output_path.write("\n")
            output_path.write("\n")

    output_path.flush()
    # sys.stdout.flush()
    output_path.close()


# generate all the possible words from a given lemma and a set of features
def generate_word(lemma, features, v):
    global generation_memo_hash
    verbose = v

    generated_output = []

    lemma = CalimaStarUtils.encode(input_encoding, 'bw', lemma)

    if lemma not in lemma_hash:
        errorList = []
        errorList.append("ERROR: The lemma " + lemma + " is not in the database")
        return errorList

    __check_feature_redundancy(features)

    features_hash = __get_features_hash(features.rstrip())
    for generation_feature in features_hash:
        if generation_feature not in define_hash:
            errorList = []
            errorList.append("ERROR: The feature " + generation_feature + " is not a valid feature")
            return errorList

    if "prc0" not in features_hash:
        features_hash["prc0"] = '0'

    if "prc1" not in features_hash:
        features_hash["prc1"] = '0'

    if "prc2" not in features_hash:
        features_hash["prc2"] = '0'

    if "prc3" not in features_hash:
        features_hash["prc3"] = '0'

    if "enc0" not in features_hash:
        features_hash["enc0"] = '0'

    if "pos" not in features_hash:
        errorList = []
        errorList.append("ERROR: pos is not specified")
        return errorList

    line = lemma + ' ' + __simple_print(features_hash)

    if memoization:
        if line in generation_memo_hash:
            return generation_memo_hash[line]

    # we assume pos is give in current db format because of lemmas having multiple pos's
    # also to be able to work with the fact that we are indexing lemmas without their _#
    # since it should not be expected for a user to know lemma codes
    # pos is used to produce error messages when an incompatible feature is specified
    # e.g. noun and vox or verb and stt
    pos = features_hash["pos"]
    
    if pos not in define_hash["pos"]:
        errorList = []
        errorList.append("ERROR: The pos value " + pos + " is not a valid pos")
        return errorList

    default_features = default_hash[pos]

    for feature in features_hash:
        if default_features[feature] == "na" and features_hash[feature] != "na":
            errorList = []
            errorList.append("ERROR: Feature " + feature + " is not a valid feature for pos " + pos)
            return errorList

        if features_hash[feature] not in define_hash[feature]:
            errorList = []
            errorList.append("ERROR: Feature " + feature + " cannot take the value " + features_hash[feature])
            return errorList

    stem_list = lemma_hash[lemma]
    for stem_entry in stem_list:
        stem_features = __get_features_hash(stem_entry)

        if "vox" in features_hash and stem_features["vox"] != features_hash["vox"]:
            continue

        if "rat" in features_hash and stem_features["rat"] != features_hash["rat"]:
            continue

        if "pos" in features_hash and stem_features["pos"] != features_hash["pos"]:
            continue

        stemcat = stem_features['stemcat']

        potential_prefixes = stem_prefix_compatibility_hash[stemcat]
        potential_suffixes = stem_suffix_compatibility_hash[stemcat]

        for prefix in potential_prefixes:
            prefix_list_features = prefix_cat_hash[prefix]
            for prefix_list_entry in prefix_list_features:
                # prefix_features = __get_features_hash(prefix_list_entry[0])
                prefix_features = prefix_list_entry
                prefix_flag = True
                for feature in features_hash:
                    if "prc" in feature:
                        if features_hash[feature] != '0' and feature not in prefix_features:
                            prefix_flag = False
                            break
                        elif feature in prefix_features and features_hash[feature] != prefix_features[feature]:
                            prefix_flag = False
                            break

                if prefix_flag:
                    for suffix in potential_suffixes:

                        if prefix + ' ' + suffix in prefix_suffix_compatibility:

                            suffix_list_features = suffix_cat_hash[suffix]

                            for suffix_list_entry in suffix_list_features:
                                # suffix_features = __get_features_hash(suffix_list_entry[0])
                                suffix_features = suffix_list_entry

                                suffix_flag = True
                                for feature in features_hash:
                                    if "enc" in feature:
                                        if features_hash[feature] != '0' and feature not in suffix_features:
                                            suffix_flag = False
                                            break
                                        elif feature in suffix_features and features_hash[feature] != suffix_features[
                                            feature]:
                                            suffix_flag = False
                                            break

                                if suffix_flag:
                                    combined_analyses_hash = __merge_features(prefix_features, stem_features,
                                                                              suffix_features)

                                    word_flag = True

                                    for feature in features_hash:
                                        if feature in combined_analyses_hash and combined_analyses_hash[feature] != \
                                                features_hash[feature]:
                                            word_flag = False
                                            break

                                    if word_flag:
                                        output_string = CalimaStarUtils.printer(combined_analyses_hash, output_encoding,
                                                                                feature_order, tokenization)
                                        generated_output.append(output_string)

    if memoization:
        generation_memo_hash[line] = generated_output

    return generated_output


# read a file with the structure
# lemma features
# where features is a string of space separated feature-value pairs, and each feature-value pair is colon ':' separated
# the output is written directly in a file
def generate_file(input_file, output_path, v):
    verbose = v
    # the expected format of the file is lemma features
    line = input_file.readline().rstrip()
    output_path = open(output_path, 'w')

    while line:
        tokens = line.split(" ")
        lemma = tokens[0]
        features = ' '.join(tokens[1:])

        output_path.write("#LEMMA: " + CalimaStarUtils.encode(input_encoding, output_encoding, lemma) + "\n"
                          + "#FEATURES: " + features + "\n")
        generations = generate_word(lemma, features, v)
        if generations:
            for generation in generations:
                output_path.write(generation + "\n")
        else:
            output_path.write("NO_POSSIBLE_GENERATIONS" + "\n")
        output_path.write("\n")
        line = input_file.readline().rstrip()

    output_path.close()


# given a word, generate all analyses, select valid analyses, and generate the required features from the lemmas of the
# valid analyses
def reinflect_word(word, features, v):
    global reinflection_memo_hash
    verbose = v

    output_array = []

    analyses = analyze_word(word, v)
    if not analyses:
        errorList = []
        errorList.append("ERROR: Word " + word + " cannot be analyzed")
        return errorList

    __check_feature_redundancy(features)

    if len(features) == 0:
        output_array.append(word)
        return output_array

    generation_features_hash = __get_features_hash(features.rstrip())

    for generation_feature in generation_features_hash:
        if generation_feature not in define_hash:
            errorList = []
            errorList.append("ERROR: The feature " + generation_feature + " is not a valid feature")
            return errorList

    line = word + ' ' + __simple_print(generation_features_hash)

    if memoization:
        if line in reinflection_memo_hash:
            return reinflection_memo_hash[line]

    clitic_flag = False
    if "enc" in features or "prc" in features:
        clitic_flag = True

    for analysis in analyses:
        analysis_features = __get_features_hash(analysis)

        diac = analysis_features["diac"]
        diac = CalimaStarUtils.encode(output_encoding, input_encoding, diac)

        # check if diac is the same as the input word or not
        if CalimaStarUtils.dediac(diac, input_encoding) != CalimaStarUtils.dediac(word, input_encoding):
            return None

        if ("pos" in generation_features_hash and analysis_features["pos"] == generation_features_hash["pos"]) or \
                        "pos" not in generation_features_hash:
            lemma = CalimaStarUtils.encode(output_encoding, input_encoding, analysis_features["lex"])
            lemma = re.split('[_-]', lemma)[0].rstrip()
            generation_feature = ""
            valid_flag = True
            for feature in analysis_features:
                if feature in features_not_for_generation:
                    pass
                elif clitic_flag and feature in special_case_features_not_for_generation:
                    pass
                else:
                    if feature in generation_features_hash:
                        if analysis_features[feature] != "na":
                            generation_feature = generation_feature + feature + ":" + \
                                                 generation_features_hash[feature] + " "
                        else:
                            valid_flag = False
                            break
                    else:
                        generation_feature = generation_feature + feature + ":" + analysis_features[feature] + " "

            if valid_flag:
                generation_feature = generation_feature.rstrip()
                generations = generate_word(lemma, generation_feature, v)

            for generation in generations:
                output_array.append(generation)

    output_array = list(set(output_array))

    if memoization:
        reinflection_memo_hash[line] = output_array

    return output_array


# read a file with the structure
# word features
# where features is a string of space separated feature-value pairs, and each feature-value pair is colon ':' separated
# the output is written directly in a file
def reinflect_file(input_file, output_path, v):
    verbose = v
    # the expected format of the file is word features
    line = input_file.readline().rstrip()
    output_path = open(output_path, 'w')

    while line:
        tokens = line.split(" ")
        word = tokens[0]
        features = ' '.join(tokens[1:])

        output_path.write("#WORD: " + CalimaStarUtils.encode(input_encoding, output_encoding, word) +
                          "\n" + "#FEATURES: " + features + "\n")
        reinflections = reinflect_word(word, features, v)
        if reinflections:
            for reinflection in reinflections:
                output_path.write(reinflection + "\n")
        else:
            output_path.write("NO_POSSIBLE_REINFLECTIONS" + "\n")
        output_path.write("\n")
        line = input_file.readline().rstrip()

    output_path.close()


# segment a word and return a list of all possible prefix-stem-suffix values
def __segment(word):
    global define_hash
    global default_hash

    global prefix_hash
    global suffix_hash
    global stem_hash

    global prefix_stem_compatibility
    global stem_suffix_compatibility
    global prefix_suffix_compatibility

    global MAXSUFLEN
    global MAXPRELEN

    prefix_len = 0
    suffix_len = 0
    stem_len = 0

    prefix = ""
    suffix = ""
    stem = ""

    str_len = len(word)

    segmentations = []

    while prefix_len <= MAXPRELEN:
        prefix = word[0:prefix_len]
        if prefix in prefix_hash:
            stem_len = str_len - prefix_len
            suffix_len = 0
            while stem_len >= 1 and suffix_len <= MAXSUFLEN:
                stem = word[prefix_len: prefix_len + stem_len]
                suffix = word[prefix_len + stem_len:]
                if suffix in suffix_hash:
                    segmentations.append(prefix + "\t" + stem + "\t" + suffix)
                stem_len -= 1
                suffix_len += 1
        prefix_len += 1

    return segmentations


# generate a hash from a line of space separated feature-value pairs
def __get_features_hash(line):
    features_hash = {}

    tokens = line.split()

    for token in tokens:
        subtoks = token.split(":")
        if len(subtoks) != 2:
            # Salam Jan 15th 2018
            # This happens when the BW of the Gloss tag have a ':' in the feature value
            features_hash[subtoks[0]] = ':'.join(subtoks[1:])
            # continue
        else:
            features_hash[subtoks[0]] = subtoks[1]

    return features_hash


# get the feature value from a feature hash
# this function is needed to avoid getting a None value when a feature does not exist
def __get_feature(feature_hash, feature):
    if feature in feature_hash:
        return feature_hash[feature]
    else:
        return ''


# generate the features hash that results in combining a prefix, stem, and suffix
# feature order for merged features is prefix > suffix > stem
# other features are concatinated or generated according to predetermined lists of features
def __merge_features(prefix_features, stem_features, suffix_features):
    merged_features_hash = {}

    for key in stem_features:
        if key in feature_order:
            merged_features_hash[key] = stem_features.get(key, '')

            if key in suffix_features:
                suff_feat = suffix_features.get(key, '')
                if suff_feat != '-' and suff_feat != '':
                    merged_features_hash[key] = suff_feat

            if key in prefix_features:
                pref_feat = prefix_features.get(key, '')
                if pref_feat != '-' and pref_feat != '':
                    merged_features_hash[key] = pref_feat

    for feature in concatinating_features:
        if feature in feature_order:
            if feature in stem_features:
                if 'seg' in feature or 'tok' in feature:
                    merged_features_hash[feature] = '{}{}{}'.format(prefix_features.get(feature, ''),
                                                stem_features.get(feature, ''),
                                                suffix_features.get(feature, ''))
                else:
                    merged_features_hash[feature] = '{}+{}+{}'.format(prefix_features.get(feature, ''),
                                                stem_features.get(feature, ''),
                                                suffix_features.get(feature, ''))

    if "diac" in feature_order:
        voc_str = __rewrite_rules(merged_features_hash["diac"])

        merged_features_hash["diac"] = voc_str

    # Salam addition for caphi
    if "caphi" in feature_order:
        caphi_str = __rewrite_rules_caphi(merged_features_hash["caphi"])
        merged_features_hash["caphi"] = caphi_str
    if "stem" in feature_order:
        merged_features_hash["stem"] = stem_features["diac"]
    if "gen" in feature_order:
        if merged_features_hash["gen"] == '-':
            merged_features_hash["gen"] = merged_features_hash["form_gen"]
    if "num" in feature_order:
        if merged_features_hash["num"] == '-':
            merged_features_hash["num"] = merged_features_hash["form_num"]
    if "pattern" in feature_order:
        merged_features_hash["pattern"] = '{}+{}+{}'.format(prefix_features.get('diac', ''), stem_features.get('pattern', ''), suffix_features.get('diac', ''))

    return merged_features_hash


# apply different rewrite rules on words including:
# the addition of $dp after sun letters
# removing of ftHp after Alf followed with the suffix tA or tA mrbwTp
# changing non-hamzated starting Alf to Alf hmzp wSl
# removing pluses
# adding ftHp before Alf and Alf mqSwrY
# modifying the orthography of tnwyn ftH before or after Alf
def __rewrite_rules(word):
    word = CalimaStarUtils.rewrite_rules(word)

    if tnwyn_ftH == "AF":
        if word.endswith("FA"):
            word = FA_re.sub("AF", word)
        if word.endswith("FY"):
            word = FY_re.sub("YF", word)
    elif tnwyn_ftH == "FA":
        if word.endswith("AF"):
            word = AF_re.sub("FA", word)
        if word.endswith("YF"):
            word = YF_re.sub("FY", word)

    return word

# Salam addition to caphi
def __rewrite_rules_caphi(word):
    word = CalimaStarUtils.rewrite_rules_caphi(word)

    return word


# return a string with the values of features in the hash ordered according to feature_order list, separated by spaces
def __simple_print(feat_hash):
    output_string = ''
    for order in feature_order:
        if order in feat_hash:
            output_string = output_string + order + ":" + feat_hash[order] + " "
    return output_string.rstrip()


# check if there are redundant features in generate and reinflect calls
def __check_feature_redundancy(feature):
    feature_tokens = feature.split(" ")
    features = {}
    for feature_entry in feature_tokens:
        if feature_entry:
            feature = feature_entry.split(":")[0]
            value = feature_entry.split(":")[1]
            if feature in features and value != features[feature]:
                print(
                    "WARNING: The feature " + feature + " appears with values " + features[
                        feature] + " and " + value + ".")
                print("Please note that the last value is the one that will be considered for your generation and "
                      "reinflection task.")
                features[feature] = value
            else:
                features[feature] = value
    pass


# check if the analysis is valid according to specific config values
# used to select valid analyses in the analysis code and lemmas to be run through generation in the reinflection code
def __valid_analysis(diac, word):
    return __valid_diacritized_analysis(diac, word) and __valid_orthographic_analysis(diac, word)


def __valid_orthographic_analysis(diac, word):
    if orthographic_match == 'none':
        return True
    elif orthographic_match == 'full':
        return CalimaStarUtils.dediac(diac, input_encoding) == CalimaStarUtils.dediac(word, input_encoding)
    else:
        if len(CalimaStarUtils.dediac(diac, input_encoding)) != len(CalimaStarUtils.dediac(word, input_encoding)):
            return False
        for char_analysis in CalimaStarUtils.dediac(diac, input_encoding):
            for char_word in CalimaStarUtils.dediac(word, input_encoding):
                if char_analysis != char_word:
                    if char_analysis in normalization and normalization[char_analysis] != char_word:
                        if char_word in normalization and normalization[char_word] != char_analysis:
                            return False
    return True


def __valid_diacritized_analysis(diac, word):
    if diac_match == 'none':
        return True
    elif diac_match == 'full':
        return diac == word
    else:
        for aset in __editops(CalimaStarUtils.normalize(word, normalization, normalization_re), CalimaStarUtils.normalize(diac,
                                                                                                        normalization, normalization_re)):
            if aset[0] != 'insert':
                return False
    return True



# sort the analyses according to a sort criteria
# random returns anlayses in the order they were generated
# frequency returns analyses according to the value of the 'freq' feature in descending order
# diac returns analyses according to the Levenshtein distance in ascending order
# alphabetical returns analyses according to the default alphabetical order in Arabic (whether it is utf8, bw, sbw, hsb)
# note: alphabetical order doesn't work well with ArabTex output because of the multiple character issue
def __sort(analyses, word):
    if analysis_order == 'random':
        return analyses
    else:
        # TODO: sort in hash not string 
        output_analyses_hash = {}
        for analysis in analyses:
            analysis_hash = __get_features_hash(analysis)
            if analysis_order == 'frequency':
                freq = analysis_hash.get('freq', '')
                output_analyses_hash[analysis] = freq
            elif analysis_order == 'diac':  # Levenshtein distance
                diac = analysis_hash.get('diac', '')
                output_analyses_hash[analysis] = __distance(word, diac)
            elif analysis_order == 'alphabetical':
                diac = analysis_hash.get('diac', '')
                output_analyses_hash[analysis] = diac

        # sort hashes according to value instead of key, and generate the sorted analyses list
        if analysis_order == 'frequency':
            sorted_analyses = [(k, output_analyses_hash[k]) for k in
                               sorted(output_analyses_hash, key=output_analyses_hash.get, reverse=True)]
        elif analysis_order == 'diac':
            sorted_analyses = [(k, output_analyses_hash[k]) for k in
                               sorted(output_analyses_hash, key=output_analyses_hash.get, reverse=False)]
        else:
            if output_encoding == 'bw':
                sorted_analyses = [(k, output_analyses_hash[k]) for k in
                                   sorted(output_analyses_hash,
                                          key=lambda x: [bw_alpha_order.index(c) if c in bw_alpha_order else ord(c) for
                                                         c in x])]
            elif output_encoding == 'sbw':
                sorted_analyses = [(k, output_analyses_hash[k]) for k in
                                   sorted(output_analyses_hash,
                                          key=lambda x: [sbw_alpha_order.index(c) if c in sbw_alpha_order else ord(c)
                                                         for
                                                         c in x])]
            elif output_encoding == 'hsb':
                sorted_analyses = [(k, output_analyses_hash[k]) for k in
                                   sorted(output_analyses_hash,
                                          key=lambda x: [hsb_alpha_order.index(c) if c in hsb_alpha_order else ord(c)
                                                         for
                                                         c in x])]
            elif output_encoding == 'utf8':
                sorted_analyses = [(k, output_analyses_hash[k]) for k in
                                   sorted(output_analyses_hash, key=output_analyses_hash.get, reverse=False)]
            else:
                sorted_analyses = [(k, output_analyses_hash[k]) for k in
                                   sorted(output_analyses_hash,
                                          key=lambda x: [
                                              arabtex_alpha_order.index(c) if c in arabtex_alpha_order else ord(c)
                                              for
                                              c in x])]
        analyses = []
        for analysis in sorted_analyses:
            analyses.append(analysis[0])
    return analyses


def __distance(string1, string2):
    n1 = len(string1)
    n2 = len(string2)
    return __levenshtein_distance_matrix(string1, string2)[n1][n2]


def __levenshtein_distance_matrix(string1, string2):
    n1 = len(string1)
    n2 = len(string2)
    d = [[0 for x in range(n2 + 1)] for y in range(n1 + 1)]
    for i in range(n1 + 1):
        # d[i, 0] = i
        d[i][0] = i
    for j in range(n2 + 1):
        # d[0, j] = j
        d[0][j] = j
    for i in range(n1):
        for j in range(n2):
            if string1[i] == string2[j]:
                cost = 0
            else:
                cost = 1
            d[i + 1][j + 1] = min(d[i][j + 1] + 1,  # insert
                                  d[i + 1][j] + 1,  # delete
                                  d[i][j] + cost)  # replace
    return d


def __editops(string1, string2):
    dist_matrix = __levenshtein_distance_matrix(string1, string2)
    i, j = (len(__levenshtein_distance_matrix(string1, string2)),) + (len(__levenshtein_distance_matrix(string1, string2)[0]),)
    i -= 1
    j -= 1
    ops = list()
    while i != -1 and j != -1:
        values = [dist_matrix[i-1][j-1], dist_matrix[i][j-1], dist_matrix[i-1][j]]
        index = values.index(min(values))

        if index == 0:
            if dist_matrix[i][j] > dist_matrix[i-1][j-1]:
                ops.insert(0, ('replace', i - 1, j - 1))
            i -= 1
            j -= 1
        elif index == 1:
            ops.insert(0, ('insert', i - 1, j - 1))
            j -= 1
        elif index == 2:
            ops.insert(0, ('delete', i - 1, i - 1))
            i -= 1
    return ops


# if backoff is set to a value other than none, this function is called to generate the backoff analyses of a given word
def __analyze_with_backoff(segmentations, word):
    analyses = []
    for segmentation in segmentations:
        tokens = segmentation.split("\t")
        prefix = tokens[0]
        stem = tokens[1]
        suffix = tokens[2]

        for prefix_value in prefix_hash[prefix]:
            prefix_cat = prefix_value[0]
            prefix_analysis = prefix_value[1]

            for suffix_value in suffix_hash[suffix]:
                suffix_cat = suffix_value[0]
                suffix_analysis = suffix_value[1]

                prefix_suffix_cat = prefix_cat + ' ' + suffix_cat
                if prefix_suffix_cat in prefix_suffix_compatibility:
                    stem_cats = []
                    if 'ALL' in backoff:
                        stem_cats = backoff_hash['ALL']
                    elif 'PROP' in backoff:
                        stem_cats = backoff_hash['PROP']
                    for stem_value in stem_hash['NOAN']:
                        stem_cat = stem_value[0]
                        stem_analysis = stem_value[1]
                        if stem_cat in stem_cats:
                            prefix_stem_cat = prefix_cat + ' ' + stem_cat
                            if prefix_stem_cat in prefix_stem_compatibility:
                                stem_suffix_cat = stem_cat + ' ' + suffix_cat
                                if stem_suffix_cat in stem_suffix_compatibility:

                                    if 'PROP' in backoff and 'NOUN_PROP' not in stem_analysis['bw']:
                                        continue

                                    stem_analysis['bw'] = analyze_with_backoff_re.sub(stem, stem_analysis['bw'])
                                    stem_analysis['diac'] = analyze_with_backoff_re.sub(stem, stem_analysis['diac'])
                                    stem_analysis['lex'] = analyze_with_backoff_re.sub(stem, stem_analysis['lex'])

                                    combined_analyses_hash = __merge_features(prefix_analysis, stem_analysis,
                                                                              suffix_analysis)

                                    combined_analyses_hash["stem"] = stem_analysis["diac"]
                                    combined_analyses_hash["stemcat"] = stem_cat
                                    combined_analyses_hash["source"] = "backoff"
                                    combined_analyses_hash["gloss"] = stem_analysis["gloss"]

                                    if combined_analyses_hash['bw'] == 'ka/PREP+tb/NOUN+K/CASE_INDEF_GEN':
                                        print()

                                    if __valid_analysis(combined_analyses_hash['diac'], word):
                                        analyses.append(CalimaStarUtils.printer(combined_analyses_hash, output_encoding,
                                                                                feature_order, tokenization))
                                        # analyses.append(combined_analyses_hash)
    return analyses


if __name__ == "__main__":

    # initialize_from_file("/Users/dimataji/Google Drive/ My_CAMeL_Files/Apps/ALMOR/almor-s31.db", 'reinflect')

    try:
        config_file = open("config.xml", 'r')
        config_file.close()
        read_config("config.xml")
    except IOError as err:
        print("Configuration file does not exist!")
        sys.exit(2)
    #
    initialize_from_hash("almor-s31.db", 'reinflect')
    #
    # run analyze on word

    a = analyze_word("syArh",verbose)
    # a = analyze_word("kamAn")
    for a1 in a:
        print(a1)
    # # a = analyze_word('wbAl$ms')
    #
    #
    # # run analyze on file
    #
    # try:
    #     # input_source = "example.txt"
    #     # output = "output.test.utf8_input"
    #     input_source = 'input.test'
    #     output = 'output.test'
    #     file = open(input_source, 'r')
    #     # temp = file.read()
    #     print()
    #     analyze_file(file, output)
    #     pass
    # except IOError as err:
    #     print(err)
    #     sys.exit(2)
    #
    # # run generate on word
    # # a = generate_word("katab", "pos:verb num:d gen:f prc2:wa_conj enc0:3ms_dobj vox:a")
    # # a = generate_word("$amos", "pos:noun stt:d cas:a prc2:wa_conj prc1:bi_prep prc0:Al_det")
    # # for a1 in a:
    # #     print(a1)
    #
    # # run generate on file
    # try:
    #     input_source = "generate_input.txt"
    #     output = "generate_output.txt"
    #     file = open(input_source, 'r')
    #     generate_file(file, output)
    # except IOError as err:
    #     print(err)
    #     sys.exit(2)
    #
    # # reinflection on word
    # # a = reinflect_word("katab", "num:d prc2:wa_conj")
    # # a = reinflect_word("wbiAlmdrs", "num:p")
    # # a = reinflect_word("$amos", "prc2:wa_conj prc1:bi_prep prc0:Al_det")
    # # for a1 in a:
    # #     print(a1)
    #
    # run reinflection on file
    # try:
    #     input_source = "reinflection_input.txt"
    #     output = "reinflection_output.txt"
    #     file = open(input_source, 'r')
    #     reinflect_file(file, output, False)
    # except IOError as err:
    #     print(err)
    #     sys.exit(2)

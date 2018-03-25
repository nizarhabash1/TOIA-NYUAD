import re

rationalities = {}
stem_lemmas_hash = {}


def ammend_gender_number(database):
    rules = {}
    try:
        db_rules = open("lemmasWithRules.txt", 'r')

        for line in db_rules.readlines():
            segments = line.rstrip().split("\t")
            lemma = segments[0]
            pos = segments[1]
            stem = segments[2]
            stemcat = segments[3]
            annotation = re.sub(r"^f", "", segments[5]) + " " + re.sub(r"^f", "", segments[6])
            key1 = lemma + "\t" + pos
            key2 = stem + "\t" + stemcat
            if key1 in stem_lemmas_hash:
                if key2 in stem_lemmas_hash[key1]:
                    print(key1 + "\t" + key2 + "\t\t" + stem_lemmas_hash[key1][key2] + "\t\t" + annotation)
                else:
                    stem_lemmas_hash[key1][key2] = annotation
            else:
                stem_lemmas_hash[key1] = {}
                stem_lemmas_hash[key1][key2] = annotation
        print()

        output = open(database + "+func", 'w')
        check = open("check_rules", 'w')

        almor_s31 = open(database, 'r')
        line = almor_s31.readline()

        while "DEFAULT" not in line:
            output.write(line)
            line = almor_s31.readline()

        output.write("DEFINE form_gen form_gen:na form_gen:m form_gen:f\n")
        output.write("DEFINE form_num form_num:s form_num:na form_num:d form_num:u form_num:p\n")

        while "ORDER" not in line:
            if line.startswith("DEFAULT"):
                if "pos:verb " not in line:
                    segments = re.split(" ", line.rstrip())
                    line = ""
                    for segment in segments:
                        if segment.startswith("gen") and "na" not in segment:
                            segment = "gen:-"
                        if segment.startswith("num") and "na" not in segment:
                            segment = "num:-"
                        line = line + segment + " "
                    line = line.rstrip()
                    if  "gen:na" in line:
                        line = line + " " + "form_gen:na form_num:na\n"
                    else:
                        line = line + " " + "form_gen:m form_num:s\n"
                else:
                    line = line.rstrip() + " " + "form_gen:m form_num:s\n"
            output.write(line)
            line = almor_s31.readline()

        while "STEMS" not in line:
            if line.startswith("ORDER"):
                line = line.rstrip() + " form_gen form_num\n"
            if "NSuff" in line:
                line = re.sub("gen:", "form_gen:", line)
                line = re.sub("num:", "form_num:", line)
            output.write(line)
            line = almor_s31.readline()

        while "TABLE" not in line:
            if line.startswith("#"):
                output.write(line)
                line = almor_s31.readline()
            else:
                segments = re.split(" ", line.rstrip())
                pos = segments[4]
                if "verb" not in pos and "NOAN" not in line:
                    lemma = segments[1]
                    if lemma == "lex:{imotiHAn_1":
                        print()
                    pos = segments[4]
                    stem = "stem:" + segments[0].split("\t")[0]
                    stemcat = "stemCat:" + segments[0].split("\t")[1]
                    key1 = lemma + "\t" + pos
                    key2 = stem + "\t" + stemcat
                    if key1 in stem_lemmas_hash:
                        if key2 in stem_lemmas_hash[key1]:
                            line = " ".join(segments[0:12])
                            line = line + " " + stem_lemmas_hash[key1][key2] + " "
                            line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + segments[
                                18] + " form_" + segments[13] + " form_" + segments[14]
                            output.write(line + "\n")
                        else:
                            line = " ".join(segments[0:12])
                            line = line + " " + "gen:- num:- "
                            line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + segments[
                                18] + " form_" + segments[13] + " form_" + segments[14]
                            output.write(line + "\n")
                    else:
                        if pos == 'noun':
                            key1 = lemma + "\t" + "adj"
                            if key1 in stem_lemmas_hash:
                                if key2 in stem_lemmas_hash[key1]:
                                    line = " ".join(segments[0:12])
                                    line = line + " " + stem_lemmas_hash[key1][key2] + " "
                                    line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + \
                                           segments[18] + " form_" + segments[13] + " form_" + segments[14]
                                    output.write(line + "\n")
                                else:
                                    line = " ".join(segments[0:12])
                                    line = line + " " + "gen:- num:- "
                                    line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + \
                                           segments[
                                               18] + " form_" + segments[13] + " form_" + segments[14]
                                    output.write(line + "\n")
                            else:
                                line = " ".join(segments[0:12])
                                line = line + " " + "gen:- num:- "
                                line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + segments[
                                    18] + " form_" + segments[13] + " form_" + segments[14]
                                output.write(line + "\n")
                        elif pos == 'adj':
                            key1 = lemma + "\t" + "noun"
                            if key1 in stem_lemmas_hash:
                                if key2 in stem_lemmas_hash[key1]:
                                    line = " ".join(segments[0:12])
                                    line = line + " " + stem_lemmas_hash[key1][key2] + " "
                                    line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + \
                                           segments[18] + " form_" + segments[13] + " form_" + segments[14]
                                    output.write(line + "\n")
                                else:
                                    line = " ".join(segments[0:12])
                                    line = line + " " + "gen:- num:- "
                                    line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + \
                                           segments[
                                               18] + " form_" + segments[13] + " form_" + segments[14]
                                    output.write(line + "\n")
                            else:
                                line = " ".join(segments[0:12])
                                line = line + " " + "gen:- num:- "
                                line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + segments[
                                    18] + " form_" + segments[13] + " form_" + segments[14]
                                output.write(line + "\n")
                        else:
                            line = " ".join(segments[0:12])
                            line = line + " " + "gen:- num:- "
                            line = line + segments[15] + " " + segments[16] + " " + segments[17] + " " + segments[
                                18] + " form_" + segments[13] + " form_" + segments[14]
                            output.write(line + "\n")
                else:
                    output.write(line)
                line = almor_s31.readline()

        while line:
            output.write(line)
            line = almor_s31.readline()

        output.close()
        check.close()

    except IOError as err:
        print(err)


def ammend_rationality(database):
    combine_rationality()
    try:
        almor_s31 = open(database, 'r')
        output= open(database + "+rat", 'w')
        output_check = open("check", 'w')
        line = almor_s31.readline()

        while "STEMS" not in line:
            if line.startswith("DEFINE") and "rat" in line:
                line = line.rstrip() + " rat:i rat:r\n"
            output.write(line)
            line = almor_s31.readline()

        while "TABLE" not in line:
            if "STEMS" in line:
                output.write(line)
            else:
                segments = re.split(" ", line)
                pos = re.sub("pos:", "", segments[4])
                if pos == "noun" or pos == "noun_prop":
                    lemma = re.sub("lex:", "", segments[1])
                    if lemma + "\t" + pos in rationalities:
                        line = " ".join(segments[:17])
                        line = line + " rat:" + rationalities[lemma + "\t" + pos].lower()
                        line = line + " " + segments[19]
                    else:
                        if pos == 'noun':
                            if lemma + "\t" + 'noun_prop' in rationalities:
                                line = " ".join(segments[:17])
                                line = line + " rat:" + rationalities[lemma + "\t" + 'noun_prop'].lower()
                                line = line + " " + segments[19]
                            else:
                                output_check.write(line)
                        else:
                            if lemma + "\t" + 'noun' in rationalities:
                                line = " ".join(segments[:17])
                                line = line + " rat:" + rationalities[lemma + "\t" + 'noun'].lower()
                                line = line + " " + segments[19]
                            else:
                                output_check.write(line)

                elif pos == "adj":
                    line = " ".join(segments[:17])
                    line = line + " rat:" + "n"
                    line = line + " " + segments[19]

                output.write(line)
            line = almor_s31.readline()

        output.write(line)

        while line:
            line = almor_s31.readline()
            output.write(line)

        output_check.close()
        output.close()

    except IOError as err:
        print(err)


def combine_rationality():
    global rationalities
    try:
        annotated_file = open("/Users/dimataji/Google Drive/ My_CAMeL_Files/CALIMA_STAR/AnnotatedTSV/rationalityCombined.txt", 'r')
        for line in annotated_file.readlines():
            segments = line.split("\t")
            pos = segments[0]
            lemma = segments[1]
            rationality = segments[4].upper().strip()
            if rationality != 'I' and rationality != 'R':
                print("Error in line:\n" + line + "\nRationality is not I or R")
            key = lemma + "\t" + pos
            rationalities[key] = rationality

        sara_jamila_file = open("/Users/dimataji/Google Drive/ My_CAMeL_Files/CALIMA_STAR/PATB3-gnr.db", 'r')
        for line in sara_jamila_file.readlines():
            if line.startswith("#"):
                pass
            else:
                segments = line.split("\t")
                lemma = segments[0]
                if "NOUN_PROP" in segments[1]:
                    pos = "noun_prop"
                elif "NOUN" in segments[1]:
                    pos = 'noun'
                rationality = segments[2].rstrip()[-1]
                if pos:
                    key = lemma + "\t" + pos
                    if key not in rationalities:
                        rationalities[key] = rationality

        # check_file = open("check", 'r')
        # for line in check_file.readlines():
        #     segments = line.split(" ")
        #     lemma = re.sub("lex:", "", segments[1])
        #     pos = re.sub("pos:", "", segments[4])
        #     rationality = "R"
        #     rationalities[lemma + "\t" + pos] = rationality

    except IOError as err:
        print(err)


    print()


if __name__ == "__main__":
    ammend_rationality("almor-s31-extended.db")
    ammend_gender_number("almor-s31-extended.db+rat")
    # main("/Users/dimataji/Google Drive/ My_CAMeL_Files/Apps/ALMOR/almor-s31.db")
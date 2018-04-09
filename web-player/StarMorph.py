import sys
import getopt
import StarMorphModules
import os
import pickle
import inspect

def usage():
    '''
    Usage function - prints the usage statement of the main StarMorph function
    required arguments:
        -d database name or database path
            database name is used when the database has already been installed using the dbInsall function,
            i.e. the database already exists in pickle format
        -m the mode in which the main will be run: analyze, generate or reinflect
        -t the type of input that is expected
            stdin is for entering one word/lemma-features/word-features at a time in stdin and outputing the resutls in
                stdin
            file is for running an entire file at once, and outputing the results in a file

    optional arguments:
        -c path to the configurations file
            if the configuration file is not provided, the default values will be assumed
        -i path to the input file
            a required argument in the case of -t file only
        -o path to the output file
            used with -t file only
            if not provided, the system creates an output file with the same name of the input file but with the
                extension .[mode].output, under the same directory
            if a directory is provided instead of a file name, a file with the same name as the input file but with the
                extension .[mode].output, under the given directory
        --verbose
            runs the code in verbose mode - not yet implemented
    :return: Nothing
    '''
    print("usage:\n")
    print("to install database:")
    print("python StarMorph.py --install db_path")
    print("db_path is the path to the database file that will be installed\n")
    print("to run:")
    print("python StarMorph.py -d database -m mode -t type [-c config] [-i input] [-o output] [--verbose]\n")
    print("Mandatory Arguments:")
    print("database: database file name if database has been installed, database path otherwise")
    print("mode: analyze, generate, or reinflect")
    print("type: stdin, file\n")
    print("Optional Arguments:")
    print("config: path to the config file")
    print("input: path to the input file (required for -t file)")
    print("output: path to the output file")


def main():
    '''
    the main function that reads the command line arguments, and assigns the proper values to the variables
    :return: Nothing
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:m:t:i:c:o:", ["verbose", "install="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    database = None
    mode = None
    input_type = None
    input_source = None
    config = None
    output = None
    verbose = False

    for o, a in opts:
        if o == "--verbose":
            verbose = True
        elif o == "-h":
            usage()
            sys.exit()
        elif o == "-d":
            database = a
        elif o == "-m":
            mode = a
        elif o == "-t":
            input_type = a
        elif o == "-i":
            input_source = a
        elif o == "-c":
            config = a
        elif o == "-o":
            output = a
        elif o == "--install":
            install(a)
            sys.exit(0)
        else:
            assert False, "unhandled option " + o

    # mode cannot be None. If None, the usage statement is printed and the session is terminated
    if mode is None:
        print("mode is a manditory argument")
        print("mode is passed using the flag -m\n")
        usage()
        sys.exit(2)

    # input_type cannot be None. If None, the usage statement is printed and the session is terminated
    if input_type is None:
        print("type is a manditory agrument")
        print("type is passed using the flag -t\n")
        usage()
        sys.exit(2)

    # if a config file is given, the read_config function is called
    if config:
        try:
            config_file = open(config, 'r')
            config_file.close()
            StarMorphModules.read_config(config)
        except IOError as err:
            print("Configuration file does not exist! Default values will be assumed for all options.")
            # No need to exit when a config file is not valid. We just inform the user that the default values for all
            # the options will be assumed
            # sys.exit(2)

    print(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, 'bin', database))
    # database cannot be None. If None, the usage statement is printed and the session is terminated
    if database is None:
        print("database is a manditory agrument")
        print("database is passed using the flag -d\n")
        usage()
        sys.exit(2)
    # if the database files do not exist under bin in a directory with the same name as the given database,
    # the database is initialized directly from the file
    # if the database cannot be open, an error message will be given in the initialize_from_file function
    elif not os.path.exists(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, 'bin' , database)):
        StarMorphModules.initialize_from_file(database, mode)
    # if the database pickle files exist under bin in a directory with the same name as the given database,
    # the database is initialized from the pickle files
    else:
        StarMorphModules.initialize_from_hash(database, mode)

    # mode is checked to be analyze, generate, or reinflect
    # otherwise an error is given, and the session is terminated
    if mode in ("analyze", "generate", "reinflect"):
        # type is checked to be stdin, or file
        # otherwise an error is given, and the session is terminated
        if input_type in ("stdin", "file"):
            # ANALYZE MODE
            if mode == "analyze":
                # STDIN
                if input_type == "stdin":
                    # the expected input is one word a time
                    # the session terminates if the user types exit()
                    # exit() doesn't work if the system is stuck at a different stage
                    print("Type exit() to exit.\n")
                    word = input("")
                    # words are read, and analyze_word is called for each word that is read
                    # the output is printed one entry at a time
                    while word != "exit()":
                        try:
                            result = []
                            result = StarMorphModules.analyze_word(word, verbose)
                            for entry in result:
                                print(entry)
                            print()
                            word = input("")
                        except TypeError as err:
                            word = input("")
                # FILE
                else:
                    # if the input type is file, and the input file is not provided, and error is given and the session
                    # is terminated
                    if input_source is None:
                        assert False, "Selection of type 'file' requires path to input file"
                    else:
                        # the output is checked, if no file was given, or only a directory was provided, and path to
                        # an output file is automatically generated
                        # analyze_file is called
                        try:
                            file = open(input_source, 'r')
                            output = check_output(input_source, output, mode)
                            StarMorphModules.analyze_file(file, output, verbose)
                            pass
                        except IOError as err:
                            print(err)
                            sys.exit(2)
            # GENERATE MODE
            elif mode == "generate":
                # STDIN
                if input_type == "stdin":
                    # the expected input is a lemma followed by space separated feature:value pairs
                    # the session terminates if the user types exit()
                    # exit() doesn't work if the system is stuck at a different stage
                    print("Expected input is in the format:")
                    print("lemma feat:value feat:value ... feat:value\n")
                    print("Type exit() to exit.\n")
                    line = input("")
                    # lines are read, segmented, and generate_word is called for each lemma and feature set that is read
                    # the output is printed one entry at a time
                    while line != "exit()":
                        try:
                            segments = line.split(" ")
                            lemma = segments[0]
                            features = ' '.join(segments[1:])
                            result = []
                            result = StarMorphModules.generate_word(lemma, features, verbose)
                            for entry in result:
                                print(entry)
                            print()
                            line = input("")
                        except TypeError as err:
                            line = input("")
                # FILE
                else:
                    # if the input type is file, and the input file is not provided, and error is given and the session
                    # is terminated
                    if input_source is None:
                        assert False, "Selection of type 'file' requires path to input file"
                    else:
                        # the output is checked, if no file was given, or only a directory was provided, and path to
                        # an output file is automatically generated
                        # generate_file is called
                        try:
                            file = open(input_source, 'r')
                            output = check_output(input_source, output, mode)
                            StarMorphModules.generate_file(file, output, verbose)
                            pass
                        except IOError as err:
                            print(err)
                            sys.exit(2)
            # REINFLECT MODE
            else:
                # STDIN
                if input_type == "stdin":
                    # the expected input is a word followed by space separated feature:value pairs
                    # the session terminates if the user types exit()
                    # exit() doesn't work if the system is stuck at a different stage
                    print("Expected input is in the format:")
                    print("word feat:value feat:value ... feat:value\n")
                    print("Type exit() to exit.\n")
                    line = input("")
                    # lines are read, segmented, and reinflect_word is called for each word and feature set that is read
                    # the output is printed one entry at a time
                    while line != "exit()":
                        try:
                            segments = line.split(" ")
                            word = segments[0]
                            features = ' '.join(segments[1:])
                            result = []
                            result = StarMorphModules.reinflect_word(word, features, verbose)
                            for entry in result:
                                print(entry)
                            print()
                            line = input("")
                        except TypeError as err:
                            line = input("")
                # FILE
                else:
                    # if the input type is file, and the input file is not provided, and error is given and the session
                    # is terminated
                    if input_source is None:
                        assert False, "Selection of type 'file' requires path to input file"
                    else:
                        # the output is checked, if no file was given, or only a directory was provided, and path to
                        # an output file is automatically generated
                        # reinflect_file is called
                        try:
                            file = open(input_source, 'r')
                            output = check_output(input_source, output, mode)
                            StarMorphModules.reinflect_file(file, output, verbose)
                            pass
                        except IOError as err:
                            print(err)
                            sys.exit(2)
        else:
            assert False, "Value of 'type' is not valid. Acceptable values are 'stdin', 'file'."
    else:
        assert False, "Value of 'mode' is not valid. Acceptable values are 'analyze', 'generate', or 'reinflect'."


def check_output(input_source, output, mode):
    '''
    If the output file is given the output path stays the same
    If the output path is not given the output path is the same as the path of the input file, with the extension
    .[mode].output
    If the output path is a directory, the output file has the same name as the input file, with the extension
    .[mode].output, and is put in the directory provided in the output path
    :param input_source: the input file that is given with the -i parameter
    :param output: the output file that is given with the -o paramter - may be a directory path, or an empty string
    :param mode: the mode that is given with the -m parameter
    :return: the full path to the output file
    '''
    if output is None:
        output = input_source + os.path.split(inspect.stack()[0][1])[0] + mode + ".output"
    # the structure of the input and output paths is taken into consideration. If paths end with a '/' then a name is
    # directly appended, otherwise, a '/' is appended before the name
    elif os.path.isdir(output):
        if os.sep in input_source:
            if output[-1] == os.sep:
                output = output + os.path.split(input_source)[1] + os.path.split(inspect.stack()[0][1])[0] + mode + ".output"
            else:
                output = output + os.sep + os.path.split(input_source)[1] + os.path.split(inspect.stack()[0][1])[0] + mode + ".output"
        else:
            if output[-1] == os.sep:
                output = output + input_source + os.path.split(inspect.stack()[0][1])[0] + mode + ".output"
            else:
                output = output + os.sep + input_source + os.path.split(inspect.stack()[0][1])[0] + mode + ".output"

    return output


def install(database):
    StarMorphModules.initialize_from_file(database, 'reinflect')
    databaseName = os.path.split(database)[1]

    if not os.path.exists(os.path.join(os.sep, "bin")):
        os.mkdir(os.path.join(os.sep, "bin"))
    if not os.path.exists(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName)):
        os.mkdir(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName))
    pickle.dump(StarMorphModules.define_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName, "define_hash.pk"),
                                                   "wb"))
    pickle.dump(StarMorphModules.default_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "default_hash.pk"),
                                                    "wb"))
    pickle.dump(StarMorphModules.backoff_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "backoff_hash.pk"),
                                                    "wb"))
    pickle.dump(StarMorphModules.prefix_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "prefix_hash.pk"),
                                                   "wb"))
    pickle.dump(StarMorphModules.suffix_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "suffix_hash.pk"),
                                                   "wb"))
    pickle.dump(StarMorphModules.stem_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "stem_hash.pk"),
                                                 "wb"))
    pickle.dump(StarMorphModules.lemma_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "lemma_hash.pk"),
                                                  "wb"))
    pickle.dump(StarMorphModules.prefix_cat_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,
                                                                          "prefix_cat_hash.pk"), "wb"))
    pickle.dump(StarMorphModules.suffix_cat_hash, open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,
                                                                          "suffix_cat_hash.pk"), "wb"))
    pickle.dump(StarMorphModules.stem_prefix_compatibility_hash,
                open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "stem_prefix_compatibility_hash.pk"), "wb"))
    pickle.dump(StarMorphModules.stem_suffix_compatibility_hash,
                open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "stem_suffix_compatibility_hash.pk"), "wb"))
    pickle.dump(StarMorphModules.prefix_stem_compatibility,
                open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "prefix_stem_compatibility.pk"), "wb"))
    pickle.dump(StarMorphModules.stem_suffix_compatibility,
                open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "stem_suffix_compatibility.pk"), "wb"))
    pickle.dump(StarMorphModules.prefix_suffix_compatibility,
                open(os.path.split(inspect.stack()[0][1])[0] + os.path.join(os.sep, "bin", databaseName,  "prefix_suffix_compatibility.pk"), "wb"))


if __name__ == "__main__":
    main()




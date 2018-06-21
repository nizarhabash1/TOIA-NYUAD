# create the almor-s31.pk file

import StarMorphModules
import os
import pickle

def main(database):
    StarMorphModules.initialize_from_file(database, 'reinflect')
    databaseName = database.split("/")[-1]

    if not os.path.exists("bin/"):
        os.mkdir("bin/")
    if not os.path.exists("bin/" + databaseName):
        os.mkdir("bin/" + databaseName)
    pickle.dump(StarMorphModules.define_hash, open("bin/" + databaseName + "/define_hash.pk", "wb"))
    pickle.dump(StarMorphModules.default_hash, open("bin/" + databaseName + "/default_hash.pk", "wb"))
    pickle.dump(StarMorphModules.prefix_hash, open("bin/" + databaseName + "/prefix_hash.pk", "wb"))
    pickle.dump(StarMorphModules.suffix_hash, open("bin/" + databaseName + "/suffix_hash.pk", "wb"))
    pickle.dump(StarMorphModules.stem_hash, open("bin/" + databaseName + "/stem_hash.pk", "wb"))
    pickle.dump(StarMorphModules.lemma_hash, open("bin/" + databaseName + "/lemma_hash.pk", "wb"))
    pickle.dump(StarMorphModules.prefix_cat_hash, open("bin/" + databaseName + "/prefix_cat_hash.pk", "wb"))
    pickle.dump(StarMorphModules.suffix_cat_hash, open("bin/" + databaseName + "/suffix_cat_hash.pk", "wb"))
    pickle.dump(StarMorphModules.stem_prefix_compatibility_hash, open("bin/" + databaseName + "/stem_prefix_compatibility_hash.pk", "wb"))
    pickle.dump(StarMorphModules.stem_suffix_compatibility_hash, open("bin/" + databaseName + "/stem_suffix_compatibility_hash.pk", "wb"))
    pickle.dump(StarMorphModules.prefix_stem_compatibility, open("bin/" + databaseName + "/prefix_stem_compatibility.pk", "wb"))
    pickle.dump(StarMorphModules.stem_suffix_compatibility, open("bin/" + databaseName + "/stem_suffix_compatibility.pk", "wb"))
    pickle.dump(StarMorphModules.prefix_suffix_compatibility, open("bin//" + databaseName + "/prefix_suffix_compatibility.pk", "wb"))
    pass

if __name__ == "__main__":
    main("/Users/dimataji/Google Drive/ My_CAMeL_Files/Apps/ALMOR/almor-s31.db")

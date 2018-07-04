This directory includes the following test files, described below

## test.py

- This is a simple testing program that takes in the following command line arguments:
language: English or Arabic
avatar name: name of avatar you'd like to test
sample file: a .tsv file of the alternative question set you'd like to test the avatar on 
(the exact format of the file is described in test.py)

- This program returns the percentage of correct answers

## test_evaluation.py and test_dm.py

- test_evaluation and test_dm are used to evaluate the different techniques in the dialogue manager. These files can be used to determine which combination of techniques work best in the dialogue manager. te

- test_evaluation depends on test_dm as the dialgue manager it is testing.

- test_evaluation can be used to run different tests with different parameters and it runs those tests on test_dm.

- The comments in the file explain the functionality of different files.



- test_dm:

	test_dm is a dialogue manager which has the same functional capabilities as the dialogue manager.

	test_dm is built such that the techniques of the dialogue manager can be controlled such that they can be turned on and off based on the test parameters.

	test_dm can be used to evaluate the different techniques's effects on the dialogue manager.

	If any changes are made into the dialogue_manager, the corresponding changes will be required in test_dm such that it mirrors the dialogue manager during testing.

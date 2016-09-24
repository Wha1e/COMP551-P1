COMP 551: Applied Machine Learning Project 1 - Predicting the Montreal Marathon
=================================


Dependencies:
----------------------
* Python 3
* numpy, matplotlib, scikit-learn (for basic math operations)

Project Structure:
------------------
* **classes/** - Contains objects that model our dataset. Includes related methods to retrieve information about Runners and Events.
* **data/** - Contains feature representation and labels, as well as the main predictions file for the upcoming 2016 Marathon results. The format of the training_features.csv: Total Races Participated (not excluding Montreal Oasis 2015), Total Oasis Races Participated (excluding Montreal Oasis 2015), and Total Races Participated in 2015 (excluding Montreal Oasis 2015). The format of training_labels.csv are classification variables for 0 == absent, 1 == present at Montreal Oasis 2015.
While, the format for the testing_features.csv features are: Total Races Participated (including Montreal Oasis 2015, if present), Total Oasis Races Participated, and Total Races Participated in 2016.
* **models/** - Contains the important implementations for the three models and cross validation.
* **Project1_files** - Original raw project folder.
* **write_up.pages** - Report about our methodology and analysis.

Usage:
--------------------
Run `python3 get_predictions.py` to generate the `data/predictions.csv` file for Montreal Oasis 2016 results. It will parse the raw data csv file and then create own data objects, which then feed
features to the models, and are then predicted.

Contribute:
------------
We are always for looking for enthusiastic programmers to join our team! :)

Contact:
-------
Tristan Struthers | tristan.struthers@mail.mcgill.ca | 260568567  
Si Hua Zhang      | si.h.zhang@mail.mcgill.ca        | 260583688  
Che-Yuan Liu      | che-yuan.liu@mail.mcgill.ca      | 260523197

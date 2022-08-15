# boiling-pt-prediction

Development & deployment of a machine learning model for predicting boiling points from chemical structures.

**Note**: The `deployment` folder necessarily includes JavaScript from [ChemDoodle Web Components](https://web.chemdoodle.com/), which is distributed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html). All other portions of this repository are original products owned by this author.

## Motivation

A chemical's boiling point (the temperature at which it boils) is useful in a variety of different contexts, from selecting appropriate experimental conditions to characterizing the components of a mixture.

[Gas chromatography](https://en.wikipedia.org/wiki/Gas_chromatography) (GC) is a very common laboratory technique that separates the components of a mixture, primarily by boiling point. Without supplementing it with other techniques (such as mass spectrometry, MS), however, *GC alone cannot provide information about the identity* of a mixture's components -- only the total number of components, their relative ranking in boiling point (low to high), and their relative abundance in the mixture.

![An example gas chromatogram](https://upload.wikimedia.org/wikipedia/commons/f/f2/3_mixtures_of_octane_and_nonane.png)

*An example of annotated GC data for three different mixtures. The x-axis is approximately a surrogate for boiling point. Component names are shown for clarity, but are not provided directly by the GC measurement. Shared by [Wikipedia user Quantumkinetics](https://commons.wikimedia.org/wiki/File:3_mixtures_of_octane_and_nonane.png) under the [Creative Commons Attribution 3.0 license](https://creativecommons.org/licenses/by/3.0/deed.en).*

A GC sample could contain, for example, a desired reaction product (such as a useful pharmaceutical) and an undesired contaminant (such as a toxic byproduct accidentally formed while preparing the valuable drug). We may even know the chemical structure of each molecule, but which component is which in a GC analysis? Answering this question helps us understand: Is this mixture mostly the useful drug, or mostly the toxic byproduct?

**Boiling point data are not available for all possible chemicals.** With new molecules being made every day, there will will *never* be a database of every chemical's boiling point. A reliable tool for predicting unknown boiling points would simplify the interpretation of GC data.

## Purpose

**This project aims to provide a tool for predicting unknown boiling points from a given chemical structure** for organic molecules in the range of 400 - 700 K. The finished predictive tool is deployed at [bp.withjosh.net](https://bp.withjosh.net).


## Repository Contents

This repository is divided into two sections:

* The development of a machine learning model for boiling point prediction, stored within the root of the repository. This includes Jupyter notebooks showing:
    1. `1_data_collection_bp.ipynb`: Collection of boiling point data (8.8k molecules) from a PDF reference textbook. Chemicals are identified by CAS number, which do not convey any structural information.
    1. `2_data_collection_smiles.ipynb`: Collection of a SMILES code for each identifying CAS number. SMILES codes relay chemical structures in plain text.
    1. `3_data_splitting.ipynb`: Splitting the data into training, test, & validation sets.
    1. `4_exploratory_analysis.ipynb`: Exploratory analysis and feature selection, in part using the Python library [RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html).
    1. `5_regression.ipynb`: Training of an XGBoost regression model.

* A Flask-based deployment of the model for prediction of user-drawn models in the `deployment` directory.

## Installation

No installation is necessary in order to view the Jupyter notebooks used in the development of this model.

If you wish to install a copy of the deployed model for generating predictions **or** if you wish to reproduce & extend this analysis, first install the required Python modules listed in `requirements.txt`. Then, clone this repository into a directory of your choice. The web app may be launched by executing `python3 frontend.py` from the `deployment` subdirectory.

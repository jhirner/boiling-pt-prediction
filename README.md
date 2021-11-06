# boiling-pt-prediction
 Development & deployment of a machine learning model for predicting boiling points from chemical structures.
 
 **Note**: The `deployment` folder necessarily includes JavaScript from [ChemDoodle Web Components](https://web.chemdoodle.com/), which is distributed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html). All other portions of this repository are original products owned by this author.
 
 ## Contents
 * Jupyter notebooks used in collecting boiling point data & training an XGBoost model.
 * A Flask-based deployment of the model for prediction of user-drawn models.
 
 ## Installation
 No installation is necessary in order to view the Jupyter notebooks used in the development of this model.
If you wish to install a copy of the deployed model for generating predictions, first install the required Python modules, which are listed in `requirements.txt`. Then, clone this repository into a directory of your choice. The web app may be launched by executing `python3 frontend.py` from the `deployment` subdirectory. 

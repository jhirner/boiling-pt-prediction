# A Flask-based web frontend for boiling point predictions.

# Import the necessary modules and instantiate the app
from flask import Flask, render_template, request
from scripts.predict import Predictor

app = Flask(__name__)

# Define routes
@app.route("/")
def build_search():
    display = render_template("search_form.html")  
    return display

@app.route("/results", methods = ["POST", "GET"])
def display_results():
    
	# This route should be accessed only from the search form at /.
	# If it is accessed directly via GET, provide a link to / instead.
	if request.method == "POST":

		# Capture the user's search parameters
		form_submission = request.form
		raw_smiles = form_submission["raw_smiles_input"]

		# If any query at all is present, try to proceed.
		if raw_smiles != "":
		    
			bp_predictor = Predictor(raw_smiles)
			
			# If the SMILES code is structurally valid, generate a prediction.
			if bp_predictor.smiles_trans.valid_smiles == True:
				
				# Check to make sure only allowable atoms (i.e.: those included
				# in the training set) are present in the user's input).
				allowable_atoms = bp_predictor.check_atoms()
				if allowable_atoms is False:
					message = """The model is currently only trained on molecules containing
						H, C, O, and N. Other heteroatoms are currently outside the scope
						of its predictive capacity."""
					display = render_template("error.html", error_msg = message)
					return display		
				
				
				# Make the prediction
				predicted_bp = bp_predictor.predict()
				
				# Check for any structural features that may give rise to 
				# inaccurate predictions.
				warnings = bp_predictor.check_warnings()
				
				display = render_template("results.html",
						smiles_code = raw_smiles,
						structure_img = "Implementation pending",
						warning_msgs = warnings,
						bp_pred = predicted_bp)
				return display
			
			else:
				message = """The SMILES code you provided could not be interpreted. 
					Please ensure that your SMILES code is valid."""

				display = render_template("error.html", error_msg = message)
				return display

		else:
			# We'll end up here if the raw_smiles_input field was left blank.
			message = """No search query was entered."""

			display = render_template("error.html", error_msg = message)
			return display 
	else:
		# We'll end up here if the access method was not POST.
		message = """You tried to access this page via a GET request, which is unsupported."""
		    
		display = render_template("error.html", error_msg = message)
		return display 

@app.route("/<unspecified_str>")
def handle_unknown(unspecified_str):
    message = """Sorry, but there is nothing at that path."""
    
    display = render_template("error.html", error_msg = message)
    return display

# Run the app
if __name__ == "__main__":
  app.run(debug = True)

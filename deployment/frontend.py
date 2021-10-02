# A Flask-based web frontend for boiling point predictions.

# Import the necessary modules and instantiate the app
from flask import Flask, render_template, request
from scripts.predict import Predictor, pred_dummy

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
			
			if bp_predictor.smiles_trans.valid_smiles == True:
				# If the SMILES code is structurally valid, generate a prediction.
				
				display = render_template("results.html",
						smiles_code = raw_smiles,
						structure_img = "Implementation pending",
						bp_pred = bp_predictor.predict())
				return display
			
			else:
				message = """The SMILES code you provided could not be interpreted. 
					Please ensure that your SMILES code is valid."""

				display = render_template("error.html",
				error_msg = message)
				return display

		else:
			# We'll end up here if the raw_smiles_input field was left blank.
			message = """No search query was entered."""

			display = render_template("error.html",
				error_msg = message)
			return display 
	else:
		# We'll end up here if the access method was not POST.
		message = """You tried to access this page via a GET request, which is unsupported."""
		    
		display = render_template("error.html",
			error_msg = message)
		return display 

@app.route("/<unspecified_str>")
def handle_unknown(unspecified_str):
    message = """Sorry, but there is nothing at that path."""
    
    display = render_template("error.html",
            		error_msg = message)
    return display

# Run the app
if __name__ == "__main__":
  app.run(debug = True)

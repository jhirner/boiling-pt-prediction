from scripts.smilestools import SmilesTransformer
from joblib import load

class Predictor():
	
	def __init__(self, mol_file):
	    self.mol_file = mol_file
	    self.smiles_trans = SmilesTransformer(self.mol_file)
	    self.pred_features = self.smiles_trans.gen_features()
	    
	    
	def predict(self):
	    
	    pred_pipeline = load("model/full_pipe.pkl")
	    pred_array = pred_pipeline.predict(self.pred_features)
	    
	    # Given a single SMILES input, the prediction is a one-item array.
	    # Return the value.
	    self.predicted_bp = round(pred_array[0])
	    return self.predicted_bp
	    
	    
	# This function will check for structural features that may not be
	# accurately predicted by the model.       
	def check_warnings(self):
		# Warnings will take the form of a list of tuples: (warning type, user-friendly warning text)
		self.warnings = []

		if self.smiles_trans.h_bond_donors > 1:
			self.warnings.append(("h_bond_donors",
				                  "Molecules with 2 or more hydrogen bonding donors are not well represented in the training data set; the predicted boiling point is likely artificially low."))

		if self.smiles_trans.mol_wt > 308 or self.smiles_trans.mol_wt < 113:
			self.warnings.append(("mol_wt",
								  "The molecular weight is more than 2 standard deviations from the training data's mean; boiling points are not accurately predicted for molecules of this size. Predictions are most accurate in the molecular weight range of 113 - 308 g/mol."))
			
		if self.smiles_trans.rings_aromatic > 1:
			self.warnings.append(("rings_aromatic",
								  "Molecules with 2 or more aromatic rings are not well represented in the training data set; boiling points are not accurately predicted for polyaromatics."))
			
		if self.predicted_bp < 425:
			self.warnings.append(("pred_bp_low",
								  "The predicted boiling point is near the lower limit of this model's capabilities (400 K, 127 &deg;C)."))
			
		if self.predicted_bp > 675:
			self.warnings.append(("pred_bp_high",
								  "The predicted boiling point is near the upper limit of this model's capabilities (700 K, 427 &deg;C)."))
								  
		return self.warnings
		
		
	def check_atoms(self):
		self.atoms_present = self.smiles_trans.get_atoms()
				
		self.allowable_atoms = True if self.atoms_present.issubset(set(["H", "C", "O", "N"])) else False
		return self.allowable_atoms
		
		

pred_dummy = 2

from scripts.smilestools import SmilesTransformer
from joblib import load

class Predictor():
	
	def __init__(self, smiles_code):
	    self.smiles_code = smiles_code
	    self.smiles_trans = SmilesTransformer(self.smiles_code)
	    self.pred_features = self.smiles_trans.gen_features()
	    print("Found features: ", self.pred_features)
	    
	def predict(self):
	    
	    pred_pipeline = load("model/full_pipe.pkl")
	    pred_array = pred_pipeline.predict(self.pred_features)
	    
	    # Given a single SMILES input, the prediction is a one-item array.
	    # Return the value.
	    return round(pred_array[0])

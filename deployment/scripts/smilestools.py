from rdkit.Chem import Lipinski, Descriptors, MolFromSmiles, MolFromSmarts
import numpy as np

class SmilesTransformer():
    
    def __init__(self, smiles_code):
        
        self.smiles_code = smiles_code

        # Check the validity of the SMILES code before proceeding.
        self.molecule = MolFromSmiles(smiles_code)
        self.valid_smiles = True if self.molecule is not None else False
    
    # Function to calculate fraction of aliphatic carbons that are branch points.
    # Called by the instance's parse_smiles function.
    def calc_branch_frac(self):

        # Use SMARTS substructure codes to count the total number of carbon atoms
        # & the total number of branched aliphatic carbons (i.e.: tertiary or quaternary carbon atoms)
        self.carbon_count = len(self.molecule.GetSubstructMatches(MolFromSmarts("[#6]")))
        self.branch_carbon_count = len(self.molecule.GetSubstructMatches(MolFromSmarts("[$([C;H1,H0]([#6])([#6])([#6]))]")))
   
        # Prevent division by zero.
        if self.carbon_count !=0:
            branch_frac = self.branch_carbon_count / self.carbon_count
        else:
            branch_frac = np.nan
    
        return branch_frac
    
    # This function is responsible for feature generation.
    # It calls calc_branch_frac as needed.
    def gen_features(self):
        
        # If the SMILES code was properly interpreted, compute the descriptors of interest.
        # If not, return an array of zeroes instead.
        # (Note: Because frontend.py only generates predictions after valid_smiles
        # is confirmed True, this if statement should never actually be false.)
        if self.valid_smiles:
        
            # Invoke the function for SMARTS-based substructure searching
            self.branching_frac = self.calc_branch_frac()
            
            # Determine other features.
            self.h_bond_donors = Lipinski.NumHDonors(self.molecule)
            self.mol_wt = Descriptors.ExactMolWt(self.molecule)
            self.rings_aromatic = Lipinski.NumAromaticRings(self.molecule)

            # Compile the prediction features as a tuple, then convert to array.
            pred_tup = (self.branching_frac, self.h_bond_donors, self.mol_wt, self.rings_aromatic)
            pred_array = np.ascontiguousarray(pred_tup)
            pred_array = pred_array.reshape((1, -1))
            

            # Returned the transformed data as a numpy array.
            return pred_array
        
        else:
            return np.zeros((1,4))
            
    # This function generates a list of unique atomic numbers present in the molecule.
    # It is used for validation purposes by frontend.py via predict.py to ensure that
    # only atoms included in the training set are present in the user-inputted structure.
    def get_atoms(self):
    	atom_list = []
    	
    	for atom in self.molecule.GetAtoms():
    		atom_list.append(atom.GetSymbol())
    	
    	return set(atom_list)

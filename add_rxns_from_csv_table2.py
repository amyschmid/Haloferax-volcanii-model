import cobra
import sys
import csv

model_in_name = sys.argv[1]
model_out_name = sys.argv[2]
reaction_csv_name = sys.argv[3]

FBA_model = cobra.io.read_sbml_model(model_in_name)
with open(reaction_csv_name,'r') as csvfile:
	rxn_reader = csv.reader(csvfile, dialect='excel')
	row = next(rxn_reader)
	while True:
		if row[0].startswith('rxn'):
			left_dict = {}
			right_dict = {}
			rxn_id = row[0]
			rxn_name = row[1]
			gene = row[2]
			met_id_row = next(rxn_reader)
			leftside = True
			for col in range(3,len(row)):
				if row[col] == '"=>"':
					dir_coeff = 1
					leftside = False
					reversible = False
				elif row[col] == '"<="':
					dir_coeff = -1
					leftside = False
					reversible = False
				elif row[col] == '"<=>"':
					dir_coeff = 1
					leftside = False
					reversible = True
				elif not row[col] == '':
					coeff_and_name = row[col].split(' ')
					try:
						coeff = int(coeff_and_name[0])
						met_name = ' '.join(coeff_and_name[1:])
					except:
						coeff = 1
						met_name = row[col]
					met_id = met_id_row[col]
					if met_id.endswith('_e0'):
						comp = 'e0'
					elif met_id.endswith('_c0'):
						comp = 'c0'
					else:
						comp = 'c0'
						met_id = met_id + '_c0'
					if met_id in FBA_model.metabolites:
						met = FBA_model.metabolites.get_by_id(met_id)
					else:
						met = cobra.Metabolite(met_id, name=met_name, compartment=comp)
					if leftside:
						left_dict[met] = -1*coeff
					else:
						right_dict[met] = dir_coeff*coeff
			if dir_coeff == -1:
				for key,val in left_dict.items():
					left_dict[key] = -1*val
			if not rxn_name == '':
				new_rxn = cobra.Reaction(rxn_id, name=rxn_name)
			else:
				new_rxn = cobra.Reaction(rxn_id)
			if reversible:
				new_rxn.lower_bound = -1*new_rxn.upper_bound
			FBA_model.add_reaction(new_rxn)
			new_rxn.add_metabolites(left_dict)
			new_rxn.add_metabolites(right_dict)
			if not gene == '':
				new_rxn.gene_reaction_rule = gene
			print(new_rxn.build_reaction_string(use_metabolite_names = True))
		try:
			row = next(rxn_reader)
		except:
			break
cobra.io.write_sbml_model(FBA_model,model_out_name)		

			
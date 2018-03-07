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
			react_dict = {}
			rxn_id = row[0]
			rxn_name = row[1]
			gene = row[2]
			met_id_row = next(rxn_reader)
			coeff_row = next(rxn_reader)
			leftside = True
			for col in range(3,len(row)):
				if not row[col] == '':
					met_id = met_id_row[col]
					coeff = float(coeff_row[col])
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
						met_name = row[col]
						met = cobra.Metabolite(met_id, name=met_name, compartment=comp)
					react_dict[met] = coeff
			if not rxn_name == '':
				new_rxn = cobra.Reaction(rxn_id, name=rxn_name)
			else:
				new_rxn = cobra.Reaction(rxn_id)
			FBA_model.add_reaction(new_rxn)
			new_rxn.add_metabolites(react_dict)
			if not gene == '':
				new_rxn.gene_reaction_rule = gene
			print(new_rxn.build_reaction_string(use_metabolite_names = True))
		try:
			row = next(rxn_reader)
		except:
			break
cobra.io.write_sbml_model(FBA_model,model_out_name)		

			
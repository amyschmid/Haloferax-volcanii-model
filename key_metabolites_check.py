import cobra
import sys

FBA_model = cobra.io.read_sbml_model(sys.argv[1])
# call as "python FBA_health_check.py model_to_test.sbml"

##growth medium
##glucose, ammonia, O2, PO4, sulfate, K, Ca, Mg2+, Fe2+, Co2+, Zn2+, H+, H2O
med_components = ['cpd00190_e0','cpd00013_e0','cpd00007_e0','cpd00009_e0','cpd00048_e0','cpd00205_e0','cpd00063_e0','cpd00254_e0','cpd10515_e0','cpd00149_e0','cpd00034_e0','cpd00067_e0','cpd00001_e0']
med = {}

def try_as_biomass(react_dict):
## note that reaction dictionary is opposite from desired metabolic reaction (things that are produced have negative coefficients)
## this is necessary for the solver to be stable--setting a coeff of -1 in model.objective gives buggy behavior
	test_biomass = FBA_model.reactions.get_by_id('test_biomass')
	biomass = FBA_model.metabolites.get_by_id('cpd11416_c0')
	react_dict[biomass] = 1
	old_mets = test_biomass.metabolites
	test_biomass.subtract_metabolites(old_mets)
	test_biomass.add_metabolites(react_dict)
	FBA_model.objective = {FBA_model.reactions.test_biomass: 1}

	FBA_model.solver = 'glpk'
	solution = FBA_model.optimize()
	if solution.f > 0.0001:
		return 'Success!'
	else:
		return 'Failed :-('

for component in med_components:
	try:
		met = FBA_model.metabolites.get_by_id(component)
	except:
		print('model to be filled has no ' + component + ': Adding it!')
		met = cobra.Metabolite(component)
	try:
		exchange = FBA_model.reactions.get_by_id('EX_' + component)
	except:
		exchange = FBA_model.add_boundary(met)
		print('new exchange reaction added: EX_' + component)
	exch_id = exchange.id
	med[exch_id] = 300
		
FBA_model.medium = med

##add a proton leak so we don't need to worry about charge balance for each individual metabolite to be checked
##this is NEVER (and should not be) saved back into the SBML file!!
H_extra = FBA_model.metabolites.get_by_id('cpd00067_e0')
H_intra = FBA_model.metabolites.get_by_id('cpd00067_c0')
H_transport = cobra.Reaction('proton_leak')
H_transport.add_metabolites({H_extra: -1, H_intra: 1})
H_transport.lower_bound = -1000
H_transport.upper_bound = 1000
FBA_model.add_reaction(H_transport)

test_biomass = cobra.Reaction('test_biomass')
FBA_model.add_reaction(test_biomass)

print('\n')
print('Checking central carbon metabolism...')
test_dict = {'cpd00020_c0': -1}
print('Trying to make pyruvate: ' + try_as_biomass(test_dict))
test_dict = {'cpd00022_c0': -1,'cpd00010_c0': 1}
print('Trying to make acetyl-CoA: ' + try_as_biomass(test_dict))
test_dict = {'cpd00137_c0': -1}
print('Trying to make citrate: ' + try_as_biomass(test_dict))
test_dict = {'cpd00024_c0': -1}
print('Trying to make alpha-ketoglutarate: ' + try_as_biomass(test_dict))
test_dict = {'cpd00236_c0': -1}
print('Trying to make erythrose-4P: ' + try_as_biomass(test_dict))
test_dict = {'cpd00105_c0': -1}
print('Trying to make ribose: ' + try_as_biomass(test_dict))
print('\n')
print('Checking redox balance...')
test_dict = {'cpd00003_c0': 1, 'cpd00004_c0': -1}
print('Trying to make reducing equivalents... NADH: ' + try_as_biomass(test_dict))
test_dict = {'cpd00006_c0': 1, 'cpd00005_c0': -1}
print('Trying to make reducing equivalents... NADPH: ' + try_as_biomass(test_dict))
test_dict = {'cpd00111_c0': 1, 'cpd00042_c0': -1}
print('Trying to make reducing equivalents... glutathione: ' + try_as_biomass(test_dict))
print('\n')
print('Checking amino acid biosynthesis...')
test_dict = {'cpd00032_c0': -1}
print('Trying to make glutamate: ' + try_as_biomass(test_dict))
test_dict = {'cpd00053_c0': -1}
print('Trying to make glutamine: ' + try_as_biomass(test_dict))
test_dict = {'cpd00054_c0': -1}
print('Trying to make serine: ' + try_as_biomass(test_dict))
test_dict = {'cpd00033_c0': -1}
print('Trying to make glycine: ' + try_as_biomass(test_dict))
test_dict = {'cpd00051_c0': -1}
print('Trying to make arginine: ' + try_as_biomass(test_dict))
test_dict = {'cpd00032_c0': -1}
print('Trying to make histidine: ' + try_as_biomass(test_dict))
test_dict = {'cpd00107_c0': -1}
print('Trying an example BCAA--leucine: ' + try_as_biomass(test_dict))
test_dict = {'cpd00066_c0': -1}
print('Trying an example aromatic AA--phenylalanine: ' + try_as_biomass(test_dict))
test_dict = {'cpd00084_c0': -1}
print('Trying an example sulfur AA--cysteine: ' + try_as_biomass(test_dict))
print('\n')
print('Checking de novo nucleotide biosynthesis...')
test_dict = {'cpd00002_c0': -1}
print('Trying to make ATP (de novo): ' + try_as_biomass(test_dict))
test_dict = {'cpd00038_c0': -1}
print('Trying to make GTP (de novo): ' + try_as_biomass(test_dict))
test_dict = {'cpd00052_c0': -1}
print('Trying to make CTP (de novo): ' + try_as_biomass(test_dict))
test_dict = {'cpd00062_c0': -1}
print('Trying to make UTP (de novo): ' + try_as_biomass(test_dict))
test_dict = {'cpd00357_c0': -1}
print('Trying to make dTTP (de novo): ' + try_as_biomass(test_dict))
test_dict = {'cpd00003_c0': -1}
print('Trying to make NAD (de novo): ' + try_as_biomass(test_dict))
test_dict = {'cpd00006_c0': -1}
print('Trying to make NADP (de novo): ' + try_as_biomass(test_dict))
print('\n')
print('Checking coenzyme biosynthesis...')
test_dict = {'cpd00016_c0': -1}
print('Trying to make PLP: ' + try_as_biomass(test_dict))
test_dict = {'cpd00056_c0': -1}
print('Trying to make TPP: ' + try_as_biomass(test_dict))
test_dict = {'cpd00104_c0': -1}
print('Trying to make biotin: ' + try_as_biomass(test_dict))
test_dict = {'cpd00050_c0': -1}
print('Trying to make FMN: ' + try_as_biomass(test_dict))
test_dict = {'cpd00028_c0': -1}
print('Trying to make heme: ' + try_as_biomass(test_dict))
test_dict = {'cpd03424_c0': -1}
print('Trying to make adenosylcobalamin(B12): ' + try_as_biomass(test_dict))
test_dict = {'cpd00338_c0': -1}
print('Trying to make ALA: ' + try_as_biomass(test_dict))
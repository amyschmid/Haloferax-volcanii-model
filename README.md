# Haloferax-volcanii-model
Flux balance analysis model of the archaeon Haloferax volcanii

Files List:
------------
"key_metabolites_check.py": A script that checks a FBA model for its ability to produce essential metabolites, given the components of the medium defined by the list of compound IDs given in "med_components" (Line 9). Aside from the lipids, which are archaea-specific, should be useful for any cell. Run from command line as "python key_metabolites_check.py FBA_model_SBML_file.sbml".

"add_rxns_from_csv_table.py": For adding reactions to a FBA model in batch, from a CSV file. Mostly obsolete, as this does NOT write anything in the "name" and "gene reaction rule" fields of the model, and does not set reaction reversibility automatically. Included only because it was used to add the auto-gap-filled reactions to the model at the beginning of the project. The newer version "add_reactions_from_csv_table2.py" should be used instead. Run in exactly the same manner as the newer file (see below).

"add_rxns_from_csv_table2.py": For adding reations to a FBA model in batch, from a CSV file. The format is described in "reaction_CSV_format_notes". Run from the command line as "python add_rxns_from_csv_table2.py old_model.sbml updated_model.sbml rxn_table.csv".

"add_rxn_table_with_coeffs_below.py": Similar to the preceding file, except rather than stoichiometric coefficients being placed to the left of the metabolite names in the CSV cells, they are placed in a separate row below the metabolite IDs. This makes it easier to use arbitrary, non-integer coefficients, as often appear in biomass reactions. Run from the command line as "python add_rxn_table_with_coeffs_below.py old_model.sbml updated_model.sbml rxn_table.csv".

"Change biomass reaction to Halobacterium.ipynb": A Jupyter notebook that shows the original biomass equation from the ModelSEED model being removed and the biomass reaction from the Gonzalez et. al. paper being added (after the sub-reactions were already added with the above file, with the reactions listed in "biomass_from_Gonzalez.csv".

"Model curation and testing.ipynb": A Jupyter notebook in which everything was done AFTER the biomass equation was replaced. This is everything in the "Model curation" and "Testing and analysis" sections in the Methods.

"gapfill_added.csv": A reaction table containing the 31 reactions automatically suggested my ModelSEED. In format to be added using the script "add_rxns_from_csv_table.py".

"Heme_enzyme_rxns.csv", "B12_missing_reactions_table.csv", "Lipid_enzymes_table.csv", and "final_missing_rxns.csv": Batches of reactions that were added to the model, in this order. In format to be added using the script "add_rxns_from_csv_table.py".

"biomass_from_Gonzalez.csv": The biomass sub-reactions from the Gonzalez et. al. Halobacterium model. In a format to be added using the script "add_rxn_table_with_coeffs_below.py".

"reaction_CSV_format_notes.txt": Description of the CSV file format for adding reactions.

"H_volcanii_curated.sbml": The final curated FBA model.

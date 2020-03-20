from modeller import *
from modeller.automodel import *

env = environ()
# ReDo the alignment that implemented by Modeller
aln = alignment(env)
mdl = model(env, file='2a31', model_segment=('FIRST:A', 'LAST:A'))
aln.append_model(mdl, align_codes='2a31A', atom_files='2a31.pdb')
aln.append(file='TMPRSS2_254.ali', align_codes='TMPRSS2_254')
aln.align2d()
aln.write(file='TMPRSS2_254_2a31A.ali', alignment_format='PIR')
# Start modelling
a = automodel(env, alnfile='TMPRSS2_254_2a31A.ali',
              knowns='2a31A', sequence='TMPRSS2_254',
              assess_methods=(assess.DOPE, assess.GA341))
a.starting_model = 1
a.ending_model = 3
a.make()

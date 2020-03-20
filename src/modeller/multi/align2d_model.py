from modeller.automodel import *
from modeller import *

log.verbose()
env = environ()

env.libs.topology.read(file='$(LIB)/top_heav.lib')

# Read aligned structure(s):
aln = alignment(env)
aln.append(file='fm_0320.ali', align_codes='all')
aln_block = len(aln)

# Read aligned sequence(s):
aln.append(file='TMPRSS2_254.ali', align_codes='TMPRSS2_254')

# Structure sensitive variable gap penalty sequence-sequence alignment:
aln.salign(output='', max_gap_length=20,
           gap_function=True,   # to use structure-dependent gap penalty
           alignment_type='PAIRWISE', align_block=aln_block,
           feature_weights=(1., 0., 0., 0., 0., 0.), overhang=0,
           gap_penalties_1d=(-450, 0),
           gap_penalties_2d=(0.35, 1.2, 0.9, 1.2, 0.6, 8.6, 1.2, 0., 0.),
           similarity_flag=True)

aln.write(file='TMPRSS2_254-mult.ali', alignment_format='PIR')

a = automodel(env, alnfile='TMPRSS2_254-mult.ali',
              knowns=('2a31A', '1a7sA', '5abwA'), sequence='TMPRSS2_254')
a.starting_model = 1
a.ending_model = 3
a.make()

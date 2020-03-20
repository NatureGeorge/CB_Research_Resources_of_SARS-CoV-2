import modeller
import matplotlib.pyplot as plt
from modeller import *
from modeller.scripts import complete_pdb

pdb_lyst = ('2a31', '1a7s', '5abw', 'TMPRSS2_254_multi.B99990001',
            'TMPRSS2_254_multi.B99990002', 'TMPRSS2_254_multi.B99990003')

log.verbose()    # request verbose output
env = environ()
env.libs.topology.read(file='$(LIB)/top_heav.lib')  # read topology
env.libs.parameters.read(file='$(LIB)/par.lib')  # read parameters

for fileName in pdb_lyst:
    # read model file
    mdl = complete_pdb(env, fileName+'.pdb')
    # Assess with DOPE:
    s = selection(mdl)   # all atom selection
    s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file=fileName+'.profile',
                  normalize_profile=True, smoothing_window=15)


def r_enumerate(seq):
    """Enumerate a sequence in reverse order"""
    # Note that we don't use reversed() since Python 2.3 doesn't have it
    num = len(seq) - 1
    while num >= 0:
        yield num, seq[num]
        num -= 1


def get_profile(profile_file, seq):
    """Read `profile_file` into a Python array, and add gaps corresponding to
       the alignment sequence `seq`."""
    # Read all non-comment and non-blank lines from the file:
    f = open(profile_file)
    vals = []
    for line in f:
        if not line.startswith('#') and len(line) > 10:
            spl = line.split()
            vals.append(float(spl[-1]))
    # Insert gaps into the profile corresponding to those in seq:
    for n, res in r_enumerate(seq.residues):
        for gap in range(res.get_leading_gaps()):
            vals.insert(n, None)
    # Add a gap at position '0', so that we effectively count from 1:
    vals.insert(0, None)
    return vals


a = modeller.alignment(env, file='TMPRSS2_254-mult.ali')

plt.figure(1, figsize=(10, 6))
plt.xlabel('Alignment position')
plt.ylabel('DOPE per-residue score')
for fileName in pdb_lyst[:3]:
    model = get_profile(fileName+'.profile', a[fileName+'A'])
    plt.plot(model, linewidth=2, label=fileName)
for fileName in pdb_lyst[3:]:
    model = get_profile(fileName+'.profile', a['TMPRSS2_254'])
    plt.plot(model, linewidth=2, label=fileName)
plt.legend()
plt.savefig('dope_profile_TMPRSS2_254_multi.png', dpi=100)

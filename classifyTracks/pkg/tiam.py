import argparse

actions = ['get_features',
	   'train',
	   'classify',
	   'visualize',
	   'stability_index',
	   'save_mat']

parser = argparse.ArgumentParser(description='T-cell motility classifier')
parser.add_argument('action', type=str, help=', '.join(actions))
parser.add_argument('-L','--labeled', metavar='',
                    help='whether data has supervised state labels. Assumed to be true for action=train',
                    action='store_const',const=True)
args = parser.parse_args()

if args.action not in actions:
    raise NameError('Invalid action. Run `python tiam.py -h` for more info.')

from TIAM.features import *
from TIAM.analysis import *

# because all the function in the features and analysis namespace are
# global to this script, the following line executes the function
exec '{0}(labeled={1})'.format(args.action,args.labeled)

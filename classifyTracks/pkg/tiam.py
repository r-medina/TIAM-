import argparse

actions = ['get_features',
	   'train',
	   'classify',
	   'test',
	   'plot',
	   'stability_index',
	   'save_mat']

parser = argparse.ArgumentParser(description='T-cell motility classifier')
parser.add_argument('action', type=str, help=', '.join(actions))
parser.add_argument('-T','--training', metavar='', help='whether data is training data', action='store_const',const=True)
args = parser.parse_args()

from TIAM import features, analysis

if args.action not in actions:
    raise Exception('Invalid action. Please specify either {0}, or {1}'.format(', '.join(actions[0:-1]),actions[-1]))

try:
    exec 'analysis.{0}()'.format(args.action)
except:
    exec 'features.{0}()'.format(args.action)


import argparse

from TIAM import features, analysis


parser = argparse.ArgumentParser(description='T-cell motility classifier')
parser.add_argument('action', type=str, help='get_features, train, classify, test, plot, stability_index')
parser.add_argument('-T','--training', metavar='', help='whether data is training data')
args = parser.parse_args()

if args.action not in ['get_features','train', 'test', 'classify', 'plot', 'stability_index']:
    raise Exception('Invalid action. Please specify either get_freatures, train, test, classify, plot, or stability_index')

if args.action == 'get_features':
    features.get_features()
if args.action == 'train':
    analysis.train()
if args.action == 'plot':
    analysis.plot()
if args.action == 'stability_index':
    analysis.stability_index()

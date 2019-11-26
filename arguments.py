import argparse
import os
import glob

from maopy.gossip_comm import GossipComm


def get_args():
    parser = argparse.ArgumentParser(description='maopy')

    parser.add_argument(
        '--user-name',
        type=str,
        default='massran',
        help='user-name to define log-file directories')
    parser.add_argument(
        '--data-file-name',
        type=str,
        default='qp_data_sg.npz',
        help='name of dataset to load from ./datasets/')
    parser.add_argument(
        '--graph-file-name',
        type=str,
        default='erdos-renyi_n2.npz',
        help='name of graph to load from ./graphs/')
    parser.add_argument(
        '--alg',
        default='gp',
        help='algorithm to use: gp | pd | ep | asy-sonata')
    parser.add_argument(
        '--asynch',
        action='store_true',
        default=False,
        help='whether to run algorithm asynchronously')
    parser.add_argument(
        '--lr',
        type=float,
        default=0.1,
        help='learning rate (default: 0.1)')
    parser.add_argument(
        '--tau',
        type=int,
        default=32,
        help='maximum processing delay (default: 32)')
    parser.add_argument(
        '--seed',
        type=int,
        default=1,
        help='random seed (default: 1)')
    parser.add_argument(
        '--num-steps',
        type=int,
        default=1000,
        help='number of optimization steps (default: 1000)')
    parser.add_argument(
        '--log-dir',
        default='/tmp/maopy/',
        help='directory to save agent logs (default: /tmp/maopy)')
    parser.add_argument(
        '--use-lr-decay',
        action='store_true',
        default=False,
        help='use a linear schedule on the learning rate')
    parser.add_argument(
        '--experiment',
        type=str,
        default='least-squares',
        help='whether to use "least-squares" or "softmax" objective')
    args = parser.parse_args()

    # Only these algorithms currently supported
    assert args.alg in ['gp', 'pd', 'ep', 'asy-sonata']

    # Only these two objectives functions currently defined in utils
    assert ('least_squares' in args.experiment) \
        or ('softmax' in args.experiment)

    # Message passing and network variables
    args.size = GossipComm.size
    args.rank = GossipComm.uid
    args.name = GossipComm.name
    args.comm = GossipComm.comm

    # Make logging directory
    args.log_dir = '/checkpoint/' + args.user_name + args.log_dir
    args.fpath = args.log_dir + 'r%s_n%s.npz' % (args.rank, args.size)
    try:
        os.makedirs(args.log_dir)
    except OSError:
        files = glob.glob(os.path.join(args.log_dir, '*.npz'))
        for f in files:
            try:
                os.remove(f)
            except Exception:
                pass
    return args

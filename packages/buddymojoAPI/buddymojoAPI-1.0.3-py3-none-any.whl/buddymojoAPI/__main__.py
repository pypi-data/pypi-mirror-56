import argparse
import buddymojo.buddymojoAPI as b
import multiprocessing as mp
from math import floor

api = b.BuddyAPI()

parser = argparse.ArgumentParser(
    description='Version 1.0.0 By squarejellyfish, An API of buddymojo.com, can spam 10/10 message to specific user(s)',
    usage='-s -T [targetID] -t [times] -n [name] [-l] (will show the page url) \n -m -r [start] [end] -n [name]')
parser.add_argument('-s', '--single', action='store_true',
                    help='Single target mode')
parser.add_argument('-m', '--multiple',
                    action='store_true', help='Multiple target mode')
parser.add_argument('-L', '--getLink', type=int, required=False,
                    help='Simply get the link page of that user, not sending any message')
optx, unknown = parser.parse_known_args()
if optx.getLink:
    print(api.get_link(optx.getLink))
if optx.single:
    parser.add_argument('-T', '--target', type=int, metavar='', required=True,
                        help='Target user quiz ID (number), when single mode')
    parser.add_argument('-t', '--times', type=int, metavar='', required=False,
                        default=1, help='Amount of spam messages, default is 1')
    parser.add_argument('-l', '--link', action='store_true',
                        required=False, help='Returns the link of that user')
    parser.add_argument('-n', '--name', type=str, metavar='',
                        required=False, default='Sent By API', help='Name of the message')
    args = parser.parse_args(unknown, namespace=optx)

    for i in range(args.times):
        api.send_single_ans(args.target, args.name)

    if args.link:
        print(api.get_link(args.target))
if optx.multiple:
    parser.add_argument('-r', '--range', nargs='+', type=int, required=True,
                        help='Range of the users\nusage: -r [StartUserID] [EndUserID]')
    parser.add_argument('-n', '--name', type=str, metavar='',
                        required=True, help='Name of the message')
    args = parser.parse_args(unknown, namespace=optx)

    pool = mp.Pool(4)
    a = args.range[0]
    b = args.range[0]
    offset = floor((args.range[1] - args.range[0]) / 4)
    for i in range(1, 5):
        pool.apply_async(api.send_range_ans,
                         (a, b + i * offset, args.name))
        a += offset

    pool.close()
    pool.join()

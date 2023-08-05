import requests
import json
import multiprocessing as mp
import argparse
from math import floor


class BuddyAPI():
    '''
    An API of buddymojo.com 

    :returns: An API 
    '''

    def __init__(self):
        self.payload = {'type': 'friend',
                        'action': 'finish'}
        self.payloadf = {'userQuizId': 1,
                         'type': 'friend',
                         'stats': '1'}

        self.url = 'https://cn.buddymojo.com/api/v1/quiz/18'
        self.match = 'https://cn.buddymojo.com/match/'

    def send_single_ans(self, ID, name: str):
        '''
        Send a single message to specific id with a specific name.

        :params ID: User quiz id.
        :type ID: int
        :params name: Name you want on the message.
        :type name: str
        '''
        self.data = {'userFullName': name,
                     'userQuizId': 1}
        self.data.update(userQuizId=ID)
        self.payloadf.update(userQuizId=ID)

        try:
            req = requests.request('GET', self.url, params=self.payloadf)
            questions = json.loads(req.text).get('data').get('questions')
            # d = text.get('data')
            # questions = d.get('questions')

            for j, q in enumerate(questions):
                qval = q.get('choosenOption')
                self.data.update(
                    {'questions['+str(j)+'][choosenOption]': qval})

            reqi = requests.post(self.url, params=self.payload, data=self.data)
            print('sending post to userQuizId: '+str(a))
        except:
            print('User not found')

    def send_range_ans(self, start, end, name: str):
        '''
        Send messages to a range of users id.

        :params start: The start user id.
        :type start: int
        :params end: The end user id.
        :type end: int
        :params name: The name you want.
        :type name: str
        '''
        for i in range(start, end):
            data = {'userFullName': name,
                    'userQuizId': 1}
            data.update(userQuizId=i)
            self.payloadf.update(userQuizId=i)

            try:
                req = requests.request('GET', self.url, params=self.payloadf)
                questions = json.loads(req.text).get('data').get('questions')
                # d = text.get('data')
                # questions = d.get('questions')

                for j, q in enumerate(questions):
                    qval = q.get('choosenOption')
                    data.update({'questions['+str(j)+'][choosenOption]': qval})

                reqi = requests.post(self.url, params=self.payload, data=data)
                print('sending post to userQuizId: '+str(i))
            except:
                continue

    # Still working out
    def get_userQuizId(self, encUserQuizId):
        '''
        Returns a user id string of the encUserQuizId.
        '''
        try:
            req = requests.request('GET', str(match+encUserQuizId))
            data = json.loads(req.text)
            print(data)
        except:
            return 'User not found'

    def get_link(self, ID):
        '''
        Returns a url string of the id.

        :params ID: The id to get the url from.
        :type ID: int
        :returns: A url string.
        :rtype: String
        '''
        self.payloadf.update(userQuizId=ID)

        try:
            req = requests.request('GET', self.url, params=self.payloadf)
            data = json.loads(req.text).get('data').get('encUserQuizId')

            return self.match + data
        except:
            return 'User not found'


if __name__ == "__main__":
    api = BuddyAPI()

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

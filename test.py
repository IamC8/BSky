import logging
import time
from atproto import Client, exceptions


class MakeDict:
    @staticmethod
    def getAttr(attr):
        return dict((name, getattr(attr, name)) for name in dir(attr) if not name.startswith('_'))


class BSkyInfo:
    def __init__(self, _data: list):
        self.logging = logging
        self.clientB = Client()
        self.info = _data

    @staticmethod
    def display(_p, _i):
        if _p is not None and _i is not None:
            try:
                pro_dict = MakeDict().getAttr(_p)
                inv_dict = MakeDict().getAttr(_i)
                for pr in pro_dict:
                    if pr != 'viewer':
                        print('%s: %s' % (pr, pro_dict[pr]))
                vs_dict = MakeDict().getAttr(pro_dict['viewer'])
                print('ViewerState:')
                for vs in vs_dict:
                    print('  %s: %s' % (vs, vs_dict[vs]))
                print('InviteCodes:')
                for InviteCode in inv_dict['codes']:
                    ic_dict = MakeDict().getAttr(InviteCode)
                    for ic in ic_dict:
                        if ic != 'uses':
                            print('  %s: %s' % (ic, ic_dict[ic]))
                    for InviteCodeUse in ic_dict['uses']:
                        icu_dict = MakeDict().getAttr(InviteCodeUse)
                        for icu in icu_dict:
                            print('    %s: %s' % (icu, icu_dict[icu]))
            except Exception as err:
                logging.error(err)
            print('\n')

    def login(self):
        for info in self.info:
            profile = None
            invites = None
            while True:
                try:
                    print(':: %s ::' % info['handle'])
                    profile = self.clientB.login(info['handle'], info['password'])
                    invites = self.clientB.com.atproto.server.get_account_invite_codes()
                    break
                except exceptions.RequestException as req:
                    logging.error('RequestException Timeout for 300s: %s' % info['handle'])
                    logging.error(req)
                    time.sleep(300)
                except exceptions.BadRequestError as bre:
                    logging.error('BadRequestError:: %s' % info['handle'])
                    break
                except exceptions.UnauthorizedError as une:
                    logging.error('UnauthorizedError:: %s' % info['handle'])
                    break
                except exceptions.InvokeTimeoutError as ite:
                    logging.error('InvokeTimeoutError Timeout for 120s: %s' % info['handle'])
                    logging.error(ite)
                    time.sleep(120)
            self.display(profile, invites)


if __name__ == '__main__':
    data = [{'handle': 'abcde.bsky.social', 'password': 'PassWord'},
            {'handle': 'fghij.bsky.social', 'password': 'PassWord'},
            {'handle': 'klmnopq.bsky.social', 'password': 'PassWord'}
            ]

    b = BSkyInfo(data)
    b.login()

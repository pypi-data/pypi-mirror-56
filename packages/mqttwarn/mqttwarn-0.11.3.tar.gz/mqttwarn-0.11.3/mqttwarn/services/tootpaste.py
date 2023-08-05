#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__    = 'Jan-Piet Mens <jpmens()gmail.com>'
__copyright__ = 'Copyright 2017 Jan-Piet Mens'
__license__   = """Eclipse Public License - v 1.0 (http://www.eclipse.org/legal/epl-v10.html)"""

HAVE_MASTODON=True
try:
    from mastodon import Mastodon
except ImportError:
    HAVE_MASTODON=False
import os
import sys

def plugin(srv, item):

    _DEFAULT_URL = 'https://mastodon.social'

    srv.logging.debug("*** MODULE=%s: service=%s, target=%s", __file__, item.service, item.target)

    if not HAVE_MASTODON:
        srv.logging.error("Python Mastodon.py is not installed")
        return False

    # item.config is brought in from the configuration file
    config   = item.config

    clientcreds, usercreds, base_url = item.addrs

    text = item.message

    try:
        mastodon = Mastodon(
            client_id = clientcreds,
            access_token = usercreds,
            api_base_url = base_url
        )

        mastodon.toot(text)
    except Exception, e:
        srv.logging.warning("Cannot post to Mastodon: %s" % (str(e)))
        return False

    return True

if __name__ == '__main__':
    from mastodon import Mastodon

    try:
        base_url, email, password, clientname, clientcred, usercred = sys.argv[1:]
    except:
        print("Usage: %s base_url email password clientname clientcredsfile usercredsfile" % sys.argv[0])
        sys.exit(2)

    if not os.path.isfile(clientcred):
        Mastodon.create_app(
            clientname,
            to_file = clientcred,
            scopes = [ 'read', 'write' ],
            api_base_url = base_url)

    if not os.path.isfile(usercred):
        mastodon_api = Mastodon(
            client_id = clientcred,
            api_base_url = base_url)

        mastodon_api.log_in(
            email,
            password,
            to_file = usercred,
            scopes = [ 'read', 'write' ],
            )


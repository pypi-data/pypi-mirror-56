#!/opt/privacyidea/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Cornelius Kölbel
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from this
# software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from privacyidea.app import create_app
from flask_script import Manager
import requests
from privacyidea.lib.user import get_user_list, User
from privacyidea.lib.token import get_tokens
import jwt

__version__ = "0.1"

app = create_app(config_name='production', silent=True)
manager = Manager(app)


@manager.option('--realm', help='Specify the realm where the users should be searched.')
@manager.option('--action', help='Specify the action "enroll".')
@manager.option('--tokentype', help='specify the tokentype you want to enroll.')
@manager.option('--jwt_privkey', help='The private key file of the JWT')
@manager.option('--jwt_user', help='The user in the JWT.')
@manager.option('--jwt_realm', help='The realm in the JWT.')
def finduser(jwt_privkey, jwt_user, jwt_realm, realm, action=None, tokentype=None):

    pkey = None
    auth_token = None
    tokentype = tokentype or "hotp"
    if jwt_privkey:
        with open(jwt_privkey, "r") as f:
            pkey = f.read()
        if pkey:
            auth_token = jwt.encode(payload={"role": "admin",
                                 "username": jwt_user,
                                 "realm": jwt_realm},
                                 key=pkey,
                                 algorithm="RS256")

        # this is simply a test
        #if auth_token:
        #    r = requests.post("https://localhost/token/init",
        #                  verify=False,
        #                  data={"type": "registration",
        #                            "serial": "regtok1-test"},
        #                  headers={"Authorization": auth_token})
        #    if r.status_code == 200:
        #        print("Authentication is working!")
        #    else:
        #        return

    # Now we do all the users
    users = get_user_list(param={"realm": realm})
    usernames = [user.get("username") for user in users]
    print("Processing {0!s} users.".format(len(usernames)))
    num_success = 0
    num_fail = 0

    for user in usernames:
        toks = get_tokens(user=User(user,realm))
        if len(toks) == 0:
            print("user {0!s} has no token assigned.".format(user))
            # Do a REST request with a trusted JWT
            # See https://privacyidea.readthedocs.io/en/latest/installation/system/inifile.html#trusted-jwts
            if auth_token and action == "enroll":
                r = requests.post("https://localhost/token/init",
                              verify=False,
                              data={"type": tokentype,
                                    "genkey": 1,
                                    "user": user,
                                    "realm": realm},
                              headers={"Authorization": auth_token})
                if r.status_code == 200:
                    print("Created token for user {0!s}.".format(user))
                    num_success += 1
                else:
                    print("Failed to create token for user {0!s}.".format(user))
                    num_fail += 1
        else:
            print(".")

        if num_fail:
            print("Failed to create {0!s} tokens.".format(num_fail))
        if num_success:
            print("Created {0!s} tokens.".format(num_success))


if __name__ == '__main__':
    manager.run()

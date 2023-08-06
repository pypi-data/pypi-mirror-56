import requests
import logging
import json
import re

__version__ = '0.2'

LOGGER = logging.getLogger(__name__)


class UserpoolLibrary:
    u"""
    A test library providing user pool support for testing.

        ``UserpoolLibrary`` is a Robot Framework third party library that enables test to borrow available user from a user pool. These allows test to run in CI server without user conflict and lessen setup and maintenance on a project.

        - borrowing an available user from the user pool and returning it.
        - retrieving a user from the user pool by user id
        - updating user password

        == Table of contents ==

        - `Usage`
        - `Examples`
        - `Borrowed User Object`
        - `Author`
        - `Developer Manual`
        - `Importing`
        - `Shortcuts`
        - `Keywords`


    = Usage =

    | =Settings= | =Value=         | =Parameter=          |
    | Library    | UserpoolLibrary | base_url/operator_id |

    Example:
    | =Settings= | =Value=         | =Parameter=                       |
    | Library    | UserpoolLibrary | http://myhost.com/userpoolapi/129 |


    = Examples =

    ``currency_code`` and ``category`` are optional parameter in `Borrow User`

    | =Test Cases=                                         |               |               | =currency_code= | =category= |
    | Borrow any free user                                 | ${user1}      | `Borrow User` | | |
    |                                                      | `Return User` | ${user}       | | |
    | | | | |
    | Borrow user by currency code                         | ${user2}      | `Borrow User` | RMB | |
    |                                                      | `Return User` | ${user}       |     | |
    | | | | |
    | Borrow user by currency code and containing category | ${user3}      | `Borrow User` | RMB | CAT1 |
    |                                                      | `Return User` | ${user}       |     |      |
    | | | | |
    | Borrow user containing category                      | ${user4}      | `Borrow User` | ${EMPTY}  | CAT1 |
    |                                                      | `Return User` | ${user}       |           |      |

    ==>

    | ${user1} = {
    |             "id": 4,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "USD",
    |             "category": "CAT1,CAT2",
    |             "status": "ACTIVE"
    |           }

    ==>
    | ${user2} = {
    |             "id": 2,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "RMB",
    |             "category": "CAT1,CAT2,CAT3",
    |             "status": "ACTIVE"
    |           }

    ==>
    | ${user3} = {
    |             "id": 2,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "RMB",
    |             "category": "CAT1,CAT2,CAT3",
    |             "status": "ACTIVE"
    |           }

    ==>
    | ${user4} = {
    |             "id": 1,
    |             "userName": "sample_username",
    |             "passWord": "sample_password,
    |             "currencyCode": "IDR",
    |             "category": "CAT1,CAT2",
    |             "status": "ACTIVE"
    |           }

    = Borrowed User Object =

    Borrow User returns a json object containing the following information:
    - id
    - userName
    - passWord
    - currencyCode
    - category
    - status

    = Author =

    Created: 09/10/2019

    Author: Shiela Buitizon | email:shiela.buitizon@mnltechnology.com

    Company: Spiralworks Technologies Inc.

    = Developer Manual =

        Compiling this pip package:
            - python setup.py bdist_wheel

        Uploading build to pip
            - python -m twine upload dist/*
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, base_url=None):
        """
        Initialize with  base url.
        """
        self.base_url = base_url

    def borrow_user(self, currency_code=None, category=None):
        """Borrows a FREE user from the user pool given `currency_code` and 'category` and sets it to ACTIVE

        - param ``currency_code``: (optional)
        - param ``category``: (optional)
        - return: free user from the user pool as json object with status set to ACTIVE
        """
        return self._get_free_user(currency_code, category)

    def return_user(self, user):
        """
        Returns an ACTIVE user to the user pool and sets it back to FREE.

        - param ``user``: user object to return to the user pool
        - return: count of record updated
        """
        user_id = user['id']

        return self._free_user(user_id)

    def get_user(self, user_id):
        """
        Returns a user given user id.

        - param ``user_id``: user id
        - return: user json object

        Example:
        | ${user}       | `Get User` | 16 |

        ==>
        | ${user} = {
        |             "id": 16,
        |             "userName": "sample_username",
        |             "passWord": "sample_password",
        |             "currencyCode": "VND",
        |             "category": "CAT6",
        |             "status": "FREE"
        |           }
        """
        return self._get_user(user_id)

    def update_user_password(self, user, new_password):
        """
        Update user password.

        - param ``user``: user json object to update
        - param ``new_password``: new password value
        - return: count of record updated

        Example:
        | ${user}       | `Get User` | 16 |
        | ${count}      | `Update User Password` | ${user} | newpassword |

        ==>
        | ${user} = {
        |             "id": 16,
        |             "userName": "sample_username",
        |             "passWord": "sample_password",
        |             "currencyCode": "VND",
        |             "category": "CAT6",
        |             "status": "FREE"
        |           }
        | ${count} = 1
        """
        user_id = user['id']
        old_password = user['passWord']

        return self._update_user_password(user_id, old_password, new_password)

    def update_user_profile(self, user, email=None, mobileNo=None):
        """
        Update user profile.

        - param ``user``: user json object to update
        - param ``email``: email
        - param ``mobileNo``: mobileNo
        - return: count of record updated or raises TypeError for invalid email or mobile no

        Example:
        | ${user}       | `Get User` | 16 |
        | ${count}      | `Update User Profile` | ${user} | newemail | newmobileno |

        ==>
        | ${user} = {
        |             "id": 16,
        |             "userName": "sample_username",
        |             "passWord": "sample_password",
        |             "currencyCode": "VND",
        |             "category": "CAT6",
        |             "status": "FREE"
        |             "email": null,
        |             "mobileNo": null
        |           }
        | ${count} = 1
        """
        user_id = user['id']

        return self._update_user_profile(user_id, email, mobileNo)

    def _get_free_user(self, currency_code=None, category=None):
        request_url = self.base_url + "/borrow/single"

        params = {'currencyCode': '', 'category': ''}

        if currency_code:
            params.update({"currencyCode": currency_code})
        if category:
            params.update({"category": category})

        LOGGER.debug(f'Params {params}')

        response = requests.get(request_url, params=params)
        response.raise_for_status()

        json_response = response.json()
        LOGGER.debug(f'Retrieved free user {json_response}')

        if bool(response):
            return json_response

        return None

    def _free_user(self, user_id):
        request_url = self.base_url + "/return/single/" + str(user_id)

        response = requests.post(request_url)
        response.raise_for_status()

        return response.text

    def _update_user_password(self, user_id, old_password, new_password):
        request_url = self.base_url + "/update/password/" + str(user_id)

        headers = {'Content-Type': 'application/json'}
        payload = {'oldPassword': old_password, 'newPassword': new_password}

        response = requests.post(request_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        return response.text

    def _update_user_profile(self, user_id, email=None, mobileNo=None):
        request_url = self.base_url + "/update/info/" + str(user_id)

        headers = {'Content-Type': 'application/json'}

        payload = {}
        if email:
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                payload.update({'email': email})
            else:
                raise TypeError("Invalid email")
        if mobileNo:
            if re.match(r"\d{10}$", mobileNo):
                payload.update({'mobileNo': mobileNo})
            else:
                raise TypeError("Invalid mobile number")

        response = requests.post(request_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        return response.text

    def _get_user(self, user_id):
        request_url = self.base_url + "/get/user/" + str(user_id)

        response = requests.get(request_url)
        response.raise_for_status()

        json_response = response.json()
        LOGGER.debug(f'Retrieved free user {json_response}')

        if bool(response):
            return json_response

        return None
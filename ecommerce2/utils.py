# -*- coding: utf-8 -*-


def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    data = {
        'token': token,
        'user': user.id,
        # 'user_braintree_id': 'some_braintreeid'
    }
    return data

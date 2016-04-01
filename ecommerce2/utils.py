# -*- coding: utf-8 -*-
from django.utils import timezone


def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    data = {
        'token': token,
        'user': user.id,
        'orig_iat': timezone.now(),
        # 'user_braintree_id': 'some_braintreeid'
    }
    return data

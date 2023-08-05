# Copyright (C) 2019-2022 Andre Laksmana <andre.laksmana@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import transaction as tx
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from django.apps import apps

from taiga.base.utils.slug import slugify_uniquely
from taiga.base import exceptions as exc
from taiga.auth.services import send_register_email
from taiga.auth.services import make_auth_response_data, get_membership_by_token
from taiga.auth.signals import user_registered as user_registered_signal

from . import connector


@tx.atomic
def openid_register(username:str, email:str, full_name:str, openid_id:int, token:str=None):
    """
    Register a new user from openid.

    This can raise `exc.IntegrityError` exceptions in
    case of conflics found.

    :returns: User
    """
    auth_data_model = apps.get_model("users", "AuthData")
    user_model = apps.get_model("users", "User")

    try:
        # openid user association exist?
        auth_data = auth_data_model.objects.get(key="openid", value=openid_id)
        user = auth_data.user
    except auth_data_model.DoesNotExist:
        try:
            # Is a user with the same email as the openid user?
            user = user_model.objects.get(email=email)
            auth_data_model.objects.create(user=user, key="openid", value=openid_id, extra={})
        except user_model.DoesNotExist:
            # Create a new user
            username_unique = slugify_uniquely(username, user_model, slugfield="username")
            user = user_model.objects.create(email=email,
                                             username=username_unique,
                                             full_name=full_name)
            auth_data_model.objects.create(user=user, key="openid", value=openid_id, extra={})

            send_register_email(user)
            user_registered_signal.send(sender=user.__class__, user=user)

    if token:
        membership = get_membership_by_token(token)

        try:
            membership.user = user
            membership.save(update_fields=["user"])
        except IntegrityError:
            raise exc.IntegrityError(_("This user is already a member of the project."))

    return user


def openid_login_func(request):
    code = request.DATA.get('code', None)
    token = request.DATA.get('token', None)
    accessToken = request.DATA.get('access_token', None)
    redirect_uri = request.DATA.get('url', None)

    user_info = connector.me(code, accessToken, redirect_uri)
    user = openid_register(username=user_info.username,
                           email=user_info.email,
                           full_name=user_info.full_name,
                           openid_id=user_info.id,
                           token=token)
    data = make_auth_response_data(user)
    return data

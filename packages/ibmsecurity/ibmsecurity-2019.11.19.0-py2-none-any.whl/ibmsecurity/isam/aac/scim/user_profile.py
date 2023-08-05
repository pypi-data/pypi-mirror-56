import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current user profile SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current user profile SCIM configuration settings",
                                    "/mga/scim/configuration/urn:ietf:params:scim:schemas:core:2.0:User",
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)


def set(isamAppliance, ldap_connection, user_suffix, search_suffix, check_mode=False, force=False):
    """
    Updating the user profile SCIM configuration settings
    """
    ret_obj = get(isamAppliance)
    ret_obj = ret_obj['data']['urn:ietf:params:scim:schemas:core:2.0:User']
    del ret_obj['ldap_connection']
    del ret_obj['user_suffix']
    del ret_obj['search_suffix']

    ret_obj['ldap_connection'] = ldap_connection
    ret_obj['user_suffix'] = user_suffix
    ret_obj['search_suffix'] = search_suffix
    return isamAppliance.invoke_put(
        "Updating the user profile SCIM configuration settings",
        "/mga/scim/configuration/urn:ietf:params:scim:schemas:core:2.0:User",
        ret_obj, requires_modules=requires_modules,
        requires_version=requires_version)
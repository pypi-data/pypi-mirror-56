import logging


logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"


def get(isamAppliance, ldap_connection, ldap_objectclasses='', check_mode=False, force=False):
    """
    Retrieving the current list of user associated ldap attributes from the configured
    """
    return isamAppliance.invoke_get(
        "Retrieving the current list of user associated ldap attributes from the configured ",
        "{0}/urn:ietf:params:scim:schemas:core:2.0:User/ldap_attributes?ldap_connection={1}&ldap_objectclasses={1}".format(
            uri, ldap_connection, ldap_objectclasses),
        requires_modules=requires_modules,
        requires_version=requires_version
        )
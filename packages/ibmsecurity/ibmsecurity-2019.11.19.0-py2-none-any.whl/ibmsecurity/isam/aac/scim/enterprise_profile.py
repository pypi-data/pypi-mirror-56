import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"

def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current enterprise user profile SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current enterprise user profile SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version)

def set(isamAppliance, mappings, check_mode=False, force=False):
    """
    Updating the enterprise user profile SCIM configuration settings

    """
    return isamAppliance.invoke_put("Updating the enterprise user profile SCIM configuration settings",
                                    "{0}/urn:ietf:params:scim:schemas:extension:enterprise:2.0:User".format(uri),
                                    mappings,
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )

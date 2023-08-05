import logging
import ibmsecurity.isam.aac.server_connections.ws
from ibmsecurity.utilities.tools import json_sort

logger = logging.getLogger(__name__)

uri = "/mga/scim/configuration"
requires_modules = ["mga", "federation"]
requires_version = "9.0.2"



def get(isamAppliance, check_mode=False, force=False):
    """
    Retrieving the current general SCIM configuration settings
    """
    return isamAppliance.invoke_get("Retrieving the current general SCIM configuration settings",
                                    "{0}/general".format(uri),
                                    requires_modules=requires_modules,
                                    requires_version=requires_version
                                    )
# coding: utf-8

"""
    assetic.FunctionalLocationTools
    Tools to assist with using Assetic API's for functional location.
"""
from __future__ import absolute_import

import six

from assetic import \
    FunctionalLocationApi\
    , CreatedRepresentationFunctionalLocationRepresentation\
    , FunctionalLocationRepresentation\
    , AssetTools

from ..rest import ApiException
from ..api_client import ApiClient
from typing import Optional, List


class FunctionalLocationTools(object):
    """
    Class to manage processes involving functional location
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        self.logger = api_client.configuration.packagelogger

        self.fl_api = FunctionalLocationApi()
        self._asset_tools = AssetTools()

    def create_functional_location(self, fl_representation):
        # type: (FunctionalLocationRepresentation) -> Optional [CreatedRepresentationFunctionalLocationRepresentation, None]
        """
        Create a functional location.
        :param fl_representation: required
        FunctionalLocationRepresentation
        :return: resultant functional location as
        FunctionalLocationRepresentation
        """
        # First make sure the object is correct
        self.logger.debug("Verify functional location fields")
        mandatory_fields = ["functional_location_name"
            , "functional_location_type"]
        if not self._asset_tools.verify_mandatory_fields(
                fl_representation
                , FunctionalLocationRepresentation
                , mandatory_fields):
            return None

        # create the functional location
        self.logger.info("Create the functional location {0}".format(
            fl_representation.functional_location_name))
        try:
            response = self.fl_api.functional_location_post(fl_representation)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return None

        return response

    def create_functional_location_if_new(self, fl_representation):
        # type: (FunctionalLocationRepresentation) ->
        # type: Optional [CreatedRepresentationFunctionalLocationRepresentation, None]
        """
        Create a functional location only if new name for the given type,
        otherwise return existing
        :param fl_representation: required
        FunctionalLocationRepresentation
        :return: resultant functional location as
        FunctionalLocationRepresentation
        """
        # check to see if existing
        existing_fl = self.get_functional_locations_for_type_by_name(
            fl_representation.functional_location_name
            , fl_representation.functional_location_type
            , fl_representation.attributes
        )
        if existing_fl and len(existing_fl) > 0:
            # return first record
            return existing_fl[0]

        # no existing fl so create the functional location
        self.logger.info("Create the functional location {0}".format(
            fl_representation.functional_location_name))
        try:
            response = self.fl_api.functional_location_post(fl_representation)
        except ApiException as e:
            self.logger.error("Status {0}, Reason: {1} {2}".format(
                e.status, e.reason, e.body))
            return None

        return response

    def get_functional_location_by_id(self, fl_id, attributes=None):
        """
        Get a functional location for the given functional location ID
        Can be either the GUID or the user friendly ID
        :param fl_id: The functional location GUID or Friendly ID
        :param attributes: A list of non-core attributes to get
        :return: fl response object or None
        """
        # type: (str, Optional [List[str]]) -> Optional [FunctionalLocationRepresentation, None]
        if not attributes:
            attributes = list()
        self.logger.debug("Get the functional location {0}".format(
            fl_id))
        try:
            fl = self.fl_api.functional_location_get(fl_id, attributes)
        except ApiException as e:
            if e.status == 404:
                self.logger.error(
                    "Functional Location for Functional Location GUID/Id {0} "
                    "not found".format(fl_id))
            else:
                msg = "Status {0}, Reason: {1} {2}".format(e.status, e.reason,
                                                           e.body)
                self.logger.error(msg)
            return None
        return fl

    def get_functional_locations_for_type_by_name(self, fl_name, fl_type,
                                                 attributes=None):
        """
        For the given name and functional location type return the
        functional location(s).  Name is not unique
        :param fl_name:
        :param fl_type:
        :param attributes:
        :return:
        """
        # type: (str, str, Optional [List[str]]) -> Optional [list[FunctionalLocationRepresentation], None]
        if not attributes:
            attributes = list()
        kwargs = {
            'request_params_page': 1
            , 'request_params_page_size': 50
            , 'request_params_filters':
                "FunctionalLocationType~eq~'{0}'~and~"
                "FunctionalLocationName~eq~'{1}'".format(fl_name, fl_type)
        }
        self.logger.debug(
            "Get the functional location for name {0} and type {1}".format(
                fl_name, fl_type))
        try:
            fl = self.fl_api.functional_location_get_0(attributes, **kwargs)
        except ApiException as e:
            if e.status == 404:
                self.logger.error(
                    "Functional Location for Functional Location for name {0}"
                    " and type {1}".format(fl_name, fl_type))
            else:
                msg = "Status {0}, Reason: {1} {2}".format(e.status, e.reason,
                                                           e.body)
                self.logger.error(msg)
            return None
        return fl["ResourceList"]

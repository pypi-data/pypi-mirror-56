# Copyright 2018 Orange and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import logging
import sys

import hug
import requests
from moon_cache.cache import Cache
from moon_engine.api.configuration import get_configuration
from moon_utilities import exceptions

logger = logging.getLogger("moon.engine.api.wrapper" + __name__)


class UpdateWrapper(object):
    __CACHE = None

    def __init__(self):
        if not self.__CACHE:
            self.__CACHE = Cache.getInstance(
                manager_url=get_configuration("manager_url"),
                incremental=get_configuration("incremental_updates"),
                manager_api_key=get_configuration("api_token"))

    def update_pdp(self, pdp_id, data, moon_user_id=None):

        url_pattern = "update/pdp/{}".format(pdp_id)
        return self.__process_request(url_pattern, body=data, moon_user_id=moon_user_id)

    def delete_pdp(self, pdp_id, moon_user_id=None):

        url_pattern = "update/pdp/{}".format(pdp_id)
        return self.__process_request(url_pattern, moon_user_id=moon_user_id, delete=True)

    def delete_policy(self, policy_id, moon_user_id=None):
        url_pattern = "update/policy/{}".format(policy_id)
        return self.__process_request(url_pattern, moon_user_id, policy_id=policy_id, delete=True)

    def update_policy(self, policy_id, data=None, moon_user_id=None):

        url_pattern = "update/policy/{}".format(policy_id)
        return self.__process_request(url_pattern, body=data, moon_user_id=moon_user_id,
                                      policy_id=policy_id)

    def delete_assignment(self, type, policy_id, perimeter_id=None, category_id=None, data_id=None,
                          moon_user_id=None):

        if policy_id and perimeter_id and category_id and data_id:
            url_pattern = "update/assignment/{}/{}/{}/{}/{}".format(policy_id, type, perimeter_id,
                                                                    category_id,
                                                                     data_id)

        if policy_id and perimeter_id and category_id:
            url_pattern = "update/assignment/{}/{}/{}/{}".format(policy_id, type, perimeter_id,
                                                                 category_id)

        if policy_id and perimeter_id:
            url_pattern = "update/assignment/{}/{}/{}".format(policy_id, type, perimeter_id)

        if policy_id:
            url_pattern = "update/assignment/{}/{}".format(policy_id, type)

        return self.__process_request(url_pattern, moon_user_id, policy_id=policy_id, delete=True)

    def update_perimeter(self, type, perimeter_id, data=None, policy_id=None, moon_user_id=None):
        url_pattern = "update/perimeter/{}/{}/{}".format(perimeter_id, policy_id, type)
        return self.__process_request(url_pattern, body=data, moon_user_id=moon_user_id,
                                policy_id=policy_id)

    def delete_perimeter(self, type, perimeter_id, policy_id=None, moon_user_id=None):
        url_pattern = "update/perimeter/{}/{}/{}".format(perimeter_id, policy_id, type)
        return self.__process_request(url_pattern, moon_user_id, policy_id=policy_id, delete=True)

    def delete_rule(self, rule_id, policy_id, moon_user_id=None):

        url_pattern = "update/rule/{}/{}".format(policy_id, rule_id)
        return self.__process_request(url_pattern, moon_user_id=moon_user_id, policy_id=policy_id,
                                      delete=True)

    def update_model(self, model_id, data=None, moon_user_id=None):

        url_pattern = "update/model/{}".format(model_id)
        return self.__process_request(url_pattern, body=data, moon_user_id=moon_user_id)

    def delete_model(self, model_id, moon_user_id=None):

        url_pattern = "update/model/{}".format(model_id)
        return self.__process_request(url_pattern, moon_user_id=moon_user_id, delete=True)

    def delete_category(self, category_id, type, moon_user_id=None):

        url_pattern = "update/meta_data/{}/{}".format(category_id, type)
        return self.__process_request(url_pattern, moon_user_id=moon_user_id, delete=True)

    def update_meta_rule(self, meta_rule_id, data=None, moon_user_id=None):

        url_pattern = "update/meta_rule/{}".format(meta_rule_id, type)
        return self.__process_request(url_pattern, body=data, moon_user_id=moon_user_id)

    def delete_meta_rule(self, meta_rule_id, moon_user_id=None):

        url_pattern = "update/meta_rule/{}".format(meta_rule_id, type)
        return self.__process_request(url_pattern, moon_user_id=moon_user_id, delete=True)

    def delete_data(self, data_id, type, moon_user_id=None):

        url_pattern = "update/data/{}/{}".format(data_id, type)
        return self.__process_request(url_pattern, moon_user_id=moon_user_id, delete=True)

    def delete_attributes(self, name, moon_user_id=None):

        url_pattern = "update/attributes/{}".format(name)
        return self.__process_request(url_pattern, moon_user_id=moon_user_id, delete=True)

    def __process_request(self, url_pattern, body=None, moon_user_id=None, policy_id=None,
                          delete=False):

        if policy_id:
            endpoint = self.__CACHE.get_pipeline_url(pipeline_id=policy_id)
            api_key = self.__CACHE.get_api_key(pipeline_id=policy_id)

            if not endpoint:
                return hug.HTTP_208
            if delete:
                return self.__execute_delete_request(endpoint, url_pattern, api_key)
            else:
                return self.__execute_put_request(endpoint, url_pattern, api_key, body)

        else:
            pdps = self.__CACHE.pdp
            for _pdp_id in pdps:
                vim_project_id = pdps.get(_pdp_id, {}).get("vim_project_id")
                if vim_project_id:
                    api_key = self.__CACHE.get_api_key(project_id=vim_project_id)
                    endpoint = self.__CACHE.get_pipeline_url(project_id=vim_project_id)

                    if delete:
                        return self.__execute_delete_request(endpoint, url_pattern, api_key)
                    else:
                        return self.__execute_put_request(endpoint, url_pattern, api_key, body)
            return hug.HTTP_206

    @staticmethod
    def __execute_put_request(endpoint, url_pattern, api_key, body):
        try:
            req = requests.put("{}/{}".format(
                endpoint, url_pattern), headers={"X-Api-Key": api_key}, json=body)

            if req.status_code == 200:
                return hug.HTTP_200
            if req.status_code == 202:
                return hug.HTTP_202
            if req.status_code == 208:
                return hug.HTTP_208

            else:
                raise exceptions.AuthzException(
                    "Receive bad response from Authz function "
                    "(with address - {})".format(req.status_code))

        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to {}".format(
                "{}/authz/{}".format(endpoint, url_pattern))
            )
        except Exception as e:
            logger.exception("Unexpected error:", e)

    @staticmethod
    def __execute_delete_request(endpoint, url_pattern, api_key):

        try:
            req = requests.delete("{}/{}".format(
                endpoint, url_pattern), headers={"X-Api-Key": api_key})

            if req.status_code == 200:
                return hug.HTTP_200
            if req.status_code == 202:
                return hug.HTTP_202
            if req.status_code == 208:
                return hug.HTTP_208

            else:
                raise exceptions.AuthzException(
                    "Receive bad response from Authz function "
                    "(with address - {})".format(req.status_code))

        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to {}".format(
                "{}/authz/{}".format(endpoint, url_pattern))
            )
        except Exception as e:
            logger.exception("Unexpected error:", e)

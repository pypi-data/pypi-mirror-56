# Copyright 2019 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class LogMessageEnum:
    """ Classobj encapsulating various logging messages """

    class DEBUG_MESSAGES:
        """ Classobj encapsulating various DEBUG messages """

        LOG_LEVEL_SET = '({file}): Log level set to {level}'
        SET_DEVELOPMENT_MODE = '({file}): DEVELOPMENT mode is ON'
        VALID_CONFIGURATION = '({file}): SDK configuration and account settings are valid.'
        CUSTOM_LOGGER_USED = '({file}): Custom logger used'
        LOGGING_LOGGER_INSTANCE_USED = '({file}): Python logging module"s logger instantiated'
        SDK_INITIALIZED = '({file}): SDK properly initialzed'
        SETTINGS_FILE_PROCESSED = '({file}): Settings file processed'
        NO_STORED_VARIATION = '({file}): No stored variation for UserId:{user_id} for Campaign:{campaign_key} found in UserStorage'
        NO_USER_STORAGE_GET = '({file}): No UserStorage to look for stored data'
        NO_USER_STORAGE_SET = '({file}): No UserStorage to set data'
        GETTING_STORED_VARIATION = '({file}): Got stored variation for UserId:{user_id} of Campaign:{campaign_key} as Variation: {variation_name} found in UserStorage'
        CHECK_USER_ELIGIBILITY_FOR_CAMPAIGN = '({file}): campaign:{campaign_key} having traffic allocation:{traffic_allocation} assigned value:{traffic_allocation} to userId:{user_id}'
        USER_HASH_BUCKET_VALUE = '({file}): userId:{user_id} having hash:{hash_value} got bucketValue:{bucket_value}'
        VARIATION_HASH_BUCKET_VALUE = '({file}): userId:{user_id} for campaign:{campaign_key} having percent traffic:{percent_traffic} got hash-value:{hash_value} and bucket value:{bucket_value}'
        GOT_VARIATION_FOR_USER = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} got variationName:{variation_name} inside method:{method}'
        USER_NOT_PART_OF_CAMPAIGN = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} did not become part of campaign method:{method}'
        UUID_FOR_USER = '({file}): Uuid generated for userId:{user_id} and accountId:{account_id} is {desired_uuid}'
        IMPRESSION_FOR_TRACK_USER = '({file}): Impression built for track-user - {properties}'
        IMPRESSION_FOR_TRACK_GOAL = '({file}): Impression built for track-goal - {properties}'

        PARAMS_FOR_PUSH_CALL = '({file}): Params for push call - {properties}'

    class INFO_MESSAGES:
        """ Classobj encapsulating various INFO messages """

        VARIATION_RANGE_ALLOCATION = '({file}): Campaign:{campaign_key} having variations:{variation_name} with weight:{variation_weight} got range as: ( {start} - {end} ))'
        VARIATION_ALLOCATED = '({file}): UserId:{user_id} of Campaign:{campaign_key} type: {campaign_type} got variation: {variation_name}'
        LOOKING_UP_USER_STORAGE = '({file}): Looked into UserStorage for userId:{user_id} successful'
        SAVING_DATA_USER_STORAGE = '({file}): Saving into UserStorage for userId:{user_id} successful'
        GOT_STORED_VARIATION = '({file}): Got stored variation:{variation_name} of campaign:{campaign_key} for userId:{user_id} from UserStorage'
        NO_VARIATION_ALLOCATED = '({file}): UserId:{user_id} of Campaign:{campaign_key} type: {campaign_type} did not get any variation'
        USER_ELIGIBILITY_FOR_CAMPAIGN = '({file}): Is userId:{user_id} part of campaign? {is_user_part}'
        GOT_VARIATION_FOR_USER = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} got variationName:{variation_name}'
        USER_GOT_NO_VARIATION = '({file}): userId:{user_id} for campaign:{campaign_key} type: {campaign_type} did not allot any variation'
        IMPRESSION_SUCCESS = '({file}): Impression event - {end_point} was successfully received by VWO'
        MAIN_KEYS_FOR_IMPRESSION = '({file}): Having main keys: accountId:{account_id} userId:{user_id} campaignId:{campaign_id} and variationId:{variation_id}'
        MAIN_KEYS_FOR_PUSH_API = '({file}): Having main keys: accountId:{account_id} userId:{user_id} u:{u} and tags:{tags}'
        INVALID_VARIATION_KEY = '({file}): Variation was not assigned to userId:{user_id} for campaign:{campaign_key}'
        RETRY_FAILED_IMPRESSION_AFTER_DELAY = '({file}): Failed impression event for {end_point} will be retried after {retry_timeout} milliseconds delay'

        USER_IN_FEATURE_ROLLOUT = '({file}): User ID:{user_id} is in feature rollout:{campaign_key}'
        USER_NOT_IN_FEATURE_ROLLOUT = '({file}): User ID:{user_id} is NOT in feature rollout:{campaign_key}'
        FEATURE_ENABLED_FOR_USER = '({file}): In API: {api_name} Feature having feature-key:{feature_key} for user ID:{user_id} is enabled'
        FEATURE_NOT_ENABLED_FOR_USER = '({file}): In API: {api_name} Feature having feature-key:{feature_key} for user ID:{user_id} is not enabled'

        VARIABLE_FOUND = '({file}): In API: {api_name} Value for variable:{variable_key} of campaign:{campaign_key} and campaign type: {campaign_type} is:{variable_value} for user:{user_id}'

        USER_PASSED_PRE_SEGMENTATION = '({file}): UserId:{user_id} of campaign:{campaign_key} with custom_variables:{custom_variables} passed pre segmentation'
        USER_FAILED_PRE_SEGMENTATION = '({file}): UserId:{user_id} of campaign:{campaign_key} with custom_variables:{custom_variables} failed pre segmentation'

        NO_CUSTOM_VARIALBES = '({file}): In API: {api_name}, for UserId:{user_id} preSegments/customVariables are not passed for campaign:{campaign_key} and campaign has pre-segmentation'
        SKIPPING_PRE_SEGMENTATION = '({file}): In API: {api_name}, Skipping pre-segmentation for UserId:{user_id} as no valid segments found in campaing:{campaign_key}'

    class WARNING_MESSAGES:
        """ Classobj encapsulating various WARNING messages """

    class ERROR_MESSAGES:
        """ Classobj encapsulating various ERROR messages """

        SETTINGS_FILE_CORRUPTED = '({file}): Settings file is corrupted. Please contact VWO Support for help.'
        ACTIVATE_API_INVALID_PARAMS = '({file}): {api_name} API got bad parameters. It expects campaignKey(String) as first and userId(String) as second argument, customVariables(dict) can be passed via kwargs for pre-segmentation'
        API_CONFIG_CORRUPTED = '({file}): "{api_name}" API has corrupted configuration'
        GET_VARIATION_NAME_API_INVALID_PARAMS = '({file}): {api_name} API got bad parameters. It expects campaignKey(String) as first and userId(String) as second argument, customVariables(dict) can be passed via kwargs for pre-segmentation'
        TRACK_API_INVALID_PARAMS = '({file}): {api_name} API got bad parameters. It expects campaignKey(String) as first userId(String) as second and goalIdentifier(String/Number) as third argument. revenueValue(Float/Number/String) can be passed through kwargs and is required for revenue goal only. customVariables(dict) can be passed via kwargs for pre-segmentation'
        TRACK_API_GOAL_NOT_FOUND = '({file}): In {api_name} Goal:{goal_identifier} not found for campaign:{campaign_key} and userId:{user_id}'
        TRACK_API_REVENUE_NOT_PASSED_FOR_REVENUE_GOAL = '({file}):  In {api_name} Revenue value should be passed for revenue goal:{goal_identifier} for campaign:{campaign_key} and userId:{user_id}'
        TRACK_API_VARIATION_NOT_FOUND = '({file}): Variation not found for campaign:{campaign_key} and userId:{user_id}'
        CAMPAIGN_NOT_RUNNING = '({file}): API used:{api_name} - Campaign:{campaign_key} is not RUNNING. Please verify from VWO App'
        LOOK_UP_USER_STORAGE_FAILED = '({file}): Looking data from UserStorage failed for userId:{user_id}'
        SET_USER_STORAGE_FAILED = '({file}): Saving data into UserStorage failed for userId:{user_id}'
        INVALID_CAMPAIGN = '({file}): Invalid campaign passed to {method} of this file'
        INVALID_USER_ID = '({file}): Invalid userId:{user_id} passed to {method} of this file'
        IMPRESSION_FAILED = '({file}): Impression event could not be sent to VWO - {end_point}'
        CUSTOM_LOGGER_MISCONFIGURED = '({file}): Custom logger is provided but seems to have misconfigured. {extra_info} Please check the API Docs. Using default logger.'

        INVALID_API = '({file}): {api_name} API is not valid for user ID: {user_id} in campaign ID: {campaign_key} having campaign type: {campaign_type}.'
        IS_FEATURE_ENABLED_API_INVALID_PARAMS = '({file}): {api_name} API got bad parameters. It expects campaign_key(String) as first and user_id(String) as second argument, customVariables(dict) can be passed via kwargs for pre-segmentation'
        GET_FEATURE_VARIABLE_VALUE_API_INVALID_PARAMS = '({file}): "get_feature_variable" API got bad parameters. It expects campaign_key(String) as first, variable_key(string) as second and user_id(String) as third argument, customVariables(dict) can be passed via kwargs for pre-segmentation'

        VARIABLE_NOT_FOUND = '({file}): In API: {api_name} Variable {variable_key} not found for campaing {campaign_key} and type {campaign_type} for user ID {user_id}'
        UNABLE_TO_TYPE_CAST = '({file}): Unable to typecast value: {value} of type: {of_type} to type: {variable_type}.'

        USER_NOT_IN_CAMPAIGN = '({file}): userId:{user_id} did not become part of campaign:{campaign_key} and campaign type:{campaign_type}'
        API_NOT_WORKING = '({file}): API: {api_name} not working, exception caught: {exception}. Please contact VWO Support for help.'

        PRE_SEGMENTATION_ERROR = '({file}): Error while segmenting the UserId:{user_id} of campaign:{campaign_key} with custom_variables:{custom_variables}. Error message: {error_message}'

        PUSH_API_INVALID_PARAMS = '({file}): {api_name} API got bad parameters. It expects tag_key(String) as first and tag_value(String) as second argument and user_id(String) as third argument'
        TAG_VALUE_LENGTH_EXCEEDED = '({file}): In API: {api_name}, the length of tag_value:{tag_value} and userID: {user_id} can not be greater than 255'
        TAG_KEY_LENGTH_EXCEEDED = '({file}): In API: {api_name}, the length of tag_key:{tag_key} and userID: {user_id} can not be greater than 255'

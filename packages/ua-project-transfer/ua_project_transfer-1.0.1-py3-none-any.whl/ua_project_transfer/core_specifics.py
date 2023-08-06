import logging
import sentry_sdk
from ua_stache_api import ua_stache_api
from ua_ilab_tools import ua_ilab_tools
from ua_project_transfer import log_config
from ua_project_transfer import project_lims_tools
from uagc_tools.contact_utility import contact
from uagc_tools.log_tools import log_tools


def setup_log():
    logging.config.dictConfig(log_config.CONFIG)
    log_tools.clear_existing_loggers("__main__", logging.WARNING)


def setup_monitoring():
    with open("sentry_stache_token.json", 'r') as file:
        contents = file.read()
    sentry_key, sentry_url = ua_stache_api.get_entry(contents)
    sentry_creds = ua_stache_api.auth(
        sentry_key, sentry_url, "uagc_research_project_transfer")
    sentry_sdk.init(sentry_creds)


def setup_lims_api(env):
    with open("lims_stache_token.json", 'r') as file:
        contents = file.read()

    lims_key, lims_endpoint = ua_stache_api.get_entry(contents)
    lims_creds = ua_stache_api.auth(lims_key, lims_endpoint, env)
    lims_utility = project_lims_tools.LimsUtility(
        lims_creds["host"], lims_creds["username"], lims_creds["password"])

    return lims_utility


def setup_ilab_api(env):
    with open("ilab_stache_token.json", 'r') as file:
        contents = file.read()

    ilab_key, ilab_endpoint = ua_stache_api.get_entry(contents)
    ilab_creds = ua_stache_api.auth(ilab_key, ilab_endpoint, env)
    ilab_tools = ua_ilab_tools.IlabTools(
        ilab_creds["CORE_ID"], ilab_creds["BTOKEN"])

    return ilab_tools


def get_entry(request_type):
    return contact.get_email(request_type)

from __future__ import absolute_import, annotations

import argparse
import logging
import os

from wenet.common.interface.hub import HubInterface
from wenet.common.interface.profile_manager import ProfileManagerInterface


logger = logging.getLogger("wenet.utils.users_profiles_aligner")


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Users-Profiles aligner - deletes users without a profile and profiles without a user")
    arg_parser.add_argument("-i", "--instance", type=str, default=os.getenv("INSTANCE", "https://wenet.u-hopper.com/dev"), help="The target WeNet instance")
    arg_parser.add_argument("--check", action='store_true', help="Flag to set for only checking users and profiles without deleting anything")
    arg_parser.add_argument("-a", "--apikey", type=str, default=os.getenv("APIKEY"), help="The apikey for accessing the WeNet services")
    args = arg_parser.parse_args()

    hub_host = args.instance + "/hub/frontend"
    profile_manager_host = args.instance + "/profile_manager"

    hub_interface = HubInterface(hub_host)
    profile_manager_connector = ProfileManagerInterface(profile_manager_host, args.apikey)

    profile_user_ids = profile_manager_connector.get_profile_user_ids()
    user_ids = hub_interface.get_user_ids()

    empty_profile_counter = 0
    for profile_user_id in profile_user_ids:
        if profile_user_id not in user_ids:
            empty_profile_counter += 1
            logger.debug(f"profile [{profile_user_id}] without user")
            if not args.check:
                profile_manager_connector.delete_user_profile(profile_user_id)
                logger.debug(f"deleted profile [{profile_user_id}]")

    logger.info(f"{empty_profile_counter} profiles without user")

    empty_user_counter = 0
    for user_id in user_ids:
        if user_id not in profile_user_ids:
            empty_user_counter += 1
            logger.debug(f"user [{user_id}] without profile")
            if not args.check:
                pass  # TODO when the endpoint for deleting users will be implemented, it will be possible to delete the users without a profile
                # hub_interface.delete_user(user_id)
                # logger.debug(f"deleted user [{user_id}]")

    logger.info(f"{empty_user_counter} users without profile")

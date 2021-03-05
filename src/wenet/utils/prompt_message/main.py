from __future__ import absolute_import, annotations

import argparse
import logging

import requests

from wenet.common.interface.hub import HubInterface
from wenet.common.model.message.message import TextualMessage


logger = logging.getLogger("wenet.utils.prompt_message")


def message_for_user(app_id: str, receiver_id: str, text: str, app_callback: str, title: str = "") -> None:
    message = TextualMessage(
        app_id,
        receiver_id,
        title,
        text,
        {
            "communityId": None,
            "taskId": None
        }
    )
    response = requests.post(app_callback, json=message.to_repr())
    logger.debug(response.status_code)
    logger.debug(response.text)


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Prompt message - Send a message to a specific user or to the whole community of an app")

    arg_parser.add_argument("-i", "--instance", type=str, default="https://wenet.u-hopper.com/dev", help="The target WeNet instance")
    arg_parser.add_argument("-a", "--app_id", required=True, type=str, help="The target application")

    sub_parsers = arg_parser.add_subparsers(dest="subParser", help="Message source")

    text_parser = sub_parsers.add_parser("text", help="Send a single text message")
    text_parser.add_argument("-t", "--text", required=True, type=str, help="The text for the message to send")
    text_parser.add_argument("-ti", "--title", type=str, default="", help="The title for the message to send")
    text_parser.add_argument("-u", "--user_id", type=str, help="The user to send the message to")

    file_parser = sub_parsers.add_parser("input", help="Send the text message of the current day from an input csv/tsv file, it should have 2 columns, `Date` and `Message`")
    file_parser.add_argument("-p", "--path", required=True, type=str, help="The path of the csv/tsv file")
    file_parser.add_argument("-u", "--user_id", type=str, help="The user to send the message to")

    args = arg_parser.parse_args()

    if args.subParser == "text":

        hub_interface = HubInterface(f"{args.instance}/hub/frontend")
        app_details = hub_interface.get_app_details(args.app_id)

        if args.user_id:
            # message for specific user
            logger.debug(f"Publishing text [{args.text}] for user [{args.user_id}]")
            message_for_user(args.app_id, args.user_id, args.text, app_details["messageCallbackUrl"], title=args.title)
        else:
            user_ids = hub_interface.get_user_ids_for_app(args.app_id)
            for user_id in user_ids:
                logger.debug(f"Publishing text [{args.text}] for user [{user_id}]")
                message_for_user(args.app_id, user_id, args.text, app_details["messageCallbackUrl"], title=args.title)

    elif args.subParser == "input":
        logger.debug("do logic here")

    else:
        logger.warning("You should choose one of the following working modes [text, input]")

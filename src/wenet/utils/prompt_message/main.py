from __future__ import absolute_import, annotations

import argparse
import logging

import requests

from wenet.common.interface.hub import HubInterface
from wenet.common.model.message.message import TextualMessage


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
    logging.debug(response.status_code)
    logging.debug(response.text)


if __name__ == "__main__":

    argParser = argparse.ArgumentParser(description="Prompt message - Send a message to the whole community of an app")

    argParser.add_argument("-i", "--instance", type=str, default="https://wenet.u-hopper.com/dev", help="The target WeNet instance")
    argParser.add_argument("-a", "--app_id", required=True, type=str, help="The target application")

    subParsers = argParser.add_subparsers(dest="subparser", help="Message source")

    text_parser = subParsers.add_parser("text", help="Send a single text")
    text_parser.add_argument("-t", "--text", required=True, type=str, help="The text for the message to send")
    text_parser.add_argument("-ti", "--title", type=str, help="The title for the message to send")
    text_parser.add_argument("-u", "--user_id", type=str, help="The user to send the message to")

    args = argParser.parse_args()

    if args.subparser == "text":

        hub_interface = HubInterface(f"{args.instance}/hub/frontend")
        app_details = hub_interface.get_app_details(args.app_id)

        if args.user_id:
            # message for specific user
            logging.debug(f"Publishing text [{args.text}] for user [{args.user_id}]")
            message_for_user(args.app_id, args.user_id, args.text, app_details["messageCallbackUrl"], title=args.title)
        else:
            user_ids = hub_interface.get_user_ids_for_app(args.app_id)
            for user_id in user_ids:
                logging.debug(f"Publishing text [{args.text}] for user [{user_id}]")
                message_for_user(args.app_id, user_id, args.text, app_details["messageCallbackUrl"], title=args.title)

    else:
        logging.warning("You should choose the working mode [text]")

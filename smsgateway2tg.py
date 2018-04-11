#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram bot for resending sms messages from smsgateway.me API POST callback to telegram bot users.

"""

import uuid
import logging
import telegram
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

ROUTE = "/smsgateway"
PORT = 8810

TELEGRAM_BOT_USERS = [21739552, 811934622]
TELEGRAM_TOKEN = "193385732:aBbs_UcsIiTfioL2w2HI_laQ2I-uhsUzNuI"
TELEGRAM_BOT = telegram.Bot(token=TELEGRAM_TOKEN)

BANK_NAME = "MyBankName"


class SMSHandler(RequestHandler):
    @staticmethod
    def get_uid():
        """Get short unique ids like a46fed3.
        """
        return uuid.uuid4().hex[:7]

    @staticmethod
    def send_telegram_message(uid, message, user):
        """Send text message to Telegram bot's user.
        """
        try:
            TELEGRAM_BOT.send_message(user, message)
            logging.debug("Send message {uid} to {user}".format(
                uid=uid, user=user))

        except:
            logging.exception("Failed to send message {uid} to {user}".format(
                uid=uid, user=user))

    @coroutine
    def post(self):
        try:
            sms_message = self.get_arguments("message")[0]
            uid = self.get_uid()

            sms_sender_name = self.get_arguments("contact[number]")[0]
            if sms_sender_name == BANK_NAME:
                logging.debug(
                    "Get message {uid} from {sender}: {message}".format(
                        uid=uid, sender=sms_sender_name, message=sms_message))

                for telegram_bot_user in TELEGRAM_BOT_USERS:
                    self.send_telegram_message(uid, sms_message,
                                               telegram_bot_user)

        except:
            logging.exception(
                "Failed to handle smsgateway message callback: {request}".
                format(request=self.request))


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)-8s] %(message)s")
        Application([(ROUTE, SMSHandler)]).listen(PORT)
        logging.info("Start server at 0.0.0.0:{}{}".format(PORT, ROUTE))
        IOLoop.current().start()

    except KeyboardInterrupt:
        pass

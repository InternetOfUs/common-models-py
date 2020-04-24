from __future__ import absolute_import, annotations

from unittest import TestCase

from wenet.service_api.authentication_account import TelegramAuthenticationAccount, AuthenticationAccount, \
    WeNetUserWithAccounts


class TestTelegramAuthenticationAccount(TestCase):

    def test_repr(self):

        account = TelegramAuthenticationAccount(
            "app_id",
            {
                "key1": "value1"
            },
            1234,
            11
        )

        from_repr = AuthenticationAccount.from_repr(account.to_repr())
        self.assertIsInstance(from_repr, TelegramAuthenticationAccount)
        self.assertEqual(account, from_repr)


class TestWeNetUserWithAccounts(TestCase):

    def test_repr(self):
        wenet_user_with_accounts = WeNetUserWithAccounts(11)

        wenet_user_with_accounts.with_account(
            TelegramAuthenticationAccount(
                "app_id",
                {
                    "key1": "value1"
                },
                1234,
                11
            )
        )

        from_repr = WeNetUserWithAccounts.from_repr(wenet_user_with_accounts.to_repr())

        self.assertIsInstance(from_repr, WeNetUserWithAccounts)
        self.assertEqual(wenet_user_with_accounts, from_repr)
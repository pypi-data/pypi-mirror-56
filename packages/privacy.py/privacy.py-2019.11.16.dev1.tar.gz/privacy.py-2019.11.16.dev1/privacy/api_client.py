"""The main client of this module."""
from typing import Iterable


from privacy.http_client import HTTPClient, Routes
from privacy.schema.card import Card, SpendLimitDuration, State, Type
from privacy.schema.transaction import Transaction
from privacy.schema.embed import EmbedRequest
from privacy.util.functional import b64_encode, hmac_sign, optional
from privacy.util.logging import LoggingClass


def auth_header(api_key=None) -> dict:
    """Optionally overwrite authorisation header for a single request."""
    return optional(Authorization=api_key)


class APIClient(LoggingClass):
    """
    The client used for using Privacy.com's restful api endpoints.

    Attributes:
        api (privacy.http_client.HTTPClient): The client used for making requests.
    """
    def __init__(
            self, api_key: str = None,
            backoff: bool = True, sandboxed: bool = False) -> None:
        """
        Args:
            api_key (str, optional): Used to set the default authorisation.
            sandboxed (bool, optional): Used to enable Privacy's sandboxed api.
            backoff (bool, optional): Used to disable toggle retry on status codes 5xx or 429.
                Will raises `privacy.http_client.APIException` instead of retrying if False.
        """
        self.api = HTTPClient(api_key=api_key, backoff=backoff, sandboxed=sandboxed)

    def update_api_key(self, api_key: str = None) -> None:
        """
        Update or unset the default authorisation key used by an initiated client.

        Args:
            api_key (str, optional): The key used for authentication, will unset if not passed.
        """
        if api_key:
            self.api.session.headers["Authorization"] = "api-key " + api_key
        else:
            self.api.session.headers.pop("Authorization", None)

    def get_api_key(self) -> str:
        """
        Get the set api key.

        Returns:
            str: Api key.

        Raises:
            TypeError: If api authentication key is unset.
        """
        api_key = self.api.session.headers.get("Authorization")
        if not api_key:
            raise TypeError("Api authentication key is unset.")

        return api_key.replace("api-key ", "")

    def cards_list(
            self, token: str = None, page: int = None, page_size: int = None,
            begin: str = None, end: str = None, api_key: str = None) -> Iterable[Card]:
        """
        Get an iterator of the cards owned by this account.

        Args:
            token (str, optional): Used to get a specific card.
            page (str, optional): Used to specify the start page.
            page_size (str, optional): Used to specify the page size.
            begin (str, optional): The start date of the results as a date string (`YYYY-MM-DD`).
            end (str, optional): The end date of the results as a date string (`YYYY-MM-DD`).
            api_key (str, optional): Used to override authentication.

        Returns:
            `privacy.util.pagination.PaginatedResponse` [ `privacy.schema.card.Card` ]

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        return Card.paginate(
            self,
            Routes.CARDS_LIST,
            headers=auth_header(api_key),
            params=optional(
                card_token=token,
                page=page,
                page_size=page_size,
                begin=begin,
                end=end,
            )
        )

    def transactions_list(
            self, approval_status: str = "all", token: str = None,
            card_token: str = None, page: int = None, page_size: int = None,
            begin: str = None, end: str = None, api_key: str = None) -> Iterable[Transaction]:
        """
        Get an iterator of the transactions under this account.

        Args:
            approval_status (str, optional): One of [`approvals`, `declines`, `all`] used to
                get transactions with a specific status.
            token (str, optional): Used to get a specific transaction.
            card_token (str, optional): Used to get the transactions associated with a specific card.
            page (int, optional): Used to specify the start page.
            page_size (int, optional): Used to specify the page size.
            begin (str, optional): The starting date of the results as a date string (`YYYY-MM-DD`).
            end (str, optional): The end date of the results as a date string (`YYYY-MM-DD`).
            api_key (str, optional): Used to override authentication.

        Returns:
            `privacy.util.pagination.PaginatedResponse`[ `privacy.schema.transaction.Transaction` ]

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        return Transaction.paginate(
            self,
            Routes.TRANSACTIONS_LIST,
            dict(approval_status=approval_status),
            headers=auth_header(api_key),
            params=optional(
                transaction_token=token,
                card_token=card_token,
                page=page,
                page_size=page_size,
                begin=begin,
                end=end,
            )
        )

    # Premium
    def cards_create(
            self, card_type: Type, memo: str = None,
            spend_limit: int = None,
            spend_limit_duration: SpendLimitDuration = None,
            api_key=None) -> Card:
        """
        PREMIUM ENDPOINT - Create a card.

        Args:
            card_type (privacy.schema.card.Type): The card type.
            memo (str, optional): The card's name.
            spend_limit (int, optional): The spending limit of the card (in pennies).
            spend_limit_duration (privacy.schema.card.SpendLimitDuration, optional): The spend limit duration.
            api_key (str, optional): Used to override authentication.

        Returns:
            `privacy.schema.card.Card`

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        request = self.api(
            Routes.CARDS_CREATE,
            headers=auth_header(api_key),
            json=optional(
                type=card_type,
                memo=memo,
                spend_limit=spend_limit,
                spend_limit_duration=spend_limit_duration,
            )
        )
        return Card(client=self.api, **request.json())

    def cards_modify(
            self, token: str, state: State = None,
            memo: str = None, spend_limit: int = None,
            spend_limit_duration: SpendLimitDuration = None,
            api_key: str = None) -> Card:
        """
        PREMIUM ENDPOINT - Modify an existing card.

        Args:
            token (str): The unique token of the card being modified.
            state (privacy.schema.card.State, optional): The new card state.
            memo (str, optional): The name card name.
            spend_limit (int, optional): The new card spend limit (in pennies).
            spend_limit_duration (privacy.schema.card.SpendLimitDuration, optional): The spend limit duration.
            api_key (str, optional): Used to override authentication.

        Returns:
            `privacy.schema.card.Card`

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.

        Note:
            Setting state to `privacy.schema.card.State.CLOSED` cannot be undone.
        """
        request = self.api(
            Routes.CARDS_MODIFY,
            headers=auth_header(api_key),
            json=optional(
                card_token=token,
                state=state,
                memo=memo,
                spend_limit=spend_limit,
                spend_limit_duration=spend_limit_duration,
            )
        )
        return Card(client=self.api, **request.json())

    def hoisted_card_ui_get(
            self, embed_request: EmbedRequest, api_key: str = None) -> str:
        """
        PREMIUM ENDPOINT - get a hosted card UI

        Args:
            embed_request (privacy.schema.embed.EmbedRequest): The embed request.
            api_key (str, optional): Used to override authentication.

        Returns:
            str: The iframe body.

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        api_key = api_key or self.get_api_key()

        embed_request_json = embed_request.json()
        embed_request = b64_encode(bytes(embed_request_json, "utf-8"))
        embed_request_hmac = hmac_sign(api_key, embed_request)

        return self.api(
            Routes.HOSTED_CARD_UI_GET,
            headers=auth_header(api_key),
            json=dict(embed_request=embed_request, hmac=embed_request_hmac),
        ).content

    # Sandbox
    def auth_simulate(
            self, descriptor: str, pan: str,
            amount: int, api_key: str = None) -> dict:
        """
        SANDBOX ENDPOINT - Simulate an auth request from a merchant acquirer.

        Args:
            descriptor (str): The merchant's descriptor.
            pan (str): The 16 digit card number.
            amount (int): The amount to authorise (in pennies).
            api_key (str): Used to override authentication.

        Returns:
            dict: {"token": str}

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        return self.api(
            Routes.SIMULATE_AUTH,
            headers=auth_header(api_key),
            json=dict(
                descriptor=descriptor,
                pan=pan,
                amount=amount,
            )
        ).json()

    def void_simulate(
            self, token: str, amount: int, api_key: str = None) -> None:
        """
        SANDBOX ENDPOINT - Void an existing, uncleared/pending authorisation.

        Args:
            token (str): The transaction token returned by Routes.SIMULATE_AUTH.
            amount (int): The amount to void (in pennies).
                Can be less than or equal to original authorisation.
            api_key (str): Used to override authentication.

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        self.api(
            Routes.SIMULATE_VOID,
            headers=auth_header(api_key),
            json=dict(token=token, amount=amount),
        )

    def clearing_simulate(
            self, token: str, amount: int, api_key: str = None) -> None:
        """
        SANDBOX ENDPOINT - Clear an existing authorisation.

        Args:
            token (str): The transaction token returned by Routes.SIMULATE_AUTH.
            amount (int): The amount to complete (in pennies).
                Can be less than or equal to original authorisation.
            api_key (str): Used to override authentication.

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        self.api(
            Routes.SIMULATE_CLEARING,
            headers=auth_header(api_key),
            json=dict(token=token, amount=amount),
        )

    def return_simulate(
            self, descriptor: str, pan: str,
            amount: int, api_key: str = None) -> dict:
        """
        SANDBOX ENDPOINT - Return/refund an amount back to a card.

        Args:
            descriptor (str): The merchant's descriptor.
            pan (str): A 16 digit card number.
            amount (int): The amount to return to the card (in pennies).
                Can be less than or equal to original authorisation.
            api_key (str, optional): Used to override authentication.

        Returns:
            dict: {"token": str}

        Raises:
            APIException (privacy.http_client.APIException): On status code 5xx and certain 429s.
            TypeError: If api authentication key is unset.
        """
        return self.api(
            Routes.SIMULATE_RETURN,
            headers=auth_header(api_key),
            json=dict(
                descriptor=descriptor,
                pan=pan,
                amount=amount,
            )
        ).json()

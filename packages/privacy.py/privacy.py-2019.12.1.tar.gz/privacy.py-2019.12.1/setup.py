# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['privacy', 'privacy.schema', 'privacy.util']

package_data = \
{'': ['*']}

install_requires = \
['pydantic==1.0', 'requests==2.22.0']

setup_kwargs = {
    'name': 'privacy.py',
    'version': '2019.12.1',
    'description': 'A Python lib for Privacy.com',
    'long_description': '# Privacy.py\nA Python wrapper for the [Privacy API](https://developer.privacy.com/).\n\n## Installation\n\nTo install Privacy.py into your environment, simply run this:\n\n```\npip install Privacy.py\n```\n\n## Usage\n\nPrivacy\'s api has 3 groups of endpoints (which are differentiated by access):\nbasic endpoints, premium endpoints and sandboxed endpoints. \n\n### Basic endpoints\n\nThese endpoints can be access by any account. \n\n```python\nimport privacy\n\nclient = privacy.Client("api-key")  # This supports `with privacy.Client("api-key") as client:`\n\n# Returns an iterator of the cards available to your account (based on optional args).\niter_cards = client.cards_list(\n    token=str,  # The token of a specific card (will still return an iterator of either 1 or 0 object(s)).\n    begin="YYYY-MM-DD",  # Used to get cards that were created after the specified date.\n    end="YYYY-MM-DD",  # Used to get cards that were created before the specified date.\n)\n\n# Returns an iterator of the transactions related to your account (based on optional args).\niter_transactions = client.transactions_list(\n    approval_status="all",  # Used to only get transactions with a specific status.\n                            # Can be `approvals`, `declines` or `all` and defaults to `all`.\n    token=str,  # Used to get a specific transaction (will still return an iterator if passed).\n    card_token=str,  # Used to get transactions related to a specific card.\n    begin="YYYY-MM-DD",   # Used to get transactions that were created after the specified date.\n    end="YYYY-MM-DD",  # Used to get transactions that were created before the specified date.\n)\n# With this being mirrored by the following function on the Card object.\niter_transactions = Card.get_transactions(*, **)  # Where card_token is from card this is attached to.\n```\n\n### Premium endpoints. \n\nThese endpoints can only be accessed by premium accounts. \n\n```python\n# Used to create a card.\ncard = client.cards_create(\n    card_type=privacy.schema.card.Type,  # The card type.\n    memo=str,  # An optional card name.\n    spend_limit=int,  # An optional spend limit (in pennies).\n    spend_limit_duration=privacy.schema.card.SpendLimitDuration,  # Optional, used to set how long the spend limit lasts.\n)\n\n# Used to modify a card based on it\'s token and optional args.\ncard = client.cards_modify(\n    token=str,  # The token of the card being modified.\n    state=privacy.schema.CardStates,  # Used to change the state of the card (cannot be reversed when set to `CLOSED`).\n    memo=str,  # Used to change the name of the card.\n    spend_limit=int,  # Used to change spend limit for the card (in pennies).\n    spend_limit_duration=privacy.schema.card.SpendLimitDuration,  # Used to change how long the spend limit lasts.\n)\n# With this being mirrored by the following function on the Card object.\ncard.update(*, **)  # Where the token used is from the card this is attached to.\n\n# Used to get a hosted card UI.\nclient.hoisted_card_ui_get(\n    embed_request=privacy.schema.embed.EmbedRequest,  # An embed request object.\n)\n```\n\n### Sandboxed endponts\n\nThe endpoints can only be accessed on Privacy\'s separate sandboxed api\n(switched to by passing `sandboxed=True` through to `privacy.Client.__init__`).\n\n* Any changes made on these endpoints won\'t effect Privacy\'s actual service as these exist purely for debugging purposes.\n\n* These endpoints can be accessed using `client.[auth_simulate, void_simulate, clearing_simulate, return_simulate]`.\n',
    'author': 'FasterSpeeding',
    'author_email': 'Luke@lmbyrne.dev',
    'url': 'https://github.com/FasterSpeeding/Privacy.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)

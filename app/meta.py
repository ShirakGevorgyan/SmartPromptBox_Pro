"""Runtime metadata for the bot.

- `BOT_NAME` and `BOT_VERSION` can be overridden via environment variables
    and are displayed by the `/about` command.
- `STARTED_AT` is used to compute a simple uptime value.
"""

import os
import time

BOT_NAME = os.getenv("BOT_NAME", "SmartPromptBox Pro")
BOT_VERSION = os.getenv("BOT_VERSION", "0.1.0")
STARTED_AT = time.time()

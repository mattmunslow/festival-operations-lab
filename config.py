"""Loads lab settings from the .env file in this folder."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_setting(name):
    value = os.environ.get(name, "").strip()

    if not value:
        raise SystemExit(
            f"Missing setting: {name}\n"
            "Copy .env.example to .env and fill in every value. "
            "See INSTRUCTIONS.md for where to find each one."
        )

    return value

from dataclasses import dataclass
from typing import Optional


@dataclass
class TelegramUser:
    """Class to represent the information of a Telegram user."""

    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None


@dataclass
class AgentDependencies:
    """Class to be used as dependencies of the agent."""

    user: TelegramUser

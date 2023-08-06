"""Spell events module."""
import re

LEVEL_UP_REGEX = re.compile(
    r'^You have gained a level! Welcome to level (?P<level>\d+)!$')
LEVEL_DOWN_REGEX = re.compile(
    r'^You LOST a level! You are now level (?P<level>\d+)!$')


class NewLevelEvent():
    """A new level event."""
    __slots__ = ('level')

    @classmethod
    def create_events(cls, client, line):
        """Parses every log line, and returns new events to be tracked."""
        level_up_match = LEVEL_UP_REGEX.match(line.message)
        if level_up_match is not None:
            level = int(level_up_match.group('level'))
            level = max(1, min(60, level))
            client.send_event(NewLevelEvent(level))

        level_down_match = LEVEL_DOWN_REGEX.match(line.message)
        if level_down_match is not None:
            level = int(level_down_match.group('level'))
            level = max(1, min(60, level))
            client.send_event(NewLevelEvent(level))

    def __init__(self, level):
        """Create a new spell effect."""
        self.level = level

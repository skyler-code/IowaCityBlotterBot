from enum import IntEnum


class TweetResult(IntEnum):
    IGNORED = 5
    ERROR = 6
    NOTWEETS = 600
    SENT = 900
from dataclasses import dataclass


@dataclass
class Video:
    channel_username: str
    video_id: str
    video_href: str

    def to_tuple(self):
        return (
            self.channel_username,
            self.video_id,
            self.video_href
        )

"""
Supplemental metadata structure:

{
  "title": "image.jpg",
  "description": "",
  "imageViews": "9",
  "creationTime": {
    "timestamp": "1639897853",
    "formatted": "19 déc. 2021, 07:10:53 UTC"
  },
  "photoTakenTime": {
    "timestamp": "1580467879",
    "formatted": "31 janv. 2020, 10:51:19 UTC"
  },
  "geoData": {
    "latitude": 0.0,
    "longitude": 0.0,
    "altitude": 0.0,
    "latitudeSpan": 0.0,
    "longitudeSpan": 0.0
  },
  "url": "https://photos.google.com/photo/xxx",
  "googlePhotosOrigin": {
    "mobileUpload": {
      "deviceType": "ANDROID_PHONE"
    }
  }
}
"""

from dataclasses import dataclass
from datetime import datetime
from datetime import timezone


@dataclass
class SupplementalMetadata:
    """Dataclass for supplemental JSON metadata from Google Photos takeout."""

    photo_taken_time: datetime

    @classmethod
    def from_json(cls, data: dict) -> "SupplementalMetadata":
        photo_taken_timestamp = int(data["photoTakenTime"]["timestamp"])
        creation_timestamp = int(data["creationTime"]["timestamp"])

        if photo_taken_timestamp > creation_timestamp:
            raise ValueError(
                f"photoTakenTime ({photo_taken_timestamp}) must be before or equal to "
                f"creationTime ({creation_timestamp})"
            )

        return cls(photo_taken_time=datetime.fromtimestamp(photo_taken_timestamp, tz=timezone.utc))

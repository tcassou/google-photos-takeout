"""
Supplemental metadata structure:

{
  "title": "IMG_20180318_222735.jpg",
  "description": "",
  "imageViews": "0",
  "creationTime": {
    "timestamp": "1521646620",
    "formatted": "21 mars 2018, 15:37:00 UTC"
  },
  "photoTakenTime": {
    "timestamp": "1521408455",
    "formatted": "18 mars 2018, 21:27:35 UTC"
  },
  "geoData": {
    "latitude": 52.3711184,
    "longitude": 4.8390853,
    "altitude": 83.0,
    "latitudeSpan": 0.0,
    "longitudeSpan": 0.0
  },
  "geoDataExif": {
    "latitude": 52.3711184,
    "longitude": 4.8390853,
    "altitude": 83.0,
    "latitudeSpan": 0.0,
    "longitudeSpan": 0.0
  },
  "url": "https://photos.google.com/photo/xxx",
  "googlePhotosOrigin": {
    "mobileUpload": {
      "deviceFolder": {
        "localFolderName": ""
      },
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
    latitude: float
    longitude: float
    altitude: float
    latitude_span: float
    longitude_span: float

    @classmethod
    def from_json(cls, data: dict) -> "SupplementalMetadata":
        photo_taken_timestamp = int(data["photoTakenTime"]["timestamp"])
        creation_timestamp = int(data["creationTime"]["timestamp"])

        if photo_taken_timestamp > creation_timestamp:
            raise ValueError(
                f"photoTakenTime ({photo_taken_timestamp}) must be before or equal to "
                f"creationTime ({creation_timestamp})"
            )

        return cls(
            photo_taken_time=datetime.fromtimestamp(photo_taken_timestamp, tz=timezone.utc),
            latitude=data["geoData"]["latitude"],
            longitude=data["geoData"]["longitude"],
            altitude=data["geoData"]["altitude"],
            latitude_span=data["geoData"]["latitudeSpan"],
            longitude_span=data["geoData"]["longitudeSpan"],
        )

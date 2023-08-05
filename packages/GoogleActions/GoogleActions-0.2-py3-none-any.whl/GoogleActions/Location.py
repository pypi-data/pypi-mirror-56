from typing import List

from .LatLng import LatLng
from .PostalAddress import PostalAddress


class Location(dict):
    """
    {
      "coordinates": {
        object(LatLng)
      },
      "formattedAddress": string,
      "zipCode": string,
      "city": string,
      "postalAddress": {
        object(PostalAddress)
      },
      "name": string,
      "phoneNumber": string,
      "notes": string,
      "placeId": string
    }
    """

    def __init__(self, coordinates: LatLng = None, formatted_address: str = None, zip_code: str = None,
                 city: str = None,
                 postal_address: str = None, name: str = None, phone_number: str = None, notes: str = None,
                 place_id: str = None):
        super().__init__()

        if coordinates is not None:
            self['coordinates'] = coordinates

        if formatted_address is not None:
            self['formattedAddress'] = formatted_address

        if zip_code is not None:
            self['zipCode'] = zip_code

        if city is not None:
            self['city'] = city

        if postal_address is not None:
            self['postalAddress'] = postal_address

        if name is not None:
            self['name'] = name

        if phone_number is not None:
            self['phoneNumber'] = phone_number

        if notes is not None:
            self['notes'] = notes

        if place_id is not None:
            self['placeId'] = place_id

    def add_latlng(self, latitude: float, longitude: float) -> LatLng:
        self['coordinates'] = LatLng(latitude=latitude, longitude=longitude)
        return self['coordinates']

    def add_postal_address(self, revision: int = None, region_code: str = None, language_code: str = None,
                           postal_code: str = None,
                           sorting_code: str = None, administrative_area: str = None, locality: str = None,
                           sublocality: str = None,
                           address_lines: List[str] = None, recipients: List[str] = None,
                           organization: str = None) -> PostalAddress:

        self['postalAddress'] = PostalAddress(revision, region_code, language_code, postal_code, sorting_code,
                                              administrative_area, locality, sublocality, address_lines,
                                              recipients, organization)

        return self['postalAddress']

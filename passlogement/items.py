from datetime import date, datetime, timedelta

from pydantic import BaseModel, Field


class Offers(BaseModel):
    id: int
    reference: str = Field(alias="specialId")
    accommodation_type_label: str = Field(alias="accommodationTypeLabel")
    surface: int
    rental_price: float = Field(alias="rentalPrice")
    roommate: int
    dalo: int
    city: str
    address: str
    zipcode: int
    number_candidates_on_offer: int = Field(alias="numberCandidatesOnOffer")
    partner_label: str = Field(alias="partnerLabel")
    date_created: datetime = Field(alias="dateCreated")
    date_updated: datetime = Field(alias="dateUpdated")
    date_validity: date = Field(alias="dateValidity")

    def is_great_offer(self):
        thirty_minutes_ago = datetime.now() - timedelta(minutes=30)
        return (
            self.number_candidates_on_offer < 5
            and self.accommodation_type_label in {"T2", "T3"}
            and self.date_created >= thirty_minutes_ago
        )

    class Config:
        allow_population_by_field_name = True

from __future__ import absolute_import, annotations

import re
from numbers import Number
from typing import List, Optional, Dict, Union

from wenet.model.protocol_norm import ProtocolNorm
from wenet.model.scope import AbstractScopeMappings, Scope
from wenet.model.user.common import Gender, Date
from babel.core import Locale

from wenet.model.user.competence import Competence
from wenet.model.user.material import Material
from wenet.model.user.meaning import Meaning
from wenet.model.user.personal_behaviors import PersonalBehavior
from wenet.model.user.planned_activity import PlannedActivity
from wenet.model.user.relationship import Relationship
from wenet.model.user.relevant_location import RelevantLocation


class CoreWeNetUserProfile:

    class ScopeMappings(AbstractScopeMappings):
        @staticmethod
        def _get_read_scope_mappings() -> Dict[Scope, str]:
            return {

                Scope.ID_READ: "id",
                Scope.BIRTHDATE_READ: "dateOfBirth",
                Scope.GENDER_READ: "gender",
                Scope.NATIONALITY_READ: "nationality",
                Scope.LOCALE_READ: "locale",
                Scope.PHONE_NUMBER_READ: "phoneNumber",
                Scope.EMAIL_READ: "email",
                Scope.AVATAR_READ: "avatar",
                Scope.OCCUPATION_READ: "occupation",
                Scope.NORMS_READ: "norms",
                Scope.ACTIVITIES_READ: "plannedActivities",
                Scope.LOCATIONS_READ: "relevantLocations",
                Scope.RELATIONSHIPS_READ: "relationships",
                Scope.BEHAVIOURS_READ: "personalBehaviors",
                Scope.MATERIALS_READ: "meanings",
                Scope.COMPETENCES_READ: "competences",
                Scope.MEANINGS_READ: "meanings",

                # TODO Legacy scopes, remove before release
                Scope.ID_LEGACY: "id",
                Scope.BIRTHDATE_LEGACY: "dateOfBirth",
                Scope.GENDER_LEGACY: "gender",
                Scope.NATIONALITY_LEGACY: "nationality",
                Scope.LOCALE_LEGACY: "locale",
                Scope.PHONE_NUMBER_LEGACY: "phoneNumber",
                Scope.EMAIL_LEGACY: "email",

            }

    def __init__(self,
                 name: Optional[UserName],
                 date_of_birth: Optional[Date],
                 gender: Optional[Gender],
                 email: Optional[str],
                 phone_number: Optional[str],
                 locale: Optional[str],
                 avatar: Optional[str],
                 nationality: Optional[str],
                 occupation: Optional[str],
                 creation_ts: Optional[Number],
                 last_update_ts: Optional[Number],
                 profile_id: Optional[str],
                 ):
        self.name = name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.phone_number = phone_number
        self.locale = locale
        self.avatar = avatar
        self.nationality = nationality
        self.occupation = occupation
        self.creation_ts = creation_ts
        self.last_update_ts = last_update_ts
        self.profile_id = profile_id

        if name:
            if not isinstance(name, UserName):
                raise TypeError("Name should be a UserName object")
        else:
            self.name = UserName(
                first=None,
                middle=None,
                last=None,
                prefix=None,
                suffix=None
            )
        if date_of_birth:
            if not isinstance(date_of_birth, Date):
                raise TypeError("Date of birth should be a Date")
        if gender:
            if not isinstance(gender, Gender):
                raise TypeError("Gender should be a Gender object")
        if email:
            if not isinstance(email, str):
                raise TypeError("Email should be a string")
            if not self.is_valid_mail(email):
                raise ValueError("[%s] is not a valid email" % email)
        if phone_number:
            if not isinstance(phone_number, str):
                raise TypeError("Phone number should be a string")
        if locale:
            if not isinstance(locale, str):
                raise TypeError("Locale should be a string")
            if not self.is_valid_locale(locale):
                raise ValueError("[%s] is not a valid Locale" % locale)
        if avatar:
            if not isinstance(avatar, str):
                raise TypeError("Avatar should be a string")
        if nationality:
            if not isinstance(nationality, str):
                raise TypeError("Nationality should be a string")

        if occupation:
            if not isinstance(occupation, str):
                raise TypeError("Occupation should be a string")

        if creation_ts:
            if not isinstance(creation_ts, Number):
                raise TypeError("CreationTs should be a Number")
        if last_update_ts:
            if not isinstance(last_update_ts, Number):
                raise TypeError("LastUpdateTs should be a Number")

        if profile_id:
            if not isinstance(profile_id, str):
                raise TypeError("Profile id should be a string")

    def to_repr(self) -> dict:
        return {
            "name": self.name.to_repr() if self.name is not None else None,
            "dateOfBirth": self.date_of_birth.to_repr() if self.date_of_birth is not None else None,
            "gender": self.gender.value if self.gender else None,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "locale": self.locale,
            "avatar": self.avatar,
            "nationality": self.nationality,
            "occupation": self.occupation,
            "_creationTs": self.creation_ts,
            "_lastUpdateTs": self.last_update_ts,
            "id": str(self.profile_id),
        }

    def to_filtered_repr(self, scope_list: List[Scope]) -> dict:
        profile_repr = self.to_repr()

        result = {
            "name": self.name.to_filtered_repr(scope_list) if self.name is not None else None
        }

        for scope in scope_list:
            field = self.ScopeMappings.get_field(scope)
            if field is not None:
                result[field] = profile_repr[field]

        return result

    def to_public_repr(self) -> dict:
        scopes = [
            Scope.ID_READ,
            Scope.FIRST_NAME_READ,
            Scope.LAST_NAME_READ
        ]

        return self.to_filtered_repr(scopes)

    @staticmethod
    def from_repr(raw_data: dict, profile_id: Optional[str] = None) -> CoreWeNetUserProfile:
        if profile_id is None:
            profile_id = raw_data.get("id")

        return CoreWeNetUserProfile(
            name=UserName.from_repr(raw_data["name"]) if raw_data.get("name") is not None else None,
            date_of_birth=Date.from_repr(raw_data["dateOfBirth"]) if raw_data.get("dateOfBirth") is not None else None,
            gender=Gender(raw_data["gender"]) if raw_data.get("gender", None) else None,
            email=raw_data.get("email", None),
            phone_number=raw_data.get("phoneNumber", None),
            locale=raw_data.get("locale", None),
            avatar=raw_data.get("avatar", None),
            nationality=raw_data.get("nationality", None),
            occupation=raw_data.get("occupation", None),
            creation_ts=raw_data.get("_creationTs", None),
            last_update_ts=raw_data.get("_lastUpdateTs", None),
            profile_id=profile_id
        )

    def update(self, other: CoreWeNetUserProfile) -> CoreWeNetUserProfile:
        self.profile_id = other.profile_id
        self.name = other.name
        self.date_of_birth = other.date_of_birth
        self.gender = other.gender
        self.email = other.email
        self.phone_number = other.phone_number
        self.locale = other.locale
        self.avatar = other.avatar
        self.nationality = other.nationality
        self.occupation = other.occupation
        self.creation_ts = other.creation_ts
        self.last_update_ts = other.last_update_ts

        return self

    @staticmethod
    def is_valid_mail(mail: str):
        reg_exp = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w+)+$"
        return re.search(reg_exp, mail)

    @staticmethod
    def is_valid_locale(locale: str) -> bool:
        try:
            Locale.parse(locale)
            return True
        except ValueError:
            return False

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o) -> bool:
        if not isinstance(o, CoreWeNetUserProfile):
            return False
        return self.name == o.name and self.date_of_birth == o.date_of_birth and self.gender == o.gender and self.email == o.email \
            and self.phone_number == o.phone_number and self.locale == o.locale and self.avatar == o.avatar and self.nationality == o.nationality \
            and self.occupation == o.occupation and self.creation_ts == o.creation_ts and self.last_update_ts == o.last_update_ts \
            and self.profile_id == o.profile_id

    @staticmethod
    def empty(wenet_user_id: str) -> CoreWeNetUserProfile:
        return CoreWeNetUserProfile(
            name=UserName.empty(),
            date_of_birth=Date.empty(),
            gender=None,
            email=None,
            phone_number=None,
            locale=None,
            avatar=None,
            nationality=None,
            occupation=None,
            creation_ts=None,
            last_update_ts=None,
            profile_id=wenet_user_id
        )


class WeNetUserProfile(CoreWeNetUserProfile):

    def __init__(self,
                 name: Optional[UserName],
                 date_of_birth: Optional[Date],
                 gender: Optional[Gender],
                 email: Optional[str],
                 phone_number: Optional[str],
                 locale: Optional[str],
                 avatar: Optional[str],
                 nationality: Optional[str],
                 occupation: Optional[str],
                 creation_ts: Optional[Number],
                 last_update_ts: Optional[Number],
                 profile_id: Optional[str],
                 norms: Optional[Union[List[dict], List[ProtocolNorm]]],
                 planned_activities: Optional[Union[List[dict], List[PlannedActivity]]],
                 relevant_locations: Optional[Union[List[dict], List[RelevantLocation]]],
                 relationships: Optional[Union[List[dict], List[Relationship]]],
                 personal_behaviours: Optional[Union[List[dict], List[PersonalBehavior]]],
                 materials: Optional[Union[List[dict], List[Material]]],
                 competences: Optional[Union[List[dict], List[Competence]]],
                 meanings: Optional[Union[List[dict], List[Meaning]]]
                 ):

        super().__init__(
            name=name,
            date_of_birth=date_of_birth,
            gender=gender,
            email=email,
            phone_number=phone_number,
            locale=locale,
            avatar=avatar,
            nationality=nationality,
            occupation=occupation,
            creation_ts=creation_ts,
            last_update_ts=last_update_ts,
            profile_id=profile_id
        )
        self.norms = norms
        self.planned_activities = planned_activities
        self.relevant_locations = relevant_locations
        self.relationships = relationships
        self.personal_behaviours = personal_behaviours
        self.materials = materials
        self.competences = competences
        self.meanings = meanings

        if norms:
            if not isinstance(norms, list):
                raise TypeError("Norms should be a list")
        else:
            self.norms = []

        if materials:
            if not isinstance(materials, list):
                raise TypeError("Materials should be a list")
        else:
            self.materials = []

        if competences:
            if not isinstance(competences, list):
                raise TypeError("Competences should be a list")
        else:
            self.competences = []

        if meanings:
            if not isinstance(meanings, list):
                raise TypeError("Meanings should be a list")
        else:
            self.meanings = []

        if planned_activities:
            if not isinstance(planned_activities, list):
                raise TypeError("PlannedActivities should be a list")
        else:
            self.planned_activities = []

        if relevant_locations:
            if not isinstance(relevant_locations, list):
                raise TypeError("RelevantLocations should be a list")
        else:
            self.relevant_locations = []

        if relationships:
            if not isinstance(relationships, list):
                raise TypeError("Relationship should be a list")
        else:
            self.relationships = []

        if personal_behaviours:
            if not isinstance(personal_behaviours, list):
                raise TypeError("personalBehaviors should be a list")
        else:
            self.personal_behaviours = []

    def to_repr(self) -> dict:
        raw_norms = [norm.to_repr() if isinstance(norm, ProtocolNorm) else norm for norm in self.norms] if self.norms is not None else None
        raw_planned_activities = [planned_activity.to_repr() if isinstance(planned_activity, PlannedActivity) else planned_activity for planned_activity in self.planned_activities] if self.planned_activities is not None else None
        raw_relevant_locations = [relevant_location.to_repr() if isinstance(relevant_location, RelevantLocation) else relevant_location for relevant_location in self.relevant_locations] if self.relevant_locations is not None else None
        raw_relationships = [relationship.to_repr() if isinstance(relationship, Relationship) else relationship for relationship in self.relationships] if self.relationships is not None else None
        raw_personal_behaviors = [personal_behavior.to_repr() if isinstance(personal_behavior, PersonalBehavior) else personal_behavior for personal_behavior in self.personal_behaviours] if self.personal_behaviours is not None else None
        raw_materials = [material.to_repr() if isinstance(material, Material) else material for material in self.materials] if self.materials is not None else None
        raw_competences = [competence.to_repr() if isinstance(competence, Competence) else competence for competence in self.competences] if self.competences is not None else None
        raw_meanings = [meaning.to_repr() if isinstance(meaning, Meaning) else meaning for meaning in self.meanings] if self.meanings is not None else None

        base_repr = super().to_repr()
        base_repr.update({
            "norms": raw_norms,
            "plannedActivities": raw_planned_activities,
            "relevantLocations": raw_relevant_locations,
            "relationships": raw_relationships,
            "personalBehaviors": raw_personal_behaviors,
            "materials": raw_materials,
            "competences": raw_competences,
            "meanings": raw_meanings
        })

        return base_repr

    @staticmethod
    def from_repr(raw_data: dict, profile_id: Optional[str] = None) -> WeNetUserProfile:

        if profile_id is None:
            profile_id = raw_data.get("id")

        return WeNetUserProfile(
            name=UserName.from_repr(raw_data["name"]) if raw_data.get("name") is not None else None,
            date_of_birth=Date.from_repr(raw_data["dateOfBirth"]) if raw_data.get("dateOfBirth") is not None else None,
            gender=Gender(raw_data["gender"]) if raw_data.get("gender", None) else None,
            email=raw_data.get("email", None),
            phone_number=raw_data.get("phoneNumber", None),
            locale=raw_data.get("locale", None),
            avatar=raw_data.get("avatar", None),
            nationality=raw_data.get("nationality", None),
            occupation=raw_data.get("occupation", None),
            creation_ts=raw_data.get("_creationTs", None),
            last_update_ts=raw_data.get("_lastUpdateTs", None),
            profile_id=profile_id,
            norms=raw_data["norms"] if raw_data.get("norms", None) else None,
            planned_activities=raw_data.get("plannedActivities", None),
            relevant_locations=raw_data.get("relevantLocations", None),
            relationships=raw_data.get("relationships", None),
            personal_behaviours=raw_data.get("personalBehaviors", None),
            materials=raw_data.get("materials", None),
            competences=raw_data.get("competences", None),
            meanings=raw_data.get("meanings", None)
        )

    @property
    def norms_as_objects(self) -> Optional[List[ProtocolNorm]]:
        """
        Returns the norms attribute as a list of ProtocolNorm objects
        """
        return [ProtocolNorm.from_repr(norm) if isinstance(norm, dict) else norm for norm in self.norms] if self.norms is not None else None

    @property
    def planned_activities_as_objects(self) -> Optional[List[PlannedActivity]]:
        """
        Returns the norms attribute as a list of PlannedActivity objects
        """
        return [PlannedActivity.from_repr(planned_activity) if isinstance(planned_activity, dict) else planned_activity for planned_activity in self.planned_activities] if self.planned_activities is not None else None

    @property
    def relevant_locations_as_objects(self) -> Optional[List[RelevantLocation]]:
        """
        Returns the norms attribute as a list of RelevantLocation objects
        """
        return [RelevantLocation.from_repr(relevant_location) if isinstance(relevant_location, dict) else relevant_location for relevant_location in self.relevant_locations] if self.relevant_locations is not None else None

    @property
    def relationships_objects(self) -> Optional[List[Relationship]]:
        """
        Returns the norms attribute as a list of Relationship objects
        """
        return [Relationship.from_repr(relationship) if isinstance(relationship, dict) else relationship for relationship in self.relationships] if self.relationships is not None else None

    @property
    def personal_behaviours_as_objects(self) -> Optional[List[PersonalBehavior]]:
        """
        Returns the norms attribute as a list of PersonalBehavior objects
        """
        return [PersonalBehavior.from_repr(personal_behavior) if isinstance(personal_behavior, dict) else personal_behavior for personal_behavior in self.personal_behaviours] if self.personal_behaviours is not None else None

    @property
    def materials_as_objects(self) -> Optional[List[Material]]:
        """
        Returns the norms attribute as a list of Material objects
        """
        return [Material.from_repr(material) if isinstance(material, dict) else material for material in self.materials] if self.materials is not None else None

    @property
    def competences_as_objects(self) -> Optional[List[Competence]]:
        """
        Returns the norms attribute as a list of Competence objects
        """
        return [Competence.from_repr(competence) if isinstance(competence, dict) else competence for competence in self.competences] if self.competences is not None else None

    @property
    def meanings_as_objects(self) -> Optional[List[Meaning]]:
        """
        Returns the norms attribute as a list of Meaning objects
        """
        return [Meaning.from_repr(meaning) if isinstance(meaning, dict) else meaning for meaning in self.meanings] if self.meanings is not None else None

    def update(self, other: CoreWeNetUserProfile) -> WeNetUserProfile:

        super().update(other)

        if isinstance(other, WeNetUserProfile):
            self.norms = other.norms
            self.planned_activities = other.planned_activities
            self.relevant_locations = other.relevant_locations
            self.relationships = other.relationships
            self.personal_behaviours = other.personal_behaviours
            self.materials = other.materials
            self.competences = other.competences
            self.meanings = other.meanings

        return self

    def __eq__(self, o):
        if not isinstance(o, WeNetUserProfile):
            return False
        return super().__eq__(o) and self.norms == o.norms and self.planned_activities == o.planned_activities \
            and self.relevant_locations == o.relevant_locations and self.relationships == o.relationships \
            and self.personal_behaviours == o.personal_behaviours and self.materials == o.materials \
            and self.competences == o.competences and self.meanings == o.meanings

    @staticmethod
    def empty(wenet_user_id: str) -> WeNetUserProfile:
        return WeNetUserProfile(
            name=UserName.empty(),
            date_of_birth=Date.empty(),
            gender=None,
            email=None,
            phone_number=None,
            locale=None,
            avatar=None,
            nationality=None,
            occupation=None,
            creation_ts=None,
            last_update_ts=None,
            profile_id=wenet_user_id,
            norms=None,
            planned_activities=None,
            relevant_locations=None,
            relationships=None,
            personal_behaviours=None,
            materials=None,
            competences=None,
            meanings=None
        )

    @staticmethod
    def create_from_core_profile(profile: CoreWeNetUserProfile) -> WeNetUserProfile:
        return WeNetUserProfile(
            name=profile.name,
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            email=profile.email,
            phone_number=profile.phone_number,
            locale=profile.locale,
            avatar=profile.avatar,
            nationality=profile.nationality,
            occupation=profile.occupation,
            creation_ts=profile.creation_ts,
            last_update_ts=profile.last_update_ts,
            profile_id=profile.profile_id,
            norms=None,
            planned_activities=None,
            relevant_locations=None,
            relationships=None,
            personal_behaviours=None,
            materials=None,
            competences=None,
            meanings=None
        )


class PatchWeNetUserProfile(CoreWeNetUserProfile):

    def __init__(self,
                 profile_id: str,
                 name: Optional[UserName] = None,
                 date_of_birth: Optional[Date] = None,
                 gender: Optional[Gender] = None,
                 email: Optional[str] = None,
                 phone_number: Optional[str] = None,
                 locale: Optional[str] = None,
                 avatar: Optional[str] = None,
                 nationality: Optional[str] = None,
                 occupation: Optional[str] = None,
                 creation_ts: Optional[Number] = None,
                 last_update_ts: Optional[Number] = None,
                 norms: Optional[Union[List[dict], List[ProtocolNorm]]] = None,
                 planned_activities: Optional[Union[List[dict], List[PlannedActivity]]] = None,
                 relevant_locations: Optional[Union[List[dict], List[RelevantLocation]]] = None,
                 relationships: Optional[Union[List[dict], List[Relationship]]] = None,
                 personal_behaviours: Optional[Union[List[dict], List[PersonalBehavior]]] = None,
                 materials: Optional[Union[List[dict], List[Material]]] = None,
                 competences: Optional[Union[List[dict], List[Competence]]] = None,
                 meanings: Optional[Union[List[dict], List[Meaning]]] = None
                 ):

        super().__init__(
            name=name,
            date_of_birth=date_of_birth,
            gender=gender,
            email=email,
            phone_number=phone_number,
            locale=locale,
            avatar=avatar,
            nationality=nationality,
            occupation=occupation,
            creation_ts=creation_ts,
            last_update_ts=last_update_ts,
            profile_id=profile_id,
        )
        self.norms = norms
        self.planned_activities = planned_activities
        self.relevant_locations = relevant_locations
        self.relationships = relationships
        self.personal_behaviours = personal_behaviours
        self.materials = materials
        self.competences = competences
        self.meanings = meanings

        if norms:
            if not isinstance(norms, list):
                raise TypeError("Norms should be a list")

        if materials:
            if not isinstance(materials, list):
                raise TypeError("Materials should be a list")

        if competences:
            if not isinstance(competences, list):
                raise TypeError("Competences should be a list")

        if meanings:
            if not isinstance(meanings, list):
                raise TypeError("Meanings should be a list")

        if planned_activities:
            if not isinstance(planned_activities, list):
                raise TypeError("PlannedActivities should be a list")

        if relevant_locations:
            if not isinstance(relevant_locations, list):
                raise TypeError("RelevantLocations should be a list")

        if relationships:
            if not isinstance(relationships, list):
                raise TypeError("Relationship should be a list")

        if personal_behaviours:
            if not isinstance(personal_behaviours, list):
                raise TypeError("personalBehaviors should be a list")

    def to_repr(self) -> dict:
        raw_norms = [norm.to_repr() if isinstance(norm, ProtocolNorm) else norm for norm in self.norms] if self.norms is not None else None
        raw_planned_activities = [planned_activity.to_repr() if isinstance(planned_activity, PlannedActivity) else planned_activity for planned_activity in self.planned_activities] if self.planned_activities is not None else None
        raw_relevant_locations = [relevant_location.to_repr() if isinstance(relevant_location, RelevantLocation) else relevant_location for relevant_location in self.relevant_locations] if self.relevant_locations is not None else None
        raw_relationships = [relationship.to_repr() if isinstance(relationship, Relationship) else relationship for relationship in self.relationships] if self.relationships is not None else None
        raw_personal_behaviors = [personal_behavior.to_repr() if isinstance(personal_behavior, PersonalBehavior) else personal_behavior for personal_behavior in self.personal_behaviours] if self.personal_behaviours is not None else None
        raw_materials = [material.to_repr() if isinstance(material, Material) else material for material in self.materials] if self.materials is not None else None
        raw_competences = [competence.to_repr() if isinstance(competence, Competence) else competence for competence in self.competences] if self.competences is not None else None
        raw_meanings = [meaning.to_repr() if isinstance(meaning, Meaning) else meaning for meaning in self.meanings] if self.meanings is not None else None

        base_repr = super().to_repr()
        base_repr.update({
            "norms": raw_norms,
            "plannedActivities": raw_planned_activities,
            "relevantLocations": raw_relevant_locations,
            "relationships": raw_relationships,
            "personalBehaviors": raw_personal_behaviors,
            "materials": raw_materials,
            "competences": raw_competences,
            "meanings": raw_meanings
        })

        return base_repr

    @staticmethod
    def from_repr(raw_data: dict, profile_id: Optional[str] = None) -> PatchWeNetUserProfile:

        if profile_id is None:
            profile_id = raw_data.get("id")

        return PatchWeNetUserProfile(
            name=UserName.from_repr(raw_data["name"]) if raw_data.get("name") is not None else None,
            date_of_birth=Date.from_repr(raw_data["dateOfBirth"]) if raw_data.get("dateOfBirth") is not None else None,
            gender=Gender(raw_data["gender"]) if raw_data.get("gender", None) else None,
            email=raw_data.get("email", None),
            phone_number=raw_data.get("phoneNumber", None),
            locale=raw_data.get("locale", None),
            avatar=raw_data.get("avatar", None),
            nationality=raw_data.get("nationality", None),
            occupation=raw_data.get("occupation", None),
            creation_ts=raw_data.get("_creationTs", None),
            last_update_ts=raw_data.get("_lastUpdateTs", None),
            profile_id=profile_id,
            norms=raw_data["norms"] if raw_data.get("norms", None) else None,
            planned_activities=raw_data.get("plannedActivities", None),
            relevant_locations=raw_data.get("relevantLocations", None),
            relationships=raw_data.get("relationships", None),
            personal_behaviours=raw_data.get("personalBehaviors", None),
            materials=raw_data.get("materials", None),
            competences=raw_data.get("competences", None),
            meanings=raw_data.get("meanings", None)
        )

    @property
    def norms_as_objects(self) -> Optional[List[ProtocolNorm]]:
        """
        Returns the norms attribute as a list of ProtocolNorm objects
        """
        return [ProtocolNorm.from_repr(norm) if isinstance(norm, dict) else norm for norm in self.norms] if self.norms is not None else None

    @property
    def planned_activities_as_objects(self) -> Optional[List[PlannedActivity]]:
        """
        Returns the norms attribute as a list of PlannedActivity objects
        """
        return [PlannedActivity.from_repr(planned_activity) if isinstance(planned_activity, dict) else planned_activity for planned_activity in self.planned_activities] if self.planned_activities is not None else None

    @property
    def relevant_locations_as_objects(self) -> Optional[List[RelevantLocation]]:
        """
        Returns the norms attribute as a list of RelevantLocation objects
        """
        return [RelevantLocation.from_repr(relevant_location) if isinstance(relevant_location, dict) else relevant_location for relevant_location in self.relevant_locations] if self.relevant_locations is not None else None

    @property
    def relationships_objects(self) -> Optional[List[Relationship]]:
        """
        Returns the norms attribute as a list of Relationship objects
        """
        return [Relationship.from_repr(relationship) if isinstance(relationship, dict) else relationship for relationship in self.relationships] if self.relationships is not None else None

    @property
    def personal_behaviours_as_objects(self) -> Optional[List[PersonalBehavior]]:
        """
        Returns the norms attribute as a list of PersonalBehavior objects
        """
        return [PersonalBehavior.from_repr(personal_behavior) if isinstance(personal_behavior, dict) else personal_behavior for personal_behavior in self.personal_behaviours] if self.personal_behaviours is not None else None

    @property
    def materials_as_objects(self) -> Optional[List[Material]]:
        """
        Returns the norms attribute as a list of Material objects
        """
        return [Material.from_repr(material) if isinstance(material, dict) else material for material in self.materials] if self.materials is not None else None

    @property
    def competences_as_objects(self) -> Optional[List[Competence]]:
        """
        Returns the norms attribute as a list of Competence objects
        """
        return [Competence.from_repr(competence) if isinstance(competence, dict) else competence for competence in self.competences] if self.competences is not None else None

    @property
    def meanings_as_objects(self) -> Optional[List[Meaning]]:
        """
        Returns the norms attribute as a list of Meaning objects
        """
        return [Meaning.from_repr(meaning) if isinstance(meaning, dict) else meaning for meaning in self.meanings] if self.meanings is not None else None

    def update(self, other: CoreWeNetUserProfile) -> PatchWeNetUserProfile:

        super().update(other)

        if isinstance(other, PatchWeNetUserProfile):
            self.norms = other.norms
            self.planned_activities = other.planned_activities
            self.relevant_locations = other.relevant_locations
            self.relationships = other.relationships
            self.personal_behaviours = other.personal_behaviours
            self.materials = other.materials
            self.competences = other.competences
            self.meanings = other.meanings

        return self

    def __eq__(self, o):
        if not isinstance(o, PatchWeNetUserProfile):
            return False
        return super().__eq__(o) and self.norms == o.norms and self.planned_activities == o.planned_activities \
            and self.relevant_locations == o.relevant_locations and self.relationships == o.relationships \
            and self.personal_behaviours == o.personal_behaviours and self.materials == o.materials \
            and self.competences == o.competences and self.meanings == o.meanings

    @staticmethod
    def empty(wenet_user_id: str) -> PatchWeNetUserProfile:
        return PatchWeNetUserProfile(
            name=UserName.empty(),
            date_of_birth=Date.empty(),
            gender=None,
            email=None,
            phone_number=None,
            locale=None,
            avatar=None,
            nationality=None,
            occupation=None,
            creation_ts=None,
            last_update_ts=None,
            profile_id=wenet_user_id,
            norms=None,
            planned_activities=None,
            relevant_locations=None,
            relationships=None,
            personal_behaviours=None,
            materials=None,
            competences=None,
            meanings=None
        )

    @staticmethod
    def create_from_core_profile(profile: CoreWeNetUserProfile) -> PatchWeNetUserProfile:
        return PatchWeNetUserProfile(
            name=profile.name,
            date_of_birth=profile.date_of_birth,
            gender=profile.gender,
            email=profile.email,
            phone_number=profile.phone_number,
            locale=profile.locale,
            avatar=profile.avatar,
            nationality=profile.nationality,
            occupation=profile.occupation,
            creation_ts=profile.creation_ts,
            last_update_ts=profile.last_update_ts,
            profile_id=profile.profile_id,
            norms=None,
            planned_activities=None,
            relevant_locations=None,
            relationships=None,
            personal_behaviours=None,
            materials=None,
            competences=None,
            meanings=None
        )

    def to_patch(self) -> dict:
        """
        The keys with values set to None will not be present in the representation for the patch method
        """
        base_repr = self.to_repr()
        return {key: base_repr[key] for key in base_repr if base_repr[key] is not None}


class UserName:

    class ScopeMappings(AbstractScopeMappings):
        @staticmethod
        def _get_read_scope_mappings() -> Dict[Scope, str]:
            return {

                Scope.FIRST_NAME_READ: "first",
                Scope.MIDDLE_NAME_READ: "middle",
                Scope.LAST_NAME_READ: "last",
                Scope.PREFIX_NAME_READ: "prefix",
                Scope.SUFFIX_NAME_READ: "suffix",

                # TODO legacy scopes, remove before release
                Scope.FIRST_NAME_LEGACY: "first",
                Scope.MIDDLE_NAME_LEGACY: "middle",
                Scope.LAST_NAME_LEGACY: "last",
                Scope.PREFIX_NAME_LEGACY: "prefix",
                Scope.SUFFIX_NAME_LEGACY: "suffix",
            }

    def __init__(self, first: Optional[str], middle: Optional[str], last: Optional[str], prefix: Optional[str], suffix: Optional[str]):
        self.first = first
        self.middle = middle
        self.last = last
        self.prefix = prefix
        self.suffix = suffix

        if first:
            if not isinstance(first, str):
                raise TypeError("First should be a string")
        if middle:
            if not isinstance(middle, str):
                raise TypeError("Middle should be a string")
        if last:
            if not isinstance(last, str):
                raise TypeError("Last should be a string")
        if prefix:
            if not isinstance(prefix, str):
                raise TypeError("Prefix should be a string")
        if suffix:
            if not isinstance(suffix, str):
                raise TypeError("Suffix should be a string")

    def to_repr(self, public_profile: bool = False) -> dict:
        if public_profile:
            return {
                "first": self.first,
                "last": self.last,
            }
        else:
            return {
                "first": self.first,
                "middle": self.middle,
                "last": self.last,
                "prefix": self.prefix,
                "suffix": self.suffix
            }

    def to_filtered_repr(self, scope_list: List[Scope]) -> dict:
        name_repr = self.to_repr()
        result = {}

        for scope in scope_list:
            field = self.ScopeMappings.get_field(scope)
            if field is not None:
                result[field] = name_repr[field]

        return result

    @staticmethod
    def from_repr(raw_data: dict) -> UserName:
        return UserName(
            first=raw_data.get("first", None),
            middle=raw_data.get("middle", None),
            last=raw_data.get("last", None),
            prefix=raw_data.get("prefix", None),
            suffix=raw_data.get("suffix", None)
        )

    @staticmethod
    def empty() -> UserName:
        return UserName(
            first=None,
            middle=None,
            last=None,
            prefix=None,
            suffix=None
        )

    def __repr__(self):
        return str(self.to_repr())

    def __str__(self):
        return self.__repr__()

    def __eq__(self, o):
        if not isinstance(o, UserName):
            return False
        return self.first == o.first and self.middle == o.middle and self.last == o.last and self.prefix == o.prefix and self.suffix == o.suffix


class WeNetUserProfilesPage:

    def __init__(self, offset: int, total: int, profiles: Optional[List[WeNetUserProfile]]):
        """
        Contains a set of profiles, used for the pagination in profiles list requests
        @param offset:
        @param total:
        @param profiles:
        """
        self.offset = offset
        self.total = total
        self.profiles = profiles

        if not isinstance(self.offset, int):
            raise TypeError("offset should be an integer")
        if not isinstance(self.total, int):
            raise TypeError("total should be an integer")
        if self.profiles:
            if isinstance(self.profiles, list):
                for profile in self.profiles:
                    if not isinstance(profile, WeNetUserProfile):
                        raise TypeError("profiles should be a list of WeNetUserProfile")
            else:
                raise TypeError("profiles should be a list of WeNetUserProfile")
        else:
            self.profiles = []

    def to_repr(self) -> dict:
        return {
            "offset": self.offset,
            "total": self.total,
            "profiles": list(x.to_repr() for x in self.profiles)
        }

    @staticmethod
    def from_repr(raw_data: dict) -> WeNetUserProfilesPage:
        profiles = raw_data.get("profiles")
        if profiles:
            profiles = list(WeNetUserProfile.from_repr(x) for x in profiles)
        return WeNetUserProfilesPage(
            offset=raw_data["offset"],
            total=raw_data["total"],
            profiles=profiles
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, WeNetUserProfilesPage):
            return False
        return self.offset == o.offset and self.total == o.total and self.profiles == o.profiles

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()


class UserIdentifiersPage:

    def __init__(self, offset: int, total: int, user_ids: Optional[List[str]]):
        """
        Contains a set of identifiers, used for the pagination in identifiers list requests
        @param offset:
        @param total:
        @param user_ids:
        """
        self.offset = offset
        self.total = total
        self.user_ids = user_ids

        if not isinstance(self.offset, int):
            raise TypeError("offset should be an integer")
        if not isinstance(self.total, int):
            raise TypeError("total should be an integer")
        if self.user_ids:
            if isinstance(self.user_ids, list):
                for user_id in self.user_ids:
                    if not isinstance(user_id, str):
                        raise TypeError("user_ids should be a list of str")
            else:
                raise TypeError("user_ids should be a list of str")
        else:
            self.user_ids = []

    def to_repr(self) -> dict:
        return {
            "offset": self.offset,
            "total": self.total,
            "userIds": self.user_ids
        }

    @staticmethod
    def from_repr(raw_data: dict) -> UserIdentifiersPage:
        return UserIdentifiersPage(
            offset=raw_data["offset"],
            total=raw_data["total"],
            user_ids=raw_data.get("userIds")
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, UserIdentifiersPage):
            return False
        return self.offset == o.offset and self.total == o.total and self.user_ids == o.user_ids

    def __repr__(self) -> str:
        return str(self.to_repr())

    def __str__(self) -> str:
        return self.__repr__()

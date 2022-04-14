from __future__ import absolute_import, annotations

import secrets
import random

from wenet.model.user.relationship import Relationship, RelationType, RelationshipPage


class RelationshipGenerator:

    @staticmethod
    def generate_relationship(user_id: str) -> Relationship:
        return Relationship(
            app_id="app1",
            source_id=user_id,
            target_id=secrets.token_urlsafe(),
            relation_type=random.choice(list(RelationType)),
            weight=random.uniform(0, 1)
        )

    @staticmethod
    def generate_relationship_page(user_id: str, number_of_relationships: int):
        page = RelationshipPage(
            offset=0,
            total=1,
            relationships=[]
        )

        for i in range(0, number_of_relationships):
            page.relationships.append(
                RelationshipGenerator.generate_relationship(user_id)
            )

        return page

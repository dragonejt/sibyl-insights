from abc import ABC, abstractmethod
from typing import override
from dataclasses import dataclass
from json import dumps as to_json, loads as from_json


class Insights(ABC):

    def serialize(self) -> str:
        return to_json(self.__dict__)

    @staticmethod
    @abstractmethod
    def deserialize(insights: dict) -> "Insights":
        raise NotImplementedError


@dataclass
class UserInsights(Insights):
    user_id: str
    psycho_hazard: bool

    @staticmethod
    @override
    def deserialize(insights: dict) -> "UserInsights":
        return UserInsights(
            user_id=insights["user_id"], psycho_hazard=insights["psycho_hazard"]
        )


@dataclass
class CommunityInsights(Insights):
    community_id: str

    @staticmethod
    @override
    def deserialize(insights: dict) -> "CommunityInsights":
        return CommunityInsights(community_id=insights["community_id"])


class InsightsDB:

    def __init__(self, insightsdb) -> None:
        self.db = insightsdb

    async def get_user(self, user_id: str) -> UserInsights:
        insights = from_json(await self.db.get(user_id))
        return UserInsights.deserialize(insights)

    async def put_user(self, user_id: str, user_insights: UserInsights) -> None:
        await self.db.put(user_id, user_insights.serialize())

    async def delete_user(self, user_id: str) -> None:
        await self.db.delete(user_id)

    async def get_community(self, community_id: str) -> CommunityInsights:
        insights = from_json(await self.db.get(community_id))
        return CommunityInsights.deserialize(insights)

    async def put_community(
        self, community_id: str, community_insights: CommunityInsights
    ) -> None:
        await self.db.put(community_id, community_insights.serialize())

    async def delete_community(self, community_id: str) -> None:
        await self.db.delete(community_id)

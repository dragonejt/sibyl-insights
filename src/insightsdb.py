from abc import ABC, abstractmethod
from typing import override
from dataclasses import dataclass
import json


class Insights(ABC):
    def serialize(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    @abstractmethod
    def deserialize(insights: dict) -> "Insights":
        raise NotImplementedError


@dataclass
class UserInsights(Insights):
    user: str
    psycho_hazard: bool

    @staticmethod
    @override
    def deserialize(insights: dict) -> "UserInsights":
        return UserInsights(
            user=insights["user"], psycho_hazard=insights["psycho_hazard"]
        )


@dataclass
class CommunityInsights(Insights):
    community: str

    @staticmethod
    @override
    def deserialize(insights: dict) -> "CommunityInsights":
        return CommunityInsights(community=insights["community"])


class InsightsDB:
    def __init__(self, insightsdb) -> None:
        self.db = insightsdb

    async def get_user(self, user: str) -> UserInsights:
        insights = json.loads(await self.db.get(user))
        return UserInsights.deserialize(insights)

    async def put_user(self, user: str, insights: UserInsights) -> None:
        await self.db.put(user, insights.serialize())

    async def get_community(self, community: str) -> CommunityInsights:
        insights = json.loads(await self.db.get(community))
        return CommunityInsights.deserialize(insights)

    async def put_community(self, community: str, insights: CommunityInsights) -> None:
        await self.db.put(community, insights.serialize())

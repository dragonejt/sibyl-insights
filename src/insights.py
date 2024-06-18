from dataclasses import dataclass
import json


class Insights:
    def serialize(self):
        return json.dumps(self.__dict__)


@dataclass
class UserInsights(Insights):
    user: str
    psycho_hazard: bool


@dataclass
class CommunityInsights(Insights):
    community: str


class InsightsDB:
    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, user: str) -> UserInsights:
        insights = json.loads(self.db.get(user))
        return UserInsights(
            user=insights.get("user"), psycho_hazard=insights.get("psycho_hazard")
        )

    def put_user(self, insights: UserInsights) -> None:
        self.db.put(insights.user, insights.serialize())

    def get_community(self, community: str) -> CommunityInsights:
        insights = json.loads(self.db.get(community))
        return CommunityInsights(community=insights.get("community"))

    def put_community(self, insights: CommunityInsights) -> None:
        self.db.put(insights.community, insights.serialize())

from dataclasses import dataclass
import json


@dataclass
class Insights:
    user: str
    psycho_hazard: bool

    def serialize(self):
        return json.dumps(self.__dict__)

class InsightsDB:
    def __init__(self, db) -> None:
        self.db = db

    def get(self, user: str) -> Insights:
        insights = json.loads(self.db.get(user))
        return Insights(
            user=insights.get("user"),
            psycho_hazard=insights.get("psycho_hazard")
        )

    def put(self, insights: Insights) -> None:
        self.db.put(insights.user, insights.serialize())

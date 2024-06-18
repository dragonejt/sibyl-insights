from js import Response
from insights import InsightsDB


async def on_fetch(request, env):
    insights_db = InsightsDB(env.insightsdb)
    return Response.new("Hello World!")

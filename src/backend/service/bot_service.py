

class BossService:
    def reply(self, query: str) -> str:
        return f"Boss replies to: {query}"


bot_service = BossService()
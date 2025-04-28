import aiohttp
from typing import Optional
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class LocationAgentPlugin:
    """Semantic Kernel Plugin to detect user's location using IP lookup or fallback input."""

    def __init__(self):
        self.api_url = "https://ipinfo.io/json"

    @kernel_function(
        name="get_location",
        description="Fetch the user's location using IP address or fallback location"
    )
    async def get_location(
        self,
        fallback_location: Optional[str] = None
    ) -> dict:
        """Returns the location details of the user as a dictionary."""

        # ✅ Make sure the input is either a string or None
        if fallback_location is not None and not isinstance(fallback_location, str):
            fallback_location = str(fallback_location)

        if fallback_location:
            return {"city": fallback_location, "source": "manual"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        loc = data.get("loc", "")
                        lat, lon = loc.split(",") if loc else ("", "")
                        return {
                            "city": data.get("city", ""),
                            "region": data.get("region", ""),
                            "country": data.get("country", ""),
                            "latitude": lat,
                            "longitude": lon,
                            "source": "ip"
                        }
        except Exception as e:
            print("⚠️ Error fetching location:", e)

        return {"city": "Unknown", "source": "error"}

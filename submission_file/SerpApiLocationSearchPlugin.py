# Updated SerpApiLocationSearchPlugin.py

from semantic_kernel.functions.kernel_function_decorator import kernel_function
import requests

class SerpApiLocationSearchPlugin:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @kernel_function(description="Search nearby places using query and location name. Format: 'query | location | country_code'")
    def search_by_location(self, input_text: str) -> str:
        try:
            query_text, location_name, country_code = [part.strip() for part in input_text.split('|')]

            params = {
                "engine": "google_maps",
                "q": query_text,
                "location": location_name,
                "gl": country_code,
                "hl": "en",
                "google_domain": "google.com",
                "api_key": self.api_key
            }

            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()

            data = response.json()
            results = data.get("local_results", [])
            if not results:
                return f"No results found for '{query_text}' in '{location_name}'."

            # Updated formatting
            formatted_results = []
            for i, r in enumerate(results[:3]):  # Show only top 3 results
                name = r.get('title', 'No name')
                address = r.get('address', 'No address')
                phone = r.get('phone', 'No phone')
                rating = r.get('rating', 'No rating')
                website = r.get('website', 'No website')
                gps = r.get('gps_coordinates', {})
                lat = gps.get('latitude', 'N/A')
                lng = gps.get('longitude', 'N/A')

                # Google Maps link
                maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}" if lat != 'N/A' and lng != 'N/A' else "No map link"

                formatted_results.append(
                    f"🏥 {i+1}. **{name}**\n"
                    f"📍 Address: {address}\n"
                    f"📞 Phone: {phone}\n"
                    f"⭐ Rating: {rating}\n"
                    f"🌐 Website: {website}\n"
                    f"🗺️ Map: {maps_link}\n"
                )

            return "\n\n".join(formatted_results)

        except Exception as e:
            return f"Error: {str(e)}"

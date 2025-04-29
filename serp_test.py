# test_serpapi_location_search.py

from SerpApiLocationSearchPlugin import SerpApiLocationSearchPlugin

def main():
    # Replace with your real SerpApi Key
    SERPAPI_API_KEY = "57d1bf60bf1194e093353ed5ed842f1f51735d45428e33cd877a810e55333cb9"
    
    # Initialize the plugin
    plugin = SerpApiLocationSearchPlugin(api_key=SERPAPI_API_KEY)

    # Example input format: 'query | location | country_code'
    test_input = "hospital | bangalore | IN"

    # Call the search_by_location method
    result = plugin.search_by_location(test_input)

    print("\n=== Test Result ===")
    print(result)

if __name__ == "__main__":
    main()

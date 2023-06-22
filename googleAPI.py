import requests
from googleapiclient.discovery import build

def get_geocoding_and_playlist(message):
    # Geocoding API
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    api_key = "AIzaSyB8nk3--gIZ5D53D7xI8CjJSZIq7b80uVE"  # Replace with your actual API key
    geocoding_params = {
        "address": message,
        "key": api_key
    }
    geocoding_response = requests.get(geocoding_url, params=geocoding_params)
    geocoding_data = geocoding_response.json()

    # Check geocoding status
    if geocoding_data['status'] == "OK":
        location = geocoding_data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        print(f"Latitude: {lat}, Longitude: {lng}")
    else:
        print("Error: Geocoding failed")

    # YouTube Playlist
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_id = "LL"  # Liked List
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id
    )
    response = request.execute()
    favorites = response['items']

    # Print snippet information of the playlist items
    for favorite in favorites:
        snippet = favorite['snippet']
        title = snippet['title']
        description = snippet['description']
        print(f"Title: {title}")
        print(f"Description: {description}")
        print("-----")

# Call the function with a message
get_geocoding_and_playlist("1600 Amphitheatre Parkway, Mountain View, CA")

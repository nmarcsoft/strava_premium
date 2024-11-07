import requests
from pprint import pprint


class API_manager:
    def __init__(self, access_token) -> None:
        self.access_token = access_token
        self.activites = None
        pass

    def get_all_activities(self):
        print(f"access_token = {self.access_token}")
        url = "https://www.strava.com/api/v3/athlete/activities"  # Endpoint for retrieving activities
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "per_page": 30,  # Number of activities to retrieve per page
            "page": 1        # Start with the first page
        }

        try:
            # Make the request to get activities
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            # Display each activity's ID and name
            activities = response.json()
            print("List of recent activities:")
            for activity in activities:
                print(f"ID: {activity['id']}, Name: {activity['name']}, Type: {activity['type']}, Distance: {activity['distance']} meters")
            return activities

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_activity(self, activity_id):
        activity_id = 12805308059  # Replace with your actual activity ID
        url = f"https://www.strava.com/api/v3/activities/{activity_id}"  # Specify activity ID in the URL
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            pprint(response.json())
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except Exception as e:
            print(f"An error occurred: {e}")

import requests

url = "https://api.cien.or.kr:443/api/system/getClubRoomPeopleCount"
response = requests.get(url)
data = response.json()

count = data.get("peopleCount")

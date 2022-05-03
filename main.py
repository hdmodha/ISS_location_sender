import requests
from datetime import datetime
import smtplib
import time

SURAT_LAT = 21.170240
SURAT_LNG = 72.831062

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()
iss_lng = float(data["iss_position"]["longitude"])
iss_lat = float(data["iss_position"]["latitude"])


def position_viable():
    if (SURAT_LNG - 5) <= iss_lng <= (SURAT_LNG + 5) and (SURAT_LAT - 5) <= iss_lat <= (
        SURAT_LAT + 5
    ):
        return True


parameters = {"lat": 21.170240, "lng": 72.831062, "formatted": 0}
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
current_hour = time_now.hour

while True:
    time.sleep(60)
    if position_viable() and (current_hour >= sunset or current_hour <= sunrise):
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.starttls()
            smtp.login(user="<your-email>", password="<your-password>")
            smtp.sendmail(
                from_addr="<your-email>",
                to_addrs="<receiver-email>",
                msg=f"Subject:ISS\n\nLook up you can see International Space station from your location\n"
                f"Longitude of ISS is: {iss_lng}\n"
                f"Latitude of ISS is: {iss_lat}",
            )

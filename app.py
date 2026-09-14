from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def accueil():

    temperature = None
    ville_nom = ""
    image_url = None
    erreur = None

    if request.method == "POST":

        ville_nom = request.form["ville"]

        # -------------------------
        #  API géographique
        # -------------------------

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": ville_nom,
            "count": 1,
            "language": "fr",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params
        )

        geo_data = geo_response.json()

        if "results" not in geo_data:
            erreur = " Ville introuvable"

        else:

            latitude = geo_data["results"][0]["latitude"]
            longitude = geo_data["results"][0]["longitude"]

            # -------------------------
            #  API météo
            # -------------------------

            weather_url = "https://api.open-meteo.com/v1/forecast"

            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m"
            }

            weather_response = requests.get(
                weather_url,
                params=weather_params
            )

            weather_data = weather_response.json()

            temperature = weather_data["current"]["temperature_2m"]

            # -------------------------
            #  API Wikimedia
            # -------------------------

            image_api_url = "https://commons.wikimedia.org/w/api.php"

            image_params = {
                "action": "query",
                "generator": "search",
                "gsrsearch": ville_nom,
                "gsrnamespace": 6,
                "gsrlimit": 1,
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json"
            }

            image_headers = {
                "User-Agent": "MonProjetPython/1.0 (projet personnel)"
            }

            image_response = requests.get(
                image_api_url,
                params=image_params,
                headers=image_headers
            )

            image_data = image_response.json()

            if "query" in image_data:

                pages = image_data["query"]["pages"]
                page = list(pages.values())[0]

                image_url = page["imageinfo"][0]["url"]

    return render_template(
        "index.html",
        ville=ville_nom,
        temperature=temperature,
        image_url=image_url,
        erreur=erreur
    )


if __name__ == "__main__":
    app.run()

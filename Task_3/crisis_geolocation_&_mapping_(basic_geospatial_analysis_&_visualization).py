
import pandas as pd
import spacy
from geopy.geocoders import Nominatim
import folium
from folium.plugins import HeatMap

path = "reddit_mentalhealth_data.csv"
df = pd.read_csv(path)
df.head()

sp = spacy.load("en_core_web_sm")
geolocator = Nominatim(user_agent="geo_crisis_mapping")

def get_location(text):
    doc = sp(text)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            return ent.text
    return None

df["location"] = df["content"].astype(str).apply(get_location)
df = df.dropna(subset=["location"])
df.head()

def location_geocode(location):
    try:
        geo = geolocator.geocode(location)
        if geo:
            return geo.latitude, geo.longitude
    except:
        return None
    return None

df["coordinates"] = df["location"].apply(location_geocode)
df = df.dropna(subset=["coordinates"])

df[["latitude", "longitude"]] = pd.DataFrame(df["coordinates"].tolist(), index=df.index)
df.head()

center = [df["latitude"].mean(), df["longitude"].mean()]
mp = folium.Map(location=center, zoom_start=5)

data = df[["latitude", "longitude"]].values.tolist()
HeatMap(data).add_to(mp)
heatmap_path = "crisisheatmap.html"
mp.save(heatmap_path)
display(mp)

top5locations = df["location"].value_counts().head(5)
print("Top 5 Crisis Locations:\n", top5locations)


from flask import Flask, render_template, request
from pyproj import Transformer

app = Flask(__name__)

# ==============================
# Coordinate Systems
# ==============================

WGS84 = "EPSG:4326"

GHANA_NATIONAL_GRID = (
    "+proj=tmerc +lat_0=4.66666666666667 "
    "+lon_0=-1 +k=0.99975 "
    "+x_0=274319.736 +y_0=0 "
    "+ellps=clrk80 "
    "+towgs84=-199,32,322,0,0,0,0 "
    "+units=m +no_defs"
)

GHANA_METRE_GRID = (
    "+proj=tmerc +lat_0=4.66666666666667 "
    "+lon_0=-1 +k=0.99975 "
    "+x_0=900000 +y_0=0 "
    "+ellps=WGS84 +units=m +no_defs"
)

# ==============================
# Transformers
# ==============================

wgs84_to_gng = Transformer.from_crs(WGS84, GHANA_NATIONAL_GRID, always_xy=True)

wgs84_to_gmg = Transformer.from_crs(WGS84, GHANA_METRE_GRID, always_xy=True)

gng_to_gmg = Transformer.from_crs(GHANA_NATIONAL_GRID, GHANA_METRE_GRID, always_xy=True)

gmg_to_gng = Transformer.from_crs(GHANA_METRE_GRID, GHANA_NATIONAL_GRID, always_xy=True)

# ==============================
# Main Route
# ==============================

@app.route("/", methods=["GET", "POST"])

def home():
    result = ""
    lat = None
    lon = None

    if request.method == "POST":

        try:

            conversion = request.form["conversion"]

            value1 = float(request.form["value1"])

            value2 = float(request.form["value2"])

            # WGS84 → Ghana National Grid
            if conversion == "WGS84 to Ghana National Grid":

                x, y = wgs84_to_gng.transform(value2, value1)

                result = f"Easting: {x:.3f} | Northing: {y:.3f}"

                lat = value1
                lon = value2

            # WGS84 → Ghana Metre Grid
            elif conversion == "WGS84 to Ghana Metre Grid":

                x, y = wgs84_to_gmg.transform(value2, value1)

                result = f"Easting: {x:.3f} | Northing: {y:.3f}"

                lat = value1
                lon = value2

            # Ghana National Grid → Ghana Metre Grid
            elif conversion == "Ghana National Grid to Ghana Metre Grid":

                x, y = gng_to_gmg.transform(value1, value2)

                result = f"Easting: {x:.3f} | Northing: {y:.3f}"

            # Ghana Metre Grid → Ghana National Grid
            elif conversion == "Ghana Metre Grid to Ghana National Grid":

                x, y = gmg_to_gng.transform(value1, value2)

                result = f"Easting: {x:.3f} | Northing: {y:.3f}"

        except:
            result = "Invalid input. Please enter numbers."

    return render_template(
        "index.html",
        result=result,
        lat=lat,
        lon=lon
    )

# ==============================
# Run App
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
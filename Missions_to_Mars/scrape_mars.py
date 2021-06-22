# import necessary libraries
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()

db.mars.insert_many(
[
{'title': 'Cerberus Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png'}, 
{'title': 'Schiaparelli Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/08eac6e22c07fb1fe72223a79252de20_schiaparelli_enhanced.tif_thumb.png'}, 
{'title': 'Syrtis Major Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/55a0a1e2796313fdeafb17c35925e8ac_syrtis_major_enhanced.tif_thumb.png'}, 
{'title': 'Valles Marineris Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/4e59980c1c57f89c680c0e1ccabbeff1_valles_marineris_enhanced.tif_thumb.png'}]
)

# create route that renders index.html template
@app.route("/")
def echo():
    mars_list = list(db.mars.find())

    return render_template("index.html", mars_list=mars_list )


if __name__ == "__main__":
    app.run(debug=True)
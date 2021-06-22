# import necessary libraries
from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

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

db.mars.insert_many([
{'title': 'Cerberus Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/39d3266553462198bd2fbc4d18fbed17_cerberus_enhanced.tif_thumb.png'}, 
{'title': 'Schiaparelli Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/08eac6e22c07fb1fe72223a79252de20_schiaparelli_enhanced.tif_thumb.png'}, 
{'title': 'Syrtis Major Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/55a0a1e2796313fdeafb17c35925e8ac_syrtis_major_enhanced.tif_thumb.png'}, 
{'title': 'Valles Marineris Hemisphere Enhanced', 'img_url': 'https://marshemispheres.com/images/4e59980c1c57f89c680c0e1ccabbeff1_valles_marineris_enhanced.tif_thumb.png'}]
)
# create route that renders index.html template
@app.route("/")
def echo():
   mars_list = list(db.mars.find())

   return render_template("index.html", mars_list=mars_list, Article_Title = Art_Title, Article_Para = Art_Para, Featured_image= featured_image_url)

@app.route("/scrape")
def scrape():
    #importing libraries
    from splinter import Browser
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import requests
    from webdriver_manager.chrome import ChromeDriverManager

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #url website to pull info from
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'

    html = browser.html
    soup = bs(html, 'html.parser')

    # results are returned and assigned to a variable
    Art_Title= soup.find("div", class_="content_title").string

    Art_Para = soup.find("div", class_="article_teaser_body").string

    #url website to pull info from
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    #grabbing url for image
    featured_image_url = browser.find_by_tag("img[class='headerimage fade-in']")['src']
    #print(featured_image_url) for error checking

    #getting url
    Mars_Facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(Mars_Facts_url)
    Mars_facts_df = tables[0]
    Mars_facts_df = Mars_facts_df.rename(columns= Mars_facts_df.iloc[0])
    Mars_facts_df = Mars_facts_df.drop(index= 0)

    html_table = Mars_facts_df.to_html()
    html_table.replace('\n', '')

    Mars_Hemi_Url = "https://marshemispheres.com/"
    browser.visit(Mars_Hemi_Url)

    html1 = browser.html
    soup1 = bs(html1, 'html.parser')

    Hemisphere_image_urls = []

    for info in soup1.find_all('div',class_="item"):
        Hemisphere_dict = {}
        #getting title of each hemisphere
        Hemisphere_dict["title"] = info.div.a.h3.text
        #getting image url of each hemisphere
        Hemisphere_dict["img_url"] = Mars_Hemi_Url+info.a.img["src"]
        
        Hemisphere_image_urls.append(Hemisphere_dict)

    #exit out of browser
    browser.quit()


if __name__ == "__main__":
    app.run(debug=True)
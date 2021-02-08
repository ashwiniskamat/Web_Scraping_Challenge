# Web_Scraping_Challenge

In this project, a web application was built that scrapes various websites for data related to the Mission to Mars and displays information in an HTML page. 

STEP 1: Scraping
- completed the initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Splinter

NASA Mars News
- scraped the NASA Mars News Site (https://mars.nasa.gov/news/) and collected the latest news title and paragraph text. 
- assigned the text to variables to reference later

Mars Facts
- visited the Mars Facts webpage (https://space-facts.com/mars/) and used Pandas to scrape the table containing facts about the planet (diameter, mass, etc.)
- used Pandas to convert the data to a HTML table string

Mars Hemispheres
- visited the USGS Astrogeology site (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mars' hemispheres
- saved both the image url string for the full resolution hemisphere image and the hemisphere title containing the hemisphere name
- used a Python dictionary to store the data using the keys img_url and title 
- appended the dictionary with the image url string and the hemisphere title to a list

STEP 2: MongoDB and Flask Application

Used MongoDB with Flask to create an HTML page that displays all the scraped information from the URLs above.
- converted the Jupyter notebook created in Step 1 into a Python script called "scape_mars.py"
- used a scrape function that executed the scraping code and formed a Python dictionary
- created a "/scrape" route which scraped the information from the URLs and inserted the Python dictionary into MongoDB and redirected to the "/" route
- the "/" route was created to read the MongoDB and render the template HTML file title "index.html" using Flask

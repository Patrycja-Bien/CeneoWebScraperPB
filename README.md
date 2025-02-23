# CeneoWebScraperPB
CeneoWebScraperPB is a Flask-based web application that scrapes product reviews from Ceneo.pl, a popular Polish e-commerce platform. The app allows users to extract and analyze customer reviews, ratings, and other relevant details in a structured format.

## Features
✅ Scrapes reviews from Ceneo.pl using a product URL
✅ Displays extracted data in a user-friendly web interface
✅ Saves data in JSON/CSV format for further analysis
✅ Handles pagination to fetch multiple reviews
✅ Filters verified purchases

## Technologies Used
Python & Flask (backend & web app)
BeautifulSoup (web scraping)
Requests (fetching webpage content)
Pandas (data processing & exporting)
HTML/CSS (frontend)

## Installation & Usage

Clone the repository:
git clone https://github.com/Patrycja-Bien/CeneoWebScraperPB.git
cd CeneoWebScraperPB

Install dependencies:
pip install -r requirements.txt

Run the Flask app:
flask run

Open the app in your browser:
http://127.0.0.1:5000/

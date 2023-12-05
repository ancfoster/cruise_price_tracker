import subprocess
import requests
from datetime import datetime
from bs4 import BeautifulSoup

urls = ['https://www.windstarcruises.com/cruise/accommodations-pricing/caribbean/bridgetown-to-bridgetown/hidden-treasures-lesser-antilles/?pkgid=342709', ]

def check_prices():
    """
    Primary script function
    """
    #Loop through the url for each cruise
    for url in urls:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            cruise_title = get_title(soup)
            cruise_price = get_price(soup)
            notifcation(cruise_title, cruise_price)
        else:
            print("Failed to retrieve the webpage. Status Code:", response.status_code)

def get_cruise_start(date_string):
    """
    This function takes a string of text from web page, converts it to a Python date.
    This is used to check if a cruise is still in the future.
    Will return false if cruise is not in future.
    """
    # Split the date string into start and end date parts
    start_date_str, end_date_str = date_string.split(" - ")

    # Define the date format for parsing
    date_format = "%a %b %d, %Y"

    # Parse start and end dates
    start_date = datetime.strptime(start_date_str, date_format)

    #Check if cruise start date is still in future
    current = datetime.now()
    if start_date > current:
        return(True)
    else:
        return(False)


def notifcation(title, price):
    """
    This function will send a macOS notifciation, takes a title and message as paramters
    """
    # Execute AppleScript command to display a notification
    script = f'display notification "Price for {title}, is now ${price}" with title "Cruise Price Alert"'
    subprocess.run(['osascript', '-e', script])


def get_title(html):
    """
    Scrapes the cruise title
    """
    # Find the HTML element using the CSS selector
    element = html.find('span', class_='title1')

    # Check if the element is found
    if element:
        # Get the text content of the element
        element_text = element.get_text(strip=True)
        return element_text
    else:
        return "Cruise Title Not Found"


def get_price(html):
    """
    Scrapes the cruise price
    """
    # Find the HTML element using the CSS selector
    element = html.find('span', class_='amount')

    # Check if the element is found
    if element:
        # Get the text content of the element
        element_text = element.get_text(strip=True)
        element_text = element_text[1:]
        price = element_text.replace(',', '.')
        price = float(price)
        return price
    else:
        return "Call For Availability"


#Run
check_prices()
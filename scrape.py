import requests
import textwrap
import os
from bs4 import BeautifulSoup

# =========================================================
# This terminal application scrapes the daily news from the
# Daily Wire. We can see top articles, most recent articles
# and hopefully top trends in the future
# =========================================================

class DailyWire:
    """ This class is responsible for scraping the Daily Wire website
    """

    def __init__( self ):
        """ Start with automatically getting the content of the main page
        """
        self.result = requests.get( "https://www.dailywire.com" )
        self.content = self.result.content
        self.soup = BeautifulSoup( self.content, "html.parser" )


    def scrape_top_headlines( self ):
        """ A method that grabs the current top headlines. Should be 5-6 headlines
        """
        top_headlines = self.soup.find_all( "h2" )
        top_headlines_list = []
        counter = 1

        print( "\n\nTOP HEADLINES:\n\n" )

        for title in top_headlines:
            # Need to avoid getting ads with this method
            if title.text != "Get This eBookFREE!" and title.text != "We're taking a whole new approach.":
                # Getting the extended url link for the article
                headline_extended_link = title.a.get( 'href' )
                stripped_text = title.text.strip( '\n' )
                top_headlines_list.append( stripped_text )
                print( "{}. {}\n( {} )\n".format( counter, stripped_text, "https://www.dailywire.com" + headline_extended_link ) )
                counter += 1


    def scrape_front_page_headlines( self ):
        """ A method that grabs rest of the headlines prior to clicking the 'load more' button
        """
        headlines = self.soup.find_all( "h3" )
        headlines_list = []
        counter = 1

        print( "\n\nOTHER HEADLINES:\n\n" )

        for title in headlines:
            # Need to avoid getting ads with this method
            if title.text != "Make the web’s best conservative commentary even better":
                # Getting the extended url link for the article
                headline_extended_link = title.a.get( 'href' )
                stripped_text = title.text.strip( '\n' )
                headlines_list.append( stripped_text )
                print( "{}. {}\n( {} )\n".format( counter, stripped_text, "https://www.dailywire.com" + headline_extended_link ) )
                counter += 1
        

    def scrape_article_title_and_content( self ):
        """ A method that gets a specific article's content and stores the content into a single string variable
        """

        # Let the user enter a URL of a Daily Wire article to scrape
        print( "\nPlease enter the URL of an article you wish to scrape\n" )
        article_to_scrape = input( "> " )

        # Try to get a result from the url, otherwise print that an error occurred
        try:
            result = requests.get( article_to_scrape )
            content = result.content
            soup = BeautifulSoup( content, "html.parser" )

            # Get the article's title
            article_title_string = ""
            # article_title = soup.select( ".page-title" )
            article_title = soup.h1.getText().upper()
            article_title_string = article_title
            # print( "\n\n\n{}\n\n\n".format( article_title ) )

            # Grabbing the article by a div class and then traversing down to the p tag children to grab the content
            article_content_string = ""
            article_content = soup.select( ".field-body > p" )
            index = 0
            for row in article_content:
                article_content_string += article_content[index].text + " "
                index += 1

            # Using the module textwrap in order to limit character column width to make the content more legible
            print( "\n\n--------------------------------------------------------------------------------\nTITLE:\n\n{}\n\n\nCONTENT:\n\n{}\n--------------------------------------------------------------------------------".format( textwrap.fill( article_title_string, width=80 ), textwrap.fill( article_content_string, width=80 ) ) )
        except:
            print( "\n\nAn error has occurred. Please try again.")


def daily_wire_menu():
    """ The main menu for the terminal application
    """
    
    # Instantiate the Daily Wire class
    dailywire = DailyWire()
    while True:
        
        print( "\n\n\n-------------------\n| DAILY WIRE MENU |\n-------------------\n\n1) View the top headlines\n2) View the other front page headlines\n3) View a specific article\n4) Clear the terminal screen\n5) Exit the program\n\n" )
        user_option_choice = input( "> " )

        # Menu options
        if int( user_option_choice ) == 1:
            dailywire.scrape_top_headlines()
        elif int( user_option_choice ) == 2:
            dailywire.scrape_front_page_headlines()
        elif int( user_option_choice ) == 3:
            dailywire.scrape_article_title_and_content()
        elif int( user_option_choice ) == 4:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif int( user_option_choice ) == 5:
            break
        else:
            print( "\nPLEASE ENTER A VALID VALUE\n" )


if __name__ == "__main__":
    daily_wire_menu()

import os

import pandas as pd
from bs4 import BeautifulSoup
from RPA.Browser.Selenium import Selenium

browser = Selenium()


class Imdb_Automation:
    """
    The Class is defined to do a Automation Pocess on IMDB.com

    Returns : A CSV of Top 250 TV shows list according to their Release Date
    """

    curr = os.getcwd()

    def open_browser(self):
        browser.open_available_browser("https://www.imdb.com")

    def go_to_table_of_top_20_tv_shows(self):
        """
        This method is defined to go Top 20 TV shows list page
        WorkFlow:
        1) Home Page
        2) Drop Down Menu (On left corner)
        3) Top 20 Tv Shows List according to their Tv shows List

        """

        # Go to Menu bar
        browser.click_element_when_visible(
            'xpath://*[@id="imdbHeader-navDrawerOpen--desktop"]/div'
            )

        # Clicking the element- Top 250 Tv Shows
        browser.click_element_when_visible(
            'xpath://*[@id="imdbHeader"]/div[2]/aside/div/div[2]/div/div[2]/div[1]/span/div/div/ul/a[2]'
            )

        # Wait until the sort options will come
        browser.wait_until_element_is_visible(
            'xpath://*[@id="lister-sort-by-options"]'
            )

        # Selecting the release data option from sort menu
        browser.select_from_list_by_value(
            'xpath://*[@id="lister-sort-by-options"]',
            "us:descending"
            )

    def correcting_the_format_of_csv(self):

        csv_path = os.path.join(
            os.getcwd(), "output/IMDB_TOP_250_TV_SHOWS_LIST.csv"
            )

        # reading the csv
        df = pd.read_csv(csv_path)
        # deleting the "Your rating" column
        df.drop("Your Rating", axis=1, inplace=True)

        # deleting all the unnamed column
        df.drop(
            df.columns[
                df.columns.str.contains('unnamed', case=False)
                ], axis=1, inplace=True
            )

        print(df)

        # Saving the dataframe to CSV
        df.to_csv(csv_path, index=False)

        os.remove("innerhtml.html")

    def html_table_to_csv(self, html_file):  # making csv
        """
        This method is defined to make a csv file from a html table
        Using BeautifulSoup method

        Args:
            html_file (HTML): contains table of 250 Tv shows list

        """

        soup = BeautifulSoup(open(html_file), 'html.parser')

        table = soup.find_all("table")[0]

        headers = []
        # taking the heading row
        for th in table.find("tr").find_all("th"):
            headers.append(th.text.strip())

        rows = []
        # taking all the table data
        for tr in table.find_all("tr")[1:]:
            cells = []
            # grab all td tags in this table row
            tds = tr.find_all("td")

            for td in tds:
                # appending the table data for each row to a list named cells
                cells.append(td.text.strip())

                if len(cells) != 1:
                    oneliner = cells[1].replace("\n", " ")
                    print(oneliner)
                    cells[1] = oneliner

            # each cells list append to another list named rows
            rows.append(cells)

        df = pd.DataFrame(rows, columns=headers)

        csv_path = os.path.join(
            os.getcwd(), "output/IMDB_TOP_250_TV_SHOWS_LIST.csv"
            )

        df.to_csv(csv_path, index=False)

    def savefile(self):
        # taking innerhtml data of the table
        html_data = browser.get_element_attribute(
            'xpath://*[@id="main"]/div/span/div/div/div[3]', 'innerHTML'
            )

        #  making a html file where innerHTMl data is saving
        new = os.path.join(os.getcwd(), "innerhtml.html")
        f = open(new, "w")
        f.write(html_data)
        f.close()


obj = Imdb_Automation()


def minimal_task():

    obj.open_browser()
    obj.go_to_table_of_top_20_tv_shows()
    obj.savefile()
    obj.html_table_to_csv("innerhtml.html")
    obj.correcting_the_format_of_csv()

    print("Done.")


minimal_task()

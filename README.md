# Hockey Team Scraper

This project scrapes hockey team data from a website and processes it into an Excel file. It also saves the raw HTML pages in a ZIP file.

## Features

- Scrapes hockey team data from multiple pages.
- Saves HTML pages for each scraped page into a ZIP file.
- Creates an Excel file with two sheets:
  1. **Hockey Data**: Contains team statistics.
  2. **Winners and Losers**: Contains the winner and loser teams for each year.

## Requirements

- Python 3.8 or higher

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sushantch12/Scrap-all-hockey-team.git 
  
   
2. **Create a virtual environment **:

    ```bash
    Copy code- python -m venv venv
                ## Activate the virtual environment:

                      On Windows:
                        bash
                        Copy code
                        venv\Scripts\activate
                        
                      On macOS/Linux:
                        bash
                        Copy code
                        source venv/bin/activate
   
3. ** Install dependencies **:

       bash
       Copy code
       pip install -r requirements.txt


##  _**Running the Program**_ 

    To run the scraper and generate the ZIP and Excel files, use the following command:

            bash
            Copy code
            python main.py
            This will:

                    Scrape data from the website.
                    Save HTML files into html_files directory.
                    Create a ZIP file named html_files.zip containing the HTML files.
                    Remove the html_files directory after zipping.
                    Generate an Excel file named hockey.xlsx with the scraped data.
                    Files
                    hockey_scrape.py : The main script that performs the scraping and file generation.
                    html_files.zip: The ZIP file containing the raw HTML pages.
                    hockey.xlsx: The Excel file containing the scraped data.
                    Logging
                    Logs are saved in scrape_log.txt. This file contains information on the scraping process and any errors encountered.


### Running Unit Tests

        To run the unit tests, navigate to the directory containing `test_hockey_scrape.py` and execute:

            ```bash
            pytest test_hockey_scrape.py

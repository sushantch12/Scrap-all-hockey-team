import aiohttp
import asyncio
import os
import zipfile
import openpyxl
from bs4 import BeautifulSoup as bs
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side
import logging
import time

# Logging setup
logging.basicConfig(filename='scrape_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directory for saving HTML files
HTML_DIR = 'html_files'
EXCEL_FILE_PATH = 'hockey.xlsx'

# Create the directory for HTML files if it doesn't exist
if not os.path.exists(HTML_DIR):
    os.makedirs(HTML_DIR)

async def fetch(session, page_num):
    """Fetches the HTML content of a page."""
    url = f'https://www.scrapethissite.com/pages/forms/?page_num={page_num}&per_page=100'
    async with session.get(url) as response:
        return await response.text()

def parse_html(html_content):
    """Parses HTML content and returns BeautifulSoup object."""
    soup = bs(html_content, 'html.parser')
    return soup

def process_team_data(data):
    """Processes raw team data for Excel file generation."""
    processed_data = {
        'TeamName': [team['TeamName'] for team in data],
        'Year': [team['Year'] for team in data],
        'Win': [team['Win'] for team in data],
        'Losses': [team['Losses'] for team in data],
        'OTLosses': [team['OTLosses'] for team in data],
        'WinPercentage': [team['WinPercentage'] for team in data],
        'GoalsFor(GF)': [team['GoalsFor(GF)'] for team in data],
        'GoalsAgainst(GA)': [team['GoalsAgainst(GA)'] for team in data],
        '+/-': [team['+/-'] for team in data]
    }
    return processed_data

def calculate_winner_loser(data):
    """Calculates the winner and loser teams based on the provided data."""
    winners_losers = {}
    for team in data:
        year = team['Year']
        if year not in winners_losers:
            winners_losers[year] = {'winner': {'team': team['TeamName'], 'wins': team['Win']}, 'loser': {'team': team['TeamName'], 'wins': team['Losses']}}
        else:
            if team['Win'] > winners_losers[year]['winner']['wins']:
                winners_losers[year]['winner'] = {'team': team['TeamName'], 'wins': team['Win']}
            if team['Losses'] > winners_losers[year]['loser']['wins']:
                winners_losers[year]['loser'] = {'team': team['TeamName'], 'wins': team['Losses']}
    return winners_losers

def create_zip_file():
    """Creates a ZIP file containing all HTML files."""
    with zipfile.ZipFile('html_files.zip', 'w') as zipf:
        for page_num in range(1, 25):
            file_name = f'{page_num}.html'
            file_path = os.path.join(HTML_DIR, file_name)
            zipf.write(file_path, arcname=file_name)

def create_excel_file(team_data, winners_losers):
    """Creates an Excel file with the hockey data and winners/losers sheets."""
    # Define styles
    border = Border(left=Side(border_style="thin"), right=Side(border_style="thin"), top=Side(border_style="thin"), bottom=Side(border_style="thin"))

    # Create a new workbook and set the active sheet
    wb = Workbook()
    ws1 = wb.active
    ws1.title = 'Hockey Data'

    # Write the header
    headers = ['TeamName', 'Year', 'Win', 'Losses', 'OTLosses', 'WinPercentage', 'GoalsFor(GF)', 'GoalsAgainst(GA)', '+/-']
    ws1.append(headers)

    # Apply bold font to the header and center align
    for cell in ws1[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')  # Center align the header
        cell.border = border  # Add border to header cells

    # Write the data to the sheet
    for i in range(len(team_data['TeamName'])):
        ws1.append([
            team_data['TeamName'][i],
            team_data['Year'][i],
            team_data['Win'][i],
            team_data['Losses'][i],
            team_data['OTLosses'][i],
            team_data['WinPercentage'][i],
            team_data['GoalsFor(GF)'][i],
            team_data['GoalsAgainst(GA)'][i],
            team_data['+/-'][i]
        ])

    # Center align the data and add borders in the columns
    for col in ws1.columns:
        max_length = 0
        for cell in col:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border  # Add border to all cells
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))  # Get max length of cell contents
        col_letter = col[0].column_letter  # Get column letter
        ws1.column_dimensions[col_letter].width = max_length + 2  # Adjust column width

    # Create the second sheet with the winners and losers data
    ws2 = wb.create_sheet(title="Winners and Losers")

    # Write the header for the second sheet
    ws2.append(['Year', 'Winner', 'Winner Num. of Wins', 'Loser', 'Loser Num. of Wins'])

    # Apply bold font to the header and center align
    for cell in ws2[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center', vertical='center')  # Center align the header
        cell.border = border  # Add border to header cells

    # Write the winners and losers data to the second sheet
    for year, teams in winners_losers.items():
        ws2.append([
            year,
            teams['winner']['team'],
            teams['winner']['wins'],
            teams['loser']['team'],
            teams['loser']['wins']
        ])

    # Center align the data and add borders in the columns
    for col in ws2.columns:
        max_length = 0
        for cell in col:
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = border  # Add border to all cells
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))  # Get max length of cell contents
        col_letter = col[0].column_letter  # Get column letter
        ws2.column_dimensions[col_letter].width = max_length + 2  # Adjust column width

    # Save the workbook to a file
    try:
        wb.save(EXCEL_FILE_PATH)
        logging.info(f"Data successfully saved to {EXCEL_FILE_PATH}")
    except Exception as e:
        logging.error(f"Error saving the Excel file: {e}")

async def main():
    """Main function to perform the scraping and data processing."""
    start_time = time.time()  # Start time for performance measurement

    # Clear old logs
    with open('scrape_log.txt', 'w') as log_file:
        log_file.write('')

    # Log the start of the process
    logging.info('Starting web scraping process.')

    # Scrape data
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, page_num) for page_num in range(1, 25)]
        html_pages = await asyncio.gather(*tasks)

    # Save HTML files
    for i, html in enumerate(html_pages, start=1):
        file_path = os.path.join(HTML_DIR, f'{i}.html')
        with open(file_path, 'w') as file:
            file.write(html)

    # Parse HTML and extract data
    team_data = []
    for page_num, html in enumerate(html_pages, start=1):
        soup = parse_html(html)
        for team in soup.find_all('tr', class_='team'):
            try:
                team_data.append({
                    'TeamName': team.find('td', class_='name').text.strip(),
                    'Year': team.find('td', class_='year').text.strip(),
                    'Win': int(team.find('td', class_='wins').text.strip() or 0),
                    'Losses': int(team.find('td', class_='losses').text.strip() or 0),
                    'OTLosses': int(team.find('td', class_='ot-losses').text.strip() or 0),
                    'WinPercentage': team.find('td', class_='pct').text.strip(),
                    'GoalsFor(GF)': int(team.find('td', class_='gf').text.strip() or 0),
                    'GoalsAgainst(GA)': int(team.find('td', class_='ga').text.strip() or 0),
                    '+/-': team.find('td', class_='diff').text.strip() or '0'
                })
            except Exception as e:
                logging.error(f"Error processing team data: {e}")

    # Process team data
    processed_data = process_team_data(team_data)

    # Calculate winners and losers
    winners_losers = calculate_winner_loser(team_data)

    # Create the ZIP file with HTML pages
    create_zip_file()

    # Create the Excel file with data and calculations
    create_excel_file(processed_data, winners_losers)

    # Log the end of the process and time taken
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Web scraping process completed in {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    asyncio.run(main())

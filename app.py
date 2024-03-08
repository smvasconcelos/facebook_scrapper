import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from openpyxl.styles import Border, Side


def create_excel_with_thumbnails(data_array, filename):
  """
  Creates an Excel file with data and hyperlinks to thumbnails in the 'thumbnail' key.

  Args:
      data_array (list): List of dictionaries containing data.
      filename (str): Name of the Excel file to create.
  """

  # Create a pandas DataFrame from the data array
  df = pd.DataFrame(data_array)

  # create a pandas.ExcelWriter object
  writer = pd.ExcelWriter(filename, engine='xlsxwriter')

  # write the data frame to Excel
  df.to_excel(writer, index=False, sheet_name='Sheet1')

  # get the XlsxWriter workbook and worksheet objects
  workbook = writer.book
  worksheet = writer.sheets['Sheet1']

  # adjust the column widths based on the content
  for i, col in enumerate(df.columns):
      width = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
      worksheet.set_column(i, i, width if width < 100 else 100)

  # save the Excel file
  writer._save()

if __name__ == '__main__':
  # Instancia dos argumentos possíveis do webdriver
  chrome_options = Options()
  # Inicia uma instancia oculta ( não mostra o navegador )
  # chrome_options.add_argument("--headless")
  # Ajustes de performance e agent do navegador
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--disable-features=NetworkService")
  chrome_options.add_argument("--window-size=1920x1080")
  chrome_options.add_argument("--disable-features=VizDisplayCompositor")

  driver = webdriver.Chrome(options=chrome_options)

  driver.get('https://www.facebook.com/marketplace/107665125929392/search?minPrice=700&maxPrice=1500&query=apartamentos%20em%20itabuna&exact=false')

  closeButton = WebDriverWait(driver, 5).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Fechar']"))
  )

  driver.find_element(By.CSS_SELECTOR,"[aria-label='Fechar']").click()

  oldPageSource = driver.page_source

  while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    currentPageSource = driver.page_source

    if (oldPageSource == currentPageSource):
      break;

    else:
      oldPageSource = currentPageSource
      time.sleep(2)

  soup = BeautifulSoup(driver.page_source, "html.parser")

  itemCollection = soup.find("div", attrs={"aria-label": "Coleção de itens do Marketplace"})

  aptos = []

  for anchor in itemCollection.findAll("a"):

    image = anchor.find('img')['src']
    spans = anchor.find_all('span')
    value = spans[0].text
    description = spans[1].text

    aptos.append({
      "thumbnail": image,
      "link": f'www.facebook.com/{anchor['href']}',
      "price": value,
      "description": description
    })

  create_excel_with_thumbnails(aptos, 'aptos.xlsx')

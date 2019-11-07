from selenium import webdriver
import sys
import pycountry
import time
import traceback
import random
import csv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Convert the @input_countries_alpha into their correct name and append it to @countries_name
def convert_country_alpha3_to_country_name(input_countries_alpha, countries_name):
    
    alphas = {}

    for alpha in pycountry.countries:
        alphas[alpha.alpha_3] = alpha.name

    countries_name.append(alphas.get(input_countries_alpha[0]))

# Get five random country (alpha3) from pycountry and append it to @input_countries_alpha
def random_grab_five_countries(input_countries_alpha):
    index = 0
    while (index <= 4):
        country = random.choice(list(pycountry.countries))
        input_countries_alpha.append(country.alpha_3)
        index += 1

def get_four_countries(driver, results):
    position = 0

    while (position < 4):
        try:
            country_name = pycountry.countries.get(name=driver.find_element_by_xpath('//*[@id="row' + str(position) + 'jqx-ProductGrid"]/div[1]/a').text).alpha_3
            export = driver.find_element_by_xpath('//*[@id="row' + str(position) + 'jqx-ProductGrid"]/div[2]/div').text
            country = country_name + ' ' + export.partition(",")[0] + 'B'
            results.append(country)

        except Exception:
            results.append("Country not found in pycountry or no more data to scrape")

        finally:
            position += 1

# Print the result of the scrapper
def print_results(results):
    for result in results:
        print(result)
    return

# Open the chrome client
def open_webdriver(input_countries_alpha, results):
    try:
        driver = webdriver.Chrome(executable_path=".//chromedriver")
        driver.maximize_window()
    except:
        print("chromedriver not found, please place it on the root of the project's folder")
        return 1
    
    try:
        driver.get('https://wits.worldbank.org/CountryProfile/en/Country/'+ input_countries_alpha[0] +'/Year/2017/TradeFlow/Export/Partner/by-country/Product/Total')
        get_four_countries(driver, results)

    except Exception:
        traceback.print_exc()
        driver.quit()

    finally:
        driver.quit()

# Check the @arguments and append the detected country alpha to @input_countries_alpha
def check_arguments(arguments, input_countries_alpha):
    save = 0
    position = 1

    while (arguments >= position):
        if (sys.argv[position] != 'save' and sys.argv[position] != 'all'):
            input_countries_alpha.append(sys.argv[position])
        elif (sys.argv[position] == 'all'):
            random_grab_five_countries(input_countries_alpha)
        elif (sys.argv[position] == 'save'):
            save = 1
        position = position + 1
    return save

# Save the results in a csv file
def save_results_in_csv(results):
    print("saving results to results.csv")
    with open('results.csv', 'w') as result_file:
        w = csv.writer(result_file, delimiter='\n')
        w.writerow(results)
    return

def main():
    input_countries_alpha = []
    countries_name = []
    results = []
    arguments = len(sys.argv) - 1
    
    if (arguments < 1):
        print("You need at least one argument")
        return 1

    save = check_arguments(arguments, input_countries_alpha)
    convert_country_alpha3_to_country_name(input_countries_alpha, countries_name)
    if (open_webdriver(input_countries_alpha, results) == 1):
        exit
    elif (save == 1):
        save_results_in_csv(results)
    else:
        print_results(results)
        print(input_countries_alpha)



main()
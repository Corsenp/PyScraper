from selenium import webdriver
import sys
import pycountry
import time
import traceback
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# convert the @input_countries_alpha into their correct name and append it to @countries_name
def convert_country_alpha3_to_country_name(input_countries_alpha, countries_name):
    
    alphas = {}

    for alpha in pycountry.countries:
        alphas[alpha.alpha_3] = alpha.name

    countries_name.append(alphas.get(input_countries_alpha[0]))

def get_four_countries(driver, results):
    position = 0

    while (position < 4):
        try:
            country = pycountry.countries.get(name=driver.find_element_by_xpath('//*[@id="row' + str(position) + 'jqx-ProductGrid"]/div[1]/a').text).alpha_3
            export = driver.find_element_by_xpath('//*[@id="row' + str(position) + 'jqx-ProductGrid"]/div[2]/div').text
            country += ' ' + export.partition(",")[0] + 'B'

            print('country = %s' % country)
            results.append(country)

        except:
            print("country not found in pycountry")
            return 
        finally:
            position += 1

# open the chrome client
def open_webdriver(input_countries_alpha, results):
    driver = webdriver.Chrome(executable_path=".//chromedriver")
    driver.maximize_window()
    
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
    position = 1

    while (arguments >= position):
        if (sys.argv[position] != 'save' and sys.argv[position] != 'all'):
            input_countries_alpha.append(sys.argv[position])
        position = position + 1

def main():
    input_countries_alpha = []
    countries_name = []
    results = []
    arguments = len(sys.argv) - 1
    
    if (arguments < 1):
        print("You need at least one argument")
        return 1

    check_arguments(arguments, input_countries_alpha)
    convert_country_alpha3_to_country_name(input_countries_alpha, countries_name)
    open_webdriver(input_countries_alpha, results)

    print(results)



main()
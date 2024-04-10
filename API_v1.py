from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route("/Cotizacion", methods=['POST'])
def get_Cotizacion():
    data = request.json
    zip_origen = data.get('zip_origen')
    zip_destino = data.get('zip_destino') 
    peso_kg = data.get('peso_kg')
    Largo = data.get('Largo')
    Ancho = data.get('Ancho')
    Alto = data.get('Alto')

    # FEDEX
    url = "https://www.fedex.com/es-mx/home.html#"

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)

    driver.minimize_window() # Minimizar la ventana del navegador

    driver.get(url)

    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fxg-cube__content")))
    button.click()


    input_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "fromGoogleAddress")))
    input_field.send_keys(zip_origen)
    time.sleep(2)
    input_field.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

    time.sleep(2)

    input_field2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "toGoogleAddress")))
    input_field2.send_keys(zip_destino)
    time.sleep(2)
    input_field2.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    time.sleep(2)

    weight_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "package-details__weight-0")))
    weight_field.send_keys(peso_kg)

    length_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="length"]')))
    length_field.send_keys(Largo)

    width_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="width"]')))
    width_field.send_keys(Ancho)

    height_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="height"]')))
    height_field.send_keys(Alto)

    submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "e2ePackageDetailsSubmitButtonRates")))
    submit_button.submit()

    price_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".magr-c-rates__button")))
    
    # Extraer Precio
    price_FEDEX = price_button.text
    driver.quit()

    # ESTAFETA
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # Correr en segundo plano
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    driver.get("https://enviaya.com.mx/es/paqueterias/estafeta/cotizador/?utm_campaign=686904761&utm_source=bing&utm_medium=cpc&utm_content=&utm_term=estafeta%20cotizador&adgroupid=1276534639665967&network=o&device=c&adposition=?matchtype=e&placement=&msclkid=a03a2bc381271bfa19d44dd3c843596b")

    time.sleep(5)

    input_field_from = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "quote_from")))
    input_field_from.send_keys(zip_origen)
    time.sleep(2)
    input_field_from.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    time.sleep(2)

    input_field_to = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "quote_to")))
    input_field_to.send_keys(zip_destino)
    time.sleep(2)
    input_field_to.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    time.sleep(2)

    # Selecciona la opción "Paquete"
    package_option = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[@for='shipping-2']")))
    package_option.click()

    time.sleep(2)

    length_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][length]")))
    length_field.send_keys(Largo)

    width_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][width]")))
    width_field.send_keys(Ancho)

    height_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][height]")))
    height_field.send_keys(Alto)

    weight_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][weight]")))
    weight_field.send_keys(peso_kg)
    time.sleep(2)

    submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()
    time.sleep(5)

    quote_price = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.rate-board-item__price")))
    price_text = quote_price.text

    # Extraer el precio de ESTAFETA
    price_ESTAFETA = price_text.split(" ")[-1]
    driver.quit()


    # DHL
    url = "https://www.dhl.com/mx-es/home/obtener-una-cotizacion.html"

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(2)

    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    button.click()

    input_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "originZip")))
    input_field.send_keys(zip_origen)
    time.sleep(5)
    input_field.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    time.sleep(5)

    input_field2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "destinationZip")))
    input_field2.send_keys(zip_destino)
    time.sleep(5)
    input_field2.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    time.sleep(5)

    input_field2.send_keys(Keys.ENTER)
    time.sleep(2)

    weight_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "weight-0")))
    weight_field.send_keys(peso_kg)

    length_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "length-0")))
    length_field.send_keys(Largo)

    width_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "width-0")))
    width_field.send_keys(Ancho)

    height_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "height-0")))
    height_field.send_keys(Alto)
    time.sleep(2)

    quote_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="get-a-quote-button"]')))
    quote_button.submit()
    time.sleep(15)

    price_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//p[@data-testid="offer-price"]')))

    # Extraer el precio de DHL
    price_DHL = price_element.text.split(" ")[1]
    driver.quit()

    # Imprimir los precios
    return jsonify({'price_FEDEX': price_FEDEX, 'price_ESTAFETA': price_ESTAFETA, 'price_DHL': price_DHL})

if __name__ == "__main__":
    app.run(debug=True)

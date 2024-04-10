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

    # Definir la URL de la página web
    url = "https://www.fedex.com/es-mx/home.html#"

    # Opciones para el navegador
    options = Options()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")  # Desactivar barra de progreso
    options.add_argument("--disable-notifications")  # Desactivar notificaciones

    # Inicializar el driver del navegador (Asegúrate de tener el driver del navegador en tu PATH)
    driver = webdriver.Chrome(options=options)

    # Minimizar la ventana del navegador
    driver.minimize_window()

    # Navegar a la URL
    driver.get(url)

    # Esperar a que el botón esté presente y hacer clic en él
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fxg-cube__content")))
    button.click()

    # Esperar a que el campo de entrada de texto esté presente e ingresar el valor "45187"
    input_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "fromGoogleAddress")))
    input_field.send_keys(zip_origen)
    time.sleep(2)
    # Simular la presión de las teclas de flecha hacia abajo y Enter
    input_field.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

    time.sleep(2)

    # Esperar a que el segundo campo de entrada de texto esté presente e ingresar el valor "45190"
    input_field2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "toGoogleAddress")))
    input_field2.send_keys(zip_destino)
    time.sleep(2)
    # Simular la presión de las teclas de flecha hacia abajo y Enter
    input_field2.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

    time.sleep(2)

    # Esperar a que el campo de peso esté presente e ingresar el valor "1"
    weight_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "package-details__weight-0")))
    weight_field.send_keys(peso_kg)

    length_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="length"]')))
    length_field.send_keys(Largo)

    width_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="width"]')))
    width_field.send_keys(Ancho)

    height_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="height"]')))
    height_field.send_keys(Alto)

    # Esperar a que el botón "Mostrar tarifas" esté presente y hacer clic en él
    submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "e2ePackageDetailsSubmitButtonRates")))
    submit_button.submit()

    # Esperar a que el botón con el precio esté presente
    price_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".magr-c-rates__button")))
    # Extraer el texto del botón
    price_FEDEX = price_button.text

    # Cerrar el navegador
    driver.quit()

    # Opciones para el navegador
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Crear una instancia del webdriver con las opciones modificadas
    driver = webdriver.Chrome(options=options)

    # Navegar a la página web de Estafeta
    driver.get("https://enviaya.com.mx/es/paqueterias/estafeta/cotizador/?utm_campaign=686904761&utm_source=bing&utm_medium=cpc&utm_content=&utm_term=estafeta%20cotizador&adgroupid=1276534639665967&network=o&device=c&adposition=?matchtype=e&placement=&msclkid=a03a2bc381271bfa19d44dd3c843596b")

    # Esperar a que la página se cargue completamente
    time.sleep(5)

    # Esperar a que el campo de entrada de texto esté presente e ingresar el valor "45187"
    input_field_from = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "quote_from")))
    input_field_from.send_keys(zip_origen)

    # Esperar a que se procese la entrada
    time.sleep(2)

    # Simular la presión de las teclas de flecha hacia abajo y Enter
    input_field_from.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

    # Esperar a que se procese la entrada
    time.sleep(2)

    # Repetir el proceso para el segundo campo de entrada de texto
    input_field_to = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "quote_to")))
    input_field_to.send_keys(zip_destino)

    # Esperar a que se procese la entrada
    time.sleep(2)

    # Simular la presión de las teclas de flecha hacia abajo y Enter
    input_field_to.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

    # Esperar a que se procese la entrada
    time.sleep(2)

    # Seleccionar la opción "Paquete"
    package_option = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[@for='shipping-2']")))
    package_option.click()

    # Esperar a que se procese la selección
    time.sleep(2)

    # Ingresar los valores de Largo, Ancho, Alto y peso_kg
    length_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][length]")))
    length_field.send_keys(Largo)

    width_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][width]")))
    width_field.send_keys(Ancho)

    height_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][height]")))
    height_field.send_keys(Alto)

    weight_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "shipment[parcels][0][weight]")))
    weight_field.send_keys(peso_kg)

    # Esperar a que se procesen las entradas
    time.sleep(2)

    # Hacer clic en el botón "Cotizar envío"
    submit_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    submit_button.click()

    # Esperar a que se cargue la nueva página
    time.sleep(5)

    # Esperar a que el precio de la cotización esté presente
    quote_price = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.rate-board-item__price")))
    price_text = quote_price.text

    # Extraer solo el precio del texto
    price_ESTAFETA = price_text.split(" ")[-1]

    # Cerrar el navegador
    driver.quit()

    # Definir la URL de la página web
    url = "https://www.dhl.com/mx-es/home/obtener-una-cotizacion.html"

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Inicializar el driver del navegador Chrome con las opciones modificadas
    driver = webdriver.Chrome(options=options)

    # Navegar a la URL
    driver.get(url)

    # Esperar explícitamente
    time.sleep(2)

    # Dar click al boton Aceptar todas las cookies
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    button.click()

    # Esperar a que el campo de entrada de texto esté presente e ingresar el valor "45187"
    input_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "originZip")))
    input_field.send_keys(zip_origen)

    # Esperar explícitamente
    time.sleep(5)

    # Simular la presión de las teclas de flecha hacia abajo y Enter
    input_field.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

    # Esperar explícitamente
    time.sleep(5)

    # Esperar a que el segundo campo de entrada de texto esté presente e ingresar el valor "45190"
    input_field2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "destinationZip")))
    input_field2.send_keys(zip_destino)

    # Esperar explícitamente
    time.sleep(5)

    # Simular la presión de las teclas de flecha hacia abajo y Enter
    input_field2.send_keys(Keys.ARROW_DOWN, Keys.RETURN)

    # Esperar explícitamente
    time.sleep(5)

    # Simular la presión de la tecla Enter
    input_field2.send_keys(Keys.ENTER)

    # Esperar explícitamente
    time.sleep(2)

    # Esperar a que el campo de peso esté presente e ingresar el valor "1"
    weight_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "weight-0")))
    weight_field.send_keys(peso_kg)

    length_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "length-0")))
    length_field.send_keys(Largo)

    width_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "width-0")))
    width_field.send_keys(Ancho)

    height_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "height-0")))
    height_field.send_keys(Alto)

    # Esperar explícitamente
    time.sleep(2)

    # Esperar a que el botón "Obtenga una cotización" esté presente y hacer clic en él
    quote_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="get-a-quote-button"]')))
    quote_button.submit()

    # Esperar explícitamente
    time.sleep(15)

    # Esperar a que el precio de la cotización esté presente
    price_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//p[@data-testid="offer-price"]')))

    # Extraer el precio de la cotización
    price_DHL = price_element.text.split(" ")[1]  # El precio está después del primer espacio en el texto
    print(f"El precio de la cotización es: {price_DHL}")

    # Cerrar el navegador
    driver.quit()

    return jsonify({'price_FEDEX': price_FEDEX, 'price_ESTAFETA': price_ESTAFETA, 'price_DHL': price_DHL})

if __name__ == "__main__":
    app.run(debug=True)
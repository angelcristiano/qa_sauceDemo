import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup():
    # Configura Chrome con webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    #driver.quit()


def test_login_success(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/")

    # 1️⃣ Localizamos los elementos
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    # 2️⃣ Introducimos credenciales válidas
    username_input.send_keys("standard_user")
    password_input.send_keys("secret_sauce")
    login_button.click()

    # 3️⃣ Verificamos que se inicia sesión correctamente
    assert "inventory.html" in driver.current_url, "❌ Error: el login no fue exitoso"
    print("✅ Inicio de sesión exitoso en SauceDemo.")


def test_login_failure(setup):
    driver = setup
    driver.get("https://www.saucedemo.com/")

    # Credenciales incorrectas
    driver.find_element(By.ID, "user-name").send_keys("usuario_falso")
    driver.find_element(By.ID, "password").send_keys("clave_incorrecta")
    driver.find_element(By.ID, "login-button").click()

    # Verificamos que aparece un mensaje de error
    error_message = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
    assert "Username and password do not match" in error_message, "❌ Error esperado no encontrado"
    print("✅ Mensaje de error mostrado correctamente.")

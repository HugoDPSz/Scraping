from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium_stealth import stealth

# Caminho do ChromeDriver no seu sistema
caminho_driver = r"C:\Users\user\Desktop\chromedriver\chromedriver.exe"  # <- ajuste se colocou em outra pasta
chrome_options = Options()

# Configurações para evitar detecção
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Desativa flags de automação
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Modo headless (se necessário)
chrome_options.add_argument("--headless=new")  # Usa o novo modo headless do Chrome
chrome_options.add_argument("--window-size=1920,1080")

service = Service(caminho_driver)
driver = webdriver.Chrome(service=service, options=chrome_options)
stealth(driver,
        languages=["pt-BR", "pt"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

# Acessa a página
url = "https://www.meutimao.com.br/artilharia-do-corinthians/2025/"
driver.get(url)

try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.relatorio"))
    )
    print("Página carregada com sucesso!")
except Exception as e:
    print(f"Erro ao carregar a página: {e}")
    driver.save_screenshot("erro.png")  # Salva um print do erro

#Descobrindo que fui bloqueado
html = driver.page_source
with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(html)
print("HTML salvo.")


# Pega o HTML renderizado
soup = BeautifulSoup(driver.page_source, 'html.parser')

jogadores = []

# Encontra a <ul class="relatorio">
ul_relatorio = soup.find('ul', class_='relatorio')

# Garante que a ul foi encontrada
if ul_relatorio:
    for jogador in ul_relatorio.find_all('li'):
        try:
            nome = jogador.select_one('h5 a span')
            info = jogador.select_one('div.info p em')

            # Verifica se os elementos foram encontrados antes de acessar o texto
            nome_texto = nome.get_text(strip=True) if nome else "Nome não encontrado"
            info_texto = info.get_text(strip=True) if info else "Info não encontrada"

            jogadores.append([nome_texto, info_texto])

        except Exception as e:
            print(f"Erro ao processar jogador: {e}")
else:
    print("ul.relatorio não encontrada!")

# Exibe os jogadores coletados
print(jogadores)

driver.quit()

import pandas as pd
df = pd.DataFrame(jogadores, columns=['Nome', 'Gols'])
df.to_csv('jogadores.csv', index=False)
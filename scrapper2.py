import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL del catálogo de productos
URL_CATALOGO = "https://www.jardepot.com/agricultura/aspersoras-motor-a-gasolina/page/4"

# Carpeta para guardar imágenes
CARPETA_DESCARGA = "imagenes_aspersora_motor"
os.makedirs(CARPETA_DESCARGA, exist_ok=True)

# Obtener el HTML de la página
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL_CATALOGO, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Buscar todas las etiquetas <img>
imagenes = soup.find_all("img")

# Descargar solo imágenes con URLs válidas
for img in imagenes:
    img_url = img.get("src")

    # Verificar si la URL es válida y no es base64
    if img_url and not img_url.startswith("data:image"):
        img_url = urljoin(URL_CATALOGO, img_url)  # Convertir URL relativa en absoluta
        img_name = os.path.join(CARPETA_DESCARGA, img_url.split("/")[-1])

        # Descargar imagen
        with open(img_name, "wb") as f:
            f.write(requests.get(img_url).content)
        print(f"✅ Descargada: {img_name}")

print("🎉 Descarga completada.")
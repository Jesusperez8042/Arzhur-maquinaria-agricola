import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import base64

# URL del sitio web
url = "https://www.jardepot.com/"

# Cambia esta línea para la carpeta de Descargas
output_folder = os.path.expanduser("~/Downloads/imagenes_jardepot")  # Para Windows y Mac

os.makedirs(output_folder, exist_ok=True)

# Obtener el contenido de la página
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Buscar todas las etiquetas <img>
images = soup.find_all("img")

# Descargar las imágenes
for img in images:
    img_url = img.get("src")
    
    if img_url:
        if img_url.startswith("data:"):  # Manejar imágenes en formato Base64
            header, encoded = img_url.split(",", 1)
            image_data = base64.b64decode(encoded)
            img_name = os.path.join(output_folder, f"image_base64_{images.index(img)}.png")
            
            with open(img_name, "wb") as img_file:
                img_file.write(image_data)
            print(f"Descargada (Base64): {img_name}")
        else:
            img_url = urljoin(url, img_url)
            
            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()
                
                img_name = os.path.join(output_folder, img_url.split("/")[-1])
                
                with open(img_name, "wb") as img_file:
                    img_file.write(img_response.content)
                
                print(f"Descargada: {img_name}")
            
            except requests.exceptions.RequestException as e:
                print(f"Error al descargar {img_url}: {e}")

print("✅ Descarga completada.")
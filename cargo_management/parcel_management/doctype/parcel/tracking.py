import requests
from bs4 import BeautifulSoup


def scrape_tracking_status(tracking_number):
    # Construir la URL con el tracking number
    url = f"http://everest.cargotrack.net/m/track.asp?track={tracking_number}"

    # Definir encabezados para la solicitud (opcional, puede ayudar a evitar bloqueos)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    # Realizar la solicitud GET
    response = requests.get(url, headers=headers)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar el contenido HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar el elemento que contiene el resultado
        # Primero, verificar si aparece "NOT FOUND"
        not_found = soup.find('strong', text='NOT FOUND')

        if not_found:
            return 'NOT FOUND'

        else:
            # Si no aparece "NOT FOUND", extraer el estado del envío
            # Buscamos el <strong> después de "Searching for tracking_number"
            search_text = f"Searching for {tracking_number}"
            searching_for = soup.find('strong', class_='ntextbig', text=search_text)

            if searching_for:
                # El siguiente <strong> debería contener el estado
                next_strong = searching_for.find_next('strong')
                if next_strong:
                    status = next_strong.get_text(strip=True)
                    return status
                else:
                    return 'Estado no encontrado en la página'
            else:
                return 'Formato inesperado de la página'
    else:
        return f'Error: Código de estado HTTP {response.status_code}'

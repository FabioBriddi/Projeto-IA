import googlemaps
from datetime import datetime
import os
import random

# --- Classe de Resposta Padrão ---
class RouteResponse:
    """Estrutura a resposta para ser compatível com a aplicação."""
    def __init__(self, order):
        self.waypoint_order = order

# --- LÓGICA INTERNA PARA A API REAL (PAGA) ---
def _route_real(origin, destination, waypoints, optimize_waypoints, mode):
    """Faz a chamada real à API do Google Maps."""
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    if not API_KEY:
        raise ValueError("A chave da API do Google Maps não foi encontrada na variável de ambiente.")

    gmaps = googlemaps.Client(key=API_KEY)
    print("--- CHAMANDO A API REAL DO GOOGLE MAPS (PAGA) ---")
    
    try:
        directions_result = gmaps.directions(
            origin,
            destination,
            waypoints=waypoints,
            optimize_waypoints=optimize_waypoints,
            mode=mode,
            departure_time=datetime.now()
        )
        if directions_result:
            return RouteResponse(directions_result[0]['waypoint_order'])
        else:
            return RouteResponse(list(range(len(waypoints))))
    except Exception as e:
        print(f"Erro na chamada da API Real: {e}")
        # Em caso de erro na API paga, retorna a rota simulada como fallback
        return _route_simulated(origin, destination, waypoints, optimize_waypoints, mode)

# --- LÓGICA INTERNA PARA A API SIMULADA (GRATUITA) ---
def _route_simulated(origin, destination, waypoints, optimize_waypoints, mode):
    """Simula a otimização de rota de forma aleatória."""
    print("--- USANDO A API SIMULADA (GRATUITA) ---")
    indices = list(range(len(waypoints)))
    if optimize_waypoints:
        random.shuffle(indices)
    return RouteResponse(indices)

# --- FUNÇÃO PRINCIPAL QUE SERÁ CHAMADA PELO APP.PY ---
def route(origin, destination, waypoints, use_paid_api=False, optimize_waypoints=False, mode='driving'):
    """
    Decide qual motor de otimização usar com base na permissão do usuário.
    """
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    # Condição para usar a API paga: o usuário deve ter permissão E a chave deve existir no .env
    if use_paid_api and API_KEY:
        return _route_real(origin, destination, waypoints, optimize_waypoints, mode)
    else:
        # Caso contrário, usa a simulação gratuita
        return _route_simulated(origin, destination, waypoints, optimize_waypoints, mode)

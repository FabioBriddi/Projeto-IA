import requests
import os
import random
import json
from datetime import datetime
from typing import List, Dict, Any
import re

# --- Função auxiliar para formatar endereços ---
def formatar_endereco_para_api(endereco: str) -> str:
    """
    Formata o endereço para melhor compatibilidade com a API do Google.
    Remove caracteres especiais desnecessários e adiciona cidade/estado se não estiver presente.
    """
    # Limpar espaços extras
    endereco = ' '.join(endereco.split())
    
    # Se o endereço não termina com cidade/estado, adicionar
    if not any(cidade in endereco.lower() for cidade in ['canoas', 'porto alegre', 'rs']):
        # Assumir Canoas, RS como padrão se não especificado
        if not endereco.endswith(','):
            endereco += ', Canoas, RS, Brasil'
        else:
            endereco += ' Canoas, RS, Brasil'
    
    return endereco

# --- Função auxiliar para logs ---
def obter_usuario_atual():
    """Obtém o login do usuário atual da sessão Flask."""
    try:
        from flask import session
        return session.get('user_login', 'usuario_desconhecido')
    except:
        return 'sistema'

def salvar_log_auditoria(api_name: str, user_login: str, tipo: str, dados: dict):
    """
    Salva logs de auditoria das chamadas de API.
    """
    try:
        # Criar pasta de logs se não existir
        logs_dir = r"C:\UniSenac-IA\STRANS-Projeto-IA\logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Timestamp para o log
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Nome do arquivo: nome_da_api_usuario_tipo.log
        nome_arquivo = f"{api_name}_{user_login}_{tipo}.log"
        caminho_arquivo = os.path.join(logs_dir, nome_arquivo)
        
        # Estrutura do log
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "api": api_name,
            "usuario": user_login,
            "tipo": tipo,
            "dados": dados
        }
        
        # Salvar log (append para manter histórico)
        with open(caminho_arquivo, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False, indent=2) + "\n" + "="*80 + "\n")
        
        print(f"📝 Log salvo: {nome_arquivo}")
        
    except Exception as e:
        print(f"⚠️  Erro ao salvar log de auditoria: {e}")

# --- Classe de Resposta Padrão ---
class RouteResponse:
    """Estrutura a resposta para ser compatível com a aplicação."""
    def __init__(self, order: List[int], total_distance: int = 0, total_duration: int = 0, route_data: Dict = None, legs_data: List[Dict] = None):
        self.waypoint_order = order
        self.total_distance_meters = total_distance
        self.total_duration_seconds = total_duration
        self.route_data = route_data or {}
        self.legs_data = legs_data or []

# --- LÓGICA INTERNA PARA A ROUTES API (OTIMIZADA) ---
def _route_optimization_api(origin: str, destination: str, waypoints: List[str], optimize_waypoints: bool, mode: str = 'DRIVE'):
    """
    Faz a chamada para a Google Routes API (Route Optimization).
    Esta API é mais moderna e oferece melhor otimização que a Directions API.
    """
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    usuario_atual = obter_usuario_atual()
    
    if not API_KEY:
        raise ValueError("A chave da API do Google Maps não foi encontrada na variável de ambiente.")
    
    print("--- CHAMANDO A ROUTES API (ROUTE OPTIMIZATION) ---")
    
    # Limpar e normalizar endereços
    origin = formatar_endereco_para_api(origin.strip())
    destination = formatar_endereco_para_api(destination.strip())
    waypoints = [formatar_endereco_para_api(w.strip()) for w in waypoints if w.strip()]
    
    print(f"🏁 Origem formatada: {origin}")
    print(f"🎯 Destino formatado: {destination}")
    print(f"📍 Total de waypoints limpos: {len(waypoints)}")
    
    # URL da Routes API
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    # Headers obrigatórios para a Routes API
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.optimizedIntermediateWaypointIndex,routes.legs.duration,routes.legs.distanceMeters'
    }
    
    # Construir waypoints intermediários
    intermediates = []
    for i, waypoint in enumerate(waypoints):
        if waypoint and len(waypoint) > 5:
            intermediates.append({"address": waypoint})
        else:
            print(f"⚠️  Waypoint {i} ignorado (endereço inválido): '{waypoint}'")
    
    # Payload para a Routes API
    payload = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "intermediates": intermediates,
        "travelMode": mode,
        "optimizeWaypointOrder": optimize_waypoints,
        "languageCode": "pt-BR",
        "regionCode": "BR", 
        "units": "METRIC"
    }
    
    if not optimize_waypoints:
        payload["routingPreference"] = "TRAFFIC_AWARE_OPTIMAL"
    else:
        payload["routingPreference"] = "TRAFFIC_UNAWARE"
    
    # Log de envio
    try:
        log_envio = {
            "url": url,
            "headers": {k: v for k, v in headers.items() if k != 'X-Goog-Api-Key'},
            "payload": payload,
            "method": "POST"
        }
        salvar_log_auditoria("routes", usuario_atual, "envio", log_envio)
    except:
        pass
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # Log de retorno
        try:
            log_retorno = {
                "status_code": response.status_code,
                "response_data": response.json() if response.status_code == 200 else response.text,
                "success": response.status_code == 200
            }
            salvar_log_auditoria("routes", usuario_atual, "retorno", log_retorno)
        except:
            pass
        
        if response.status_code == 200:
            data = response.json()
            
            if 'routes' in data and len(data['routes']) > 0:
                route = data['routes'][0]
                
                # Extrair ordem otimizada dos waypoints
                optimized_order = []
                if optimize_waypoints and 'optimizedIntermediateWaypointIndex' in route:
                    optimized_order = route['optimizedIntermediateWaypointIndex']
                else:
                    optimized_order = list(range(len(waypoints)))
                
                # Extrair métricas da rota
                total_distance = route.get('distanceMeters', 0)
                total_duration = 0
                if 'duration' in route:
                    duration_str = route['duration']
                    if duration_str.endswith('s'):
                        total_duration = int(duration_str[:-1])
                
                # Extrair dados dos trechos (legs)
                legs_data = []
                if 'legs' in route:
                    for leg in route['legs']:
                        leg_distance = leg.get('distanceMeters', 0)
                        leg_duration = 0
                        if 'duration' in leg:
                            duration_str = leg['duration']
                            if duration_str.endswith('s'):
                                leg_duration = int(duration_str[:-1])
                        
                        toll_cost = 0
                        if 'tollInfo' in leg and 'estimatedPrice' in leg['tollInfo']:
                            for price_info in leg['tollInfo']['estimatedPrice']:
                                if price_info.get('currencyCode') == 'BRL':
                                    toll_cost = price_info.get('units', 0) + price_info.get('nanos', 0) / 1000000000
                                    break
                        
                        legs_data.append({
                            'distance_meters': leg_distance,
                            'duration_seconds': leg_duration,
                            'toll_cost': toll_cost
                        })
                
                print(f"✅ Rota otimizada com sucesso!")
                print(f"   📏 Distância total: {total_distance/1000:.1f} km")
                print(f"   ⏱️  Tempo estimado: {total_duration//60:.0f} minutos")
                print(f"   🎯 Ordem otimizada: {optimized_order}")
                
                if optimize_waypoints and len(optimized_order) != len(waypoints):
                    print(f"⚠️  AVISO: Ordem otimizada tem {len(optimized_order)} elementos, mas temos {len(waypoints)} waypoints")
                    print("   Usando ordem original como fallback")
                    optimized_order = list(range(len(waypoints)))
                
                return RouteResponse(
                    order=optimized_order,
                    total_distance=total_distance,
                    total_duration=total_duration,
                    route_data=route,
                    legs_data=legs_data
                )
            else:
                print("❌ Nenhuma rota encontrada na resposta da API")
                return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
                
        else:
            print(f"❌ Erro na Routes API: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
            # Analisar erro específico
            if response.status_code == 400:
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        print(f"   Detalhes do erro: {error_data['error'].get('message', 'Erro desconhecido')}")
                except:
                    pass
            elif response.status_code == 403:
                print(f"   🔍 Erro 403: Problema de billing ou permissão da API key")
                # Se for erro de billing, fazer fallback para Directions API
                print(f"   ➡️  Tentando fallback para Directions API...")
                return _directions_api_com_fallback_billing(origin, destination, waypoints, optimize_waypoints, 'driving')
            
            return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout na Routes API - usando simulação")
        return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
    except requests.exceptions.RequestException as e:
        print(f"🌐 Erro de conexão na Routes API: {e}")
        return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
    except Exception as e:
        print(f"💥 Erro inesperado na Routes API: {e}")
        return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)

# --- LÓGICA INTERNA PARA A DIRECTIONS API (COM FALLBACK BILLING) ---
def _directions_api_com_fallback_billing(origin: str, destination: str, waypoints: List[str], optimize_waypoints: bool, mode: str = 'driving'):
    """Directions API com tratamento de erro de billing."""
    try:
        import googlemaps
        
        API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
        usuario_atual = obter_usuario_atual()
        
        if not API_KEY:
            print("❌ API Key não encontrada")
            return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
        
        gmaps = googlemaps.Client(key=API_KEY)
        print("--- USANDO DIRECTIONS API ---")
        
        # Log de envio
        try:
            log_envio = {
                "origin": origin,
                "destination": destination,
                "waypoints_count": len(waypoints),
                "optimize_waypoints": optimize_waypoints,
                "mode": mode,
                "api_type": "googlemaps_client"
            }
            salvar_log_auditoria("directions", usuario_atual, "envio", log_envio)
        except:
            pass
        
        directions_result = gmaps.directions(
            origin,
            destination,
            waypoints=waypoints,
            optimize_waypoints=optimize_waypoints,
            mode=mode
        )
        
        if directions_result:
            route = directions_result[0]
            waypoint_order = route.get('waypoint_order', list(range(len(waypoints))))
            
            total_distance = 0
            total_duration = 0
            legs_data = []
            
            for leg in route['legs']:
                leg_dist = leg['distance']['value']
                leg_dur = leg['duration']['value']
                total_distance += leg_dist
                total_duration += leg_dur
                
                legs_data.append({
                    'distance_meters': leg_dist,
                    'duration_seconds': leg_dur,
                    'toll_cost': 0
                })
            
            # Log de retorno
            try:
                log_retorno = {
                    "success": True,
                    "waypoint_order": waypoint_order,
                    "total_distance": total_distance,
                    "total_duration": total_duration,
                    "legs_count": len(route['legs'])
                }
                salvar_log_auditoria("directions", usuario_atual, "retorno", log_retorno)
            except:
                pass
            
            print(f"✅ Directions API sucesso: {total_distance/1000:.1f}km, {total_duration//60:.0f}min")
            
            return RouteResponse(
                order=waypoint_order,
                total_distance=total_distance,
                total_duration=total_duration,
                legs_data=legs_data
            )
        else:
            print("❌ Directions API: Nenhuma rota encontrada")
            return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
            
    except ImportError:
        print("❌ googlemaps library não instalada - usando simulação")
        return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
    except Exception as e:
        error_str = str(e).lower()
        if 'billing' in error_str or 'permission_denied' in error_str:
            print(f"⚠️  Directions API erro de billing: {e}")
        else:
            print(f"❌ Directions API erro: {e}")
        
        # Log de erro
        try:
            log_erro = {"error": str(e), "error_type": type(e).__name__}
            salvar_log_auditoria("directions", obter_usuario_atual(), "erro", log_erro)
        except:
            pass
        
        return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)

# --- LÓGICA INTERNA PARA A API SIMULADA (GRATUITA) ---
def _route_simulated_com_logs(origin: str, destination: str, waypoints: List[str], optimize_waypoints: bool, mode: str):
    """Simula a otimização de rota de forma mais inteligente."""
    print("--- USANDO SIMULAÇÃO (GRATUITA) ---")
    usuario_atual = obter_usuario_atual()
    
    # Log de envio
    try:
        log_envio = {
            "origin": origin,
            "destination": destination,
            "waypoints_count": len(waypoints),
            "optimize_waypoints": optimize_waypoints,
            "mode": mode,
            "api_type": "simulation"
        }
        salvar_log_auditoria("simulation", usuario_atual, "envio", log_envio)
    except:
        pass
    
    indices = list(range(len(waypoints)))
    
    if optimize_waypoints:
        print("🧠 Aplicando otimização inteligente simulada...")
        
        try:
            # Estratégia: Ordenar por similaridade de endereços
            waypoints_com_info = []
            for i, endereco in enumerate(waypoints):
                partes = endereco.split(',')
                rua = partes[0].strip() if len(partes) > 0 else ""
                numero = ""
                bairro = ""
                
                # Tentar extrair número da rua
                numeros = re.findall(r'\d+', rua)
                if numeros:
                    numero = int(numeros[0])
                else:
                    numero = 9999
                
                # Extrair bairro
                if len(partes) > 1:
                    bairro = partes[1].strip()
                
                waypoints_com_info.append({
                    'indice': i,
                    'endereco': endereco,
                    'rua': rua,
                    'numero': numero,
                    'bairro': bairro
                })
            
            # Ordenar por bairro primeiro, depois por rua, depois por número
            waypoints_com_info.sort(key=lambda x: (x['bairro'], x['rua'], x['numero']))
            indices = [item['indice'] for item in waypoints_com_info]
            
            print(f"🎯 Ordem otimizada por proximidade: {indices}")
            print("   Critério: bairro → rua → número")
            
        except Exception as e:
            print(f"⚠️  Erro na otimização, usando ordem sequencial: {e}")
            indices = list(range(len(waypoints)))
    else:
        print("📍 Mantendo ordem original dos waypoints")
    
    # Simular métricas básicas para cada trecho
    legs_data = []
    for i in range(len(waypoints) + 1):
        if i == 0:
            estimated_distance = random.randint(1500, 3500)
        elif i == len(waypoints):
            estimated_distance = random.randint(1000, 2500)
        else:
            estimated_distance = random.randint(800, 2000)
        
        velocidade_media = random.uniform(20, 30)
        estimated_duration = int((estimated_distance / 1000) / velocidade_media * 3600)
        
        legs_data.append({
            'distance_meters': estimated_distance,
            'duration_seconds': estimated_duration,
            'toll_cost': 0
        })
    
    total_distance = sum(leg['distance_meters'] for leg in legs_data)
    total_duration = sum(leg['duration_seconds'] for leg in legs_data)
    
    # Log de retorno
    try:
        log_retorno = {
            "success": True,
            "optimized_order": indices,
            "total_distance_meters": total_distance,
            "total_duration_seconds": total_duration,
            "legs_count": len(legs_data),
            "optimization_applied": optimize_waypoints
        }
        salvar_log_auditoria("simulation", usuario_atual, "retorno", log_retorno)
    except:
        pass
    
    print(f"🎲 Simulação - Distância: {total_distance/1000:.1f} km, Tempo: {total_duration//60:.0f} min")
    print(f"📊 {len(legs_data)} trechos simulados")
    
    return RouteResponse(
        order=indices,
        total_distance=total_distance,
        total_duration=total_duration,
        legs_data=legs_data
    )

# --- FUNÇÃO PRINCIPAL QUE SERÁ CHAMADA PELO APP.PY ---
def route(origin: str, destination: str, waypoints: List[str], has_api_key: bool = False, 
         user_profile: str = 'operador', optimize_waypoints: bool = False, mode: str = 'driving'):
    """
    Função principal com nova interface e fallback para billing.
    
    Args:
        origin: Endereço de origem
        destination: Endereço de destino  
        waypoints: Lista de endereços intermediários
        has_api_key: Se usuário tem API key válida
        user_profile: Perfil do usuário ('operador' ou 'administrador')
        optimize_waypoints: Se deve otimizar ordem dos waypoints
        mode: Modo de transporte
    
    Returns:
        RouteResponse com ordem otimizada e métricas
    """
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if not waypoints:
        print("⚠️  Nenhum waypoint fornecido")
        return RouteResponse(order=[], total_distance=0, total_duration=0)
    
    user_profile_clean = user_profile.strip().lower() if user_profile else 'operador'
    
    print(f"\n🎯 === ROUTE COM FALLBACK BILLING ===")
    print(f"   has_api_key: {has_api_key}")
    print(f"   user_profile: '{user_profile_clean}'")
    print(f"   API_KEY existe: {bool(API_KEY)}")
    print(f"   Waypoints: {len(waypoints)}")
    
    # LÓGICA CONDICIONAL ATUALIZADA
    if not has_api_key or not API_KEY:
        print("🎲 DECISÃO: Simulação (sem API key)")
        return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)
    
    elif has_api_key and user_profile_clean == 'operador':
        print("🚗 DECISÃO: Directions API (Operador)")
        return _directions_api_com_fallback_billing(origin, destination, waypoints, optimize_waypoints, 'driving')
    
    elif has_api_key and user_profile_clean == 'administrador':
        # TEMPORÁRIO: Admin usa Directions API até billing ser ativado
        # Quando billing estiver ativo, mudar para _route_optimization_api
        print("🚗 DECISÃO: Directions API (Admin temporário)")
        return _directions_api_com_fallback_billing(origin, destination, waypoints, optimize_waypoints, 'driving')
    
    else:
        print(f"🎲 DECISÃO: Simulação (perfil: '{user_profile_clean}')")
        return _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, mode)

# --- FUNÇÃO AUXILIAR PARA COMPARAR APIS ---
def compare_apis(origin: str, destination: str, waypoints: List[str], optimize_waypoints: bool = True):
    """
    Compara resultados entre Routes API, Directions API e simulação.
    Útil para testes e validação.
    """
    print("\n🔍 === COMPARAÇÃO DE APIs ===")
    
    results = {}
    
    # Testar Routes API
    try:
        routes_result = _route_optimization_api(origin, destination, waypoints, optimize_waypoints, 'DRIVE')
        results['routes'] = routes_result
    except Exception as e:
        print(f"Routes API falhou: {e}")
        results['routes'] = None
    
    # Testar Directions API
    try:
        directions_result = _directions_api_com_fallback_billing(origin, destination, waypoints, optimize_waypoints, 'driving')
        results['directions'] = directions_result
    except Exception as e:
        print(f"Directions API falhou: {e}")
        results['directions'] = None
    
    # Testar simulação
    sim_result = _route_simulated_com_logs(origin, destination, waypoints, optimize_waypoints, 'driving')
    results['simulation'] = sim_result
    
    # Comparar resultados
    print("\n📊 === RESULTADOS DA COMPARAÇÃO ===")
    for api_name, result in results.items():
        if result:
            print(f"{api_name.upper()}:")
            print(f"  🎯 Ordem: {result.waypoint_order}")
            print(f"  📏 Distância: {result.total_distance_meters/1000:.1f} km")
            print(f"  ⏱️  Tempo: {result.total_duration_seconds//60:.0f} min")
            print()
    
    return results
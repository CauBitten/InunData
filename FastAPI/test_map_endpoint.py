#!/usr/bin/env python3
"""
Teste para verificar se o endpoint do mapa está funcionando corretamente
"""

import requests
from datetime import datetime

def test_map_endpoint():
    """Testa o endpoint do mapa"""
    base_url = "http://localhost:8000"
    test_date = "2022-05-01"
    
    try:
        print(f"🧪 Testando endpoint: {base_url}/mapa_rmr/{test_date}")
        
        response = requests.get(f"{base_url}/mapa_rmr/{test_date}", timeout=30)
        
        if response.status_code == 200:
            print("✅ Endpoint funcionando!")
            print(f"📊 Tamanho da resposta: {len(response.text)} caracteres")
            
            # Verifica se é HTML válido
            if "<html" in response.text.lower() or "<!doctype" in response.text.lower():
                print("✅ Resposta contém HTML válido")
            else:
                print("⚠️ Resposta pode não ser HTML válido")
            
            # Verifica se contém elementos do Folium
            if "folium" in response.text.lower() or "leaflet" in response.text.lower():
                print("✅ Resposta contém elementos do Folium/Leaflet")
            else:
                print("⚠️ Resposta pode não conter mapa Folium")
                
        else:
            print(f"❌ Erro na resposta: {response.status_code}")
            print(f"📝 Mensagem: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - verifique se o servidor FastAPI está rodando")
    except requests.exceptions.Timeout:
        print("❌ Timeout - o servidor demorou muito para responder")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_health_check():
    """Testa se o servidor está funcionando"""
    base_url = "http://localhost:8000"
    
    try:
        print(f"🏥 Verificando saúde do servidor: {base_url}/docs")
        response = requests.get(f"{base_url}/docs", timeout=10)
        
        if response.status_code == 200:
            print("✅ Servidor FastAPI está funcionando!")
        else:
            print(f"⚠️ Resposta inesperada: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor FastAPI não está acessível")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🔍 TESTE DO ENDPOINT DO MAPA RMR")
    print("=" * 40)
    
    # Teste básico de conectividade
    test_health_check()
    print()
    
    # Teste do endpoint do mapa
    test_map_endpoint()

#!/usr/bin/env python3
"""
Teste para verificar a funcionalidade de extração de códigos CID-W
"""

def test_codigo_extraction():
    """Testa a extração de números dos códigos CID-W"""
    
    # Lista simulada como no código real
    cid_w_list = [
        "W00 - Queda no mesmo nível por escorregão, tropeção ou cambalhota",
        "W01 - Queda no mesmo nível por tropeção ou escorregão com colisão", 
        "W02 - Queda envolvendo patins, esqui, patinete ou pranchas",
        "W19 - Queda, não especificada",
        "W20 - Atingido por objeto lançado, projetado ou em queda",
        "W77 - Envolvimento ou engolfamento em avalanche, deslizamento ou outro movimento de massa"
    ]
    
    # Códigos de teste
    test_codes = ["W00", "W01", "W02", "W19", "W20", "W77"]
    
    print("=== Teste de Extração de Códigos CID-W ===")
    print()
    
    for code in test_codes:
        try:
            # Extrair XX de WXX e converter para int
            numero = int(code[1:])  # Remove o 'W' e converte para int
            if 0 <= numero < len(cid_w_list):
                description = cid_w_list[numero]
                print(f"Código: {code} -> Índice: {numero}")
                print(f"Descrição: {description}")
                print()
            else:
                print(f"Código: {code} -> Índice: {numero} (FORA DO INTERVALO)")
                print()
        except (ValueError, IndexError) as e:
            print(f"Erro ao processar {code}: {e}")
            print()
    
    print("=== Simulação com Pandas Series ===")
    import pandas as pd
    
    # Simular um resultado de value_counts()
    causas_data = {"W00": 5, "W19": 3, "W77": 2}
    causas = pd.Series(causas_data)
    
    print(f"Causas encontradas: {list(causas.index)}")
    
    descriptions = []
    for causa_code in causas.index:
        try:
            numero = int(causa_code[1:])
            if 0 <= numero < len(cid_w_list):
                descriptions.append(cid_w_list[numero])
            else:
                descriptions.append(f"{causa_code} - Código fora do intervalo válido")
        except (ValueError, IndexError):
            descriptions.append(f"{causa_code} - Código inválido")
    
    print("\\nDescrições que serão mostradas no gráfico:")
    for i, desc in enumerate(descriptions[:3]):  # Top 3
        print(f"{i+1}. {desc}")

if __name__ == "__main__":
    test_codigo_extraction()

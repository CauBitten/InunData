#!/usr/bin/env python3
"""
Teste simples para verificar o mapeamento CID-W
"""

def test_cid_mapping():
    """Testa o mapeamento existente"""
    
    # Simular o mapeamento como no código real
    cid_w_list = [
        "W00 - Queda no mesmo nível por escorregão, tropeção ou cambalhota",
        "W01 - Queda no mesmo nível por tropeção ou escorregão com colisão",
        "W02 - Queda envolvendo patins, esqui, patinete ou pranchas",
        # ... outros códigos existem no mapeamento original
    ]
    
    # Criar dicionário mapeando código para descrição (como no código original)
    mapping = {}
    for item in cid_w_list:
        codigo = item.split(' - ')[0]  # Extrai o código (ex: W00)
        mapping[codigo] = item
    
    print("=== Mapeamento CID-W ===")
    print()
    
    # Códigos de teste
    test_codes = ["W00", "W01", "W02", "W19", "W77"]
    
    for code in test_codes:
        if code in mapping:
            print(f"✅ {code}: {mapping[code]}")
        else:
            print(f"❌ {code}: Descrição não encontrada")
    
    print()
    print("=== Simulação de Resultado Final ===")
    import pandas as pd
    
    # Simular causas encontradas
    causas_data = {"W00": 5, "W01": 3, "W02": 1}
    causas = pd.Series(causas_data)
    
    descriptions = []
    for causa_code in causas.index:
        if causa_code in mapping:
            descriptions.append(mapping[causa_code])
        else:
            descriptions.append(f"{causa_code} - Descrição não encontrada")
    
    print("Texto que aparecerá abaixo do gráfico:")
    print("Principais causas do dia:")
    for i, desc in enumerate(descriptions[:3]):  # Top 3
        print(f"• {desc}")

if __name__ == "__main__":
    test_cid_mapping()

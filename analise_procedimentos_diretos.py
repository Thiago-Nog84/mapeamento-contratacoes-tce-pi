import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def analyze_dataset(filepath, orgao_label):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"=== {orgao_label} (Total compras: {len(data)}) ===")
    
    dispensas = []
    inexigibilidades = []
    adesao_carona = []
    
    for item in data:
        mod = item.get('modalidade', '')
        obj = item.get('objeto', '')
        num = item.get('numero_compra', '')
        val = item.get('valor_estimado', 0)
        arqs = len(item.get('arquivos', []))
        
        info = {'num': num, 'obj': obj, 'val': val, 'arqs': arqs, 'mod': mod}
        
        if any(w in obj.lower() for w in ['adesão', 'adesao', 'carona', 'ata de registro', 'arp', 'órgão não participante', 'orgao nao participante']):
            adesao_carona.append(info)
            
        if 'Dispensa' in mod:
            dispensas.append(info)
        elif 'Inexigibilidade' in mod:
            inexigibilidades.append(info)
            
    print(f"-> Dispensas: {len(dispensas)}")
    for d in dispensas[:8]:
        v = d['val'] if d['val'] else 0
        print(f"   [{d['num']}] R$ {v:,.2f} | Arqs: {d['arqs']} | {d['obj'][:90]}")
        
    print(f"\n-> Inexigibilidades: {len(inexigibilidades)}")
    for d in inexigibilidades[:8]:
        v = d['val'] if d['val'] else 0
        print(f"   [{d['num']}] R$ {v:,.2f} | Arqs: {d['arqs']} | {d['obj'][:90]}")
        
    print(f"\n-> Menções a Adesão / Carona / ARP: {len(adesao_carona)}")
    for d in adesao_carona[:8]:
        v = d['val'] if d['val'] else 0
        print(f"   [{d['num']}] ({d['mod']}) R$ {v:,.2f} | Arqs: {d['arqs']} | {d['obj'][:90]}")

analyze_dataset('contratacoes_mppi_pncp_2024.json', 'MPPI 2024')
print("\n" + "="*70 + "\n")
analyze_dataset('contratacoes_tce_pncp_2024.json', 'TCE-PI 2024')

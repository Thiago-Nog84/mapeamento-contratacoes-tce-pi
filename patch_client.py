with open('src/pncp_client.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """        data_ini = f"{ano}0101"
        data_fim = f"{ano}1231" """

# check without trailing space
lines = code.splitlines()
new_lines = []
for l in lines:
    if 'data_fim = f"{ano}1231"' in l:
        indent = l[:l.find('data_fim')]
        new_lines.append(f"{indent}from datetime import datetime")
        new_lines.append(f"{indent}data_ini = f'{{ano}}0101'")
        new_lines.append(f"{indent}agora = datetime.now()")
        new_lines.append(f"{indent}data_fim = agora.strftime('%Y%m%d') if ano >= agora.year else f'{{ano}}1231'")
    elif 'data_ini = f"{ano}0101"' in l:
        continue
    else:
        new_lines.append(l)

with open('src/pncp_client.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Patch aplicado em pncp_client.py!")

import re

with open('src/pncp_client.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('src/pncp_client.py', 'w', encoding='utf-8') as f:
    for line in lines:
        if line.startswith('    import time'):
            f.write(line[4:])
        elif line.startswith('    def _get'):
            f.write(line[4:])
        elif line.startswith('        req = urllib'):
            f.write(line[4:])
        elif line.startswith('            url,'):
            f.write(line[4:])
        elif line.startswith('            headers={'):
            f.write(line[4:])
        elif line.startswith('                "User-Agent"'):
            f.write(line[4:])
        elif line.startswith('                "Accept"'):
            f.write(line[4:])
        elif line.startswith('            }'):
            f.write(line[4:])
        elif line.startswith('        )'):
            f.write(line[4:])
        elif line.startswith('        for t in range(5):'):
            f.write(line[4:])
        elif line.startswith('            try:'):
            f.write(line[4:])
        elif line.startswith('                with urllib'):
            f.write(line[4:])
        elif line.startswith('                    return json'):
            f.write(line[4:])
        elif line.startswith('            except urllib'):
            f.write(line[4:])
        elif line.startswith('                if e.code'):
            f.write(line[4:])
        elif line.startswith('                    print('):
            f.write(line[4:])
        elif line.startswith('                    time.sleep(10)'):
            f.write(line[4:])
        elif line.startswith('                else:'):
            f.write(line[4:])
        elif line.startswith('                    return {}'):
            f.write(line[4:])
        elif line.startswith('            except Exception'):
            f.write(line[4:])
        elif line.startswith('                    time.sleep(5)'):
            f.write(line[4:])
        elif line.startswith('        return {}'):
            f.write(line[4:])
        else:
            f.write(line)

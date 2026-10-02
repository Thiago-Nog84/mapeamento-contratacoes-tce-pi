import sys
sys.stdout.reconfigure(encoding="utf-8")

for path in ["corpus_ia/contrato/2026_31_4_contrato_005.md", "corpus_ia/etp/2026_13_1_etp_001.md"]:
    print(f"=== {path} ===")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read()[:1500])
        print("\n" + "-"*50)

import json

json_path = r"E:\Thiago\Dev\Mapeamento TCE\dashboard\src\data\corpus_resumo.json"

with open(json_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

if "premio_boas_praticas" in corpus:
    corpus["premio_boas_praticas"]["nome_oficial"] = "PROJETO ANNONA"
    corpus["premio_boas_praticas"]["titulo"] = "PROJETO ANNONA: OBSERVATÓRIO DE GOVERNANÇA, PREÇOS E INTELIGÊNCIA EM CONTRATAÇÕES PÚBLICAS"
    corpus["premio_boas_praticas"]["subtitulo"] = "Inspirado na histórica magistratura romana da Cura Annonae: inteligência artificial, governança preventiva de riscos e padronização regional sob a Lei Federal nº 14.133/2021"
    corpus["premio_boas_praticas"]["origem_nome"] = "Inspirado na magistratura romana da Cura Annonae (Praefectus Annonae), instituída pelo imperador César Augusto em 7 d.C. para planejar compras públicas, fiscalizar fornecedores, combater o sobrepreço e garantir o abastecimento contínuo do Estado. Na doutrina clássica de Direito Administrativo, é reconhecida como o berço dos contratos administrativos no Ocidente."

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(corpus, f, indent=2, ensure_ascii=False)

print("corpus_resumo.json atualizado com o nome PROJETO ANNONA!")

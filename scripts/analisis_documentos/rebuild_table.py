import re
from pathlib import Path
import unicodedata

def normalize_name(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()

branch_keywords = {
    'paraiso': 'Paraíso',
    'poas': 'Poás',
    'nicoya': 'Nicoya',
    'santa elena': 'Santa Elena',
    'liberia': 'Liberia',
    'guatuso': 'Guatuso',
    'pacayas': 'Pacayas',
    'desamparados': 'Desamparados',
    'bagaces': 'Bagaces',
    'quepos': 'Quepos',
    'san rafael': 'San Rafael',
    'miramar': 'Miramar',
    'palmar norte': 'Palmar Norte',
    'guadalupe': 'Guadalupe',
    'la roxana': 'La Roxana',
    'roxana': 'La Roxana',
    'turrialba': 'Turrialba',
    'atenas': 'Atenas',
    'santo domingo': 'Santo Domingo',
    'limon': 'Limón',
    'ticaban': 'Ticabán',
    'union': 'La Unión',
    'puriscal': 'Puriscal',
    'tibas': 'Tibás',
    'guanacaste': 'Guanacaste',
    'chorotega': 'Chorotega',
}

lines = Path('document_list.txt').read_text(encoding='utf-8').strip().splitlines()
pattern = re.compile(r'^(?P<num>\d+)\.\s+(?P<doc>[^|]+)\|\s*(?P<trata>[^|]+)\|\s*(?P<antecedente>.+)$')
code_to_num = {}
for line in lines:
    match = pattern.match(line)
    if not match:
        continue
    num = match.group('num')
    doc = match.group('doc').strip()
    code_match = re.match(r'(GF[\w\-]+)', doc)
    if code_match:
        code_to_num[code_match.group(1).upper()] = num

rows = []
for line in lines:
    match = pattern.match(line)
    if not match:
        continue
    num = match.group('num')
    document = match.group('doc').strip()
    subject = match.group('trata').strip()
    antecedent = match.group('antecedente').strip()
    if subject.lower().startswith('trata de:'):
        subject = subject[len('trata de:'):].strip()
    if antecedent.lower().startswith('antecedente:'):
        antecedent = antecedent[len('antecedente:'):].strip()
    text_for_branch = f"{document} {subject}"
    norm_text = normalize_name(text_for_branch)
    branch = 'General'
    for key, label in branch_keywords.items():
        if key in norm_text:
            branch = label
            break
    if not antecedent:
        antecedent = 'No especificado'
    else:
        matches = re.findall(r'GF(?:\s|-)+(?:[A-Z0-9]+(?:-?[0-9]+)*)', antecedent.upper())
        if matches:
            candidate = matches[0].replace(' ', '')
            if candidate.endswith('-'):
                candidate = candidate[:-1]
            antecedent = code_to_num.get(candidate, candidate)
        elif 'SICOP' in antecedent.upper():
            antecedent = 'SICOP'
    rows.append((num, document, branch, subject, antecedent))

header = "| # | Documento | Sucursal | Trata de | Antecedente |"
separator = "| --- | --- | --- | --- | --- |"
body = "\n".join(f"| {num} | {doc} | {branch} | {subject} | {antecedent} |" for num, doc, branch, subject, antecedent in rows)
Path('document_table_with_branch.md').write_text(header + '\n' + separator + '\n' + body, encoding='utf-8')
print(f"Wrote table with {len(rows)} rows to document_table_with_branch.md")

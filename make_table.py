from pathlib import Path
lines = Path('document_list.txt').read_text(encoding='utf-8').strip().splitlines()
rows = []
for line in lines:
    parts = line.split(' | ')
    if len(parts) < 3:
        continue
    consec_title = parts[0].split('. ', 1)
    number = consec_title[0]
    title = consec_title[1] if len(consec_title) > 1 else parts[0]
    subject = parts[1].replace('Trata de: ', '').strip()
    antecedent = parts[2].replace('Antecedente: ', '').strip()
    rows.append((number, title, subject, antecedent))

header = "| # | Documento | Trata de | Antecedente |"
sep = "| --- | --- | --- | --- |"
body = "\n".join(f"| {num} | {title} | {subject} | {antecedent} |" for num, title, subject, antecedent in rows)
Path('document_table.md').write_text(header + '\n' + sep + '\n' + body, encoding='utf-8')
print(f"Wrote table with {len(rows)} rows to document_table.md")

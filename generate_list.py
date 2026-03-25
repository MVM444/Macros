import json
from pathlib import Path
path = Path('pdf_summaries_v2.json')
with path.open(encoding='utf-8') as fh:
    entries = json.load(fh)
lines = []
for idx, entry in enumerate(entries, start=1):
    title = Path(entry['path']).name
    subject_raw = entry['subject'].strip()
    if ':' in subject_raw:
        after = subject_raw.split(':', 1)[1].strip()
        subject = after if after else title
    else:
        subject = subject_raw or title
    antecedent = entry['antecedent'].strip() or entry['reference'].strip() or 'No especificado'
    lines.append(f"{idx}. {title} | Trata de: {subject} | Antecedente: {antecedent}")
with open('document_list.txt', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(lines))
print(f"Wrote {len(lines)} lines to document_list.txt")

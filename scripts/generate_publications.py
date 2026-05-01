#!/usr/bin/env python3
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB_DIR = ROOT / 'assets' / 'files' / 'bibtex'
OUT_DIR = ROOT / 'assets' / 'files' / 'publications'

ENTRY_RE = re.compile(r'@(?P<type>\w+)\s*\{\s*(?P<key>[^,]+),(?P<body>.*?)\n\}\s*(?=@|$)', re.S)


def clean_val(v: str) -> str:
    v = v.strip()
    if v.startswith('{') and v.endswith('}'):
        v = v[1:-1]
    if v.startswith('"') and v.endswith('"'):
        v = v[1:-1]
    return re.sub(r'\s+', ' ', v).strip()


def parse_fields(text: str):
    fields = {}
    i = 0
    n = len(text)
    while i < n:
        while i < n and text[i] in ' \t\r\n,':
            i += 1
        if i >= n:
            break
        if not (text[i].isalpha() or text[i] == '_'):
            i += 1
            continue
        start = i
        while i < n and (text[i].isalnum() or text[i] in '_-'):
            i += 1
        name = text[start:i].lower()
        while i < n and text[i] in ' \t\r\n':
            i += 1
        if i >= n or text[i] != '=':
            continue
        i += 1
        while i < n and text[i] in ' \t\r\n':
            i += 1
        if i >= n:
            break
        if text[i] == '{':
            depth = 0
            start = i
            while i < n:
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                i += 1
            val = text[start:i]
        elif text[i] == '"':
            start = i
            i += 1
            while i < n:
                if text[i] == '"' and text[i - 1] != '\\':
                    i += 1
                    break
                i += 1
            val = text[start:i]
        else:
            start = i
            while i < n and text[i] not in ',\n':
                i += 1
            val = text[start:i]
        fields[name] = clean_val(val)
    return fields


def parse_bib_file(path: Path):
    text = path.read_text(encoding='utf-8')
    entries = []
    for m in ENTRY_RE.finditer(text):
        etype = m.group('type')
        key = m.group('key').strip()
        body = m.group('body')
        fields = parse_fields(body)
        fields['_entry_type'] = etype
        fields['_key'] = key
        entries.append(fields)
    # if no matches, try simple fallback: whole file as one entry
    if not entries and text.strip():
        # try to parse lines like 'title = {...}'
        fields = parse_fields(text)
        if fields:
            fields['_entry_type'] = 'unknown'
            fields['_key'] = path.stem
            entries.append(fields)
    return entries


def classify_entry(fields: dict):
    if 'journal' in fields:
        return 'journal'
    if 'booktitle' in fields or fields.get('_entry_type','').lower() in ('inproceedings','conference','proceedings'):
        return 'conference'
    # fallback: if venue-like 'conference' in note or publisher
    note = fields.get('note','') + ' ' + fields.get('publisher','')
    if 'conference' in note.lower() or 'proceedings' in note.lower():
        return 'conference'
    return 'journal'


def to_record(fields: dict, bibid: str):
    title = fields.get('title','').replace('"','').replace('{','').replace('}','').strip()
    authors = fields.get('author','').replace('{','').replace('}','').strip()
    year = fields.get('year','')
    try:
        year = int(year)
    except Exception:
        year = None
    venue = fields.get('journal') or fields.get('booktitle') or fields.get('series') or ''
    return {
        'title': title,
        'authors': authors,
        'venue': venue,
        'year': year,
        'bibId': bibid
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    journals = []
    conferences = []

    for bib in sorted(BIB_DIR.glob('*.bib')):
        entries = parse_bib_file(bib)
        # prefer first entry for bibId mapping, but still process all
        for idx, fields in enumerate(entries):
            bibid = bib.stem
            kind = classify_entry(fields)
            rec = to_record(fields, bibid)
            if kind == 'journal':
                journals.append(rec)
            else:
                conferences.append(rec)

    # sort by year desc (None last)
    def sort_key(r):
        return (-(r['year'] or 0), r['title'])

    journals.sort(key=sort_key)
    conferences.sort(key=sort_key)

    (OUT_DIR / 'journals.json').write_text(json.dumps(journals, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT_DIR / 'conferences.json').write_text(json.dumps(conferences, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()

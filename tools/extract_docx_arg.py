import sys, os, zipfile, xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print('USAGE: script docx_file')
    sys.exit(1)

docx_file = sys.argv[1]
out_file = 'mdp_report_text_new.txt'
meta_file = 'mdp_report_meta_new.txt'

if not os.path.exists(docx_file):
    print('DOCX_NOT_FOUND')
    sys.exit(2)

with zipfile.ZipFile(docx_file, 'r') as z:
    try:
        xml = z.read('word/document.xml')
    except KeyError:
        print('NO_DOCUMENT_XML')
        sys.exit(3)
    root = ET.fromstring(xml)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paras = []
    for p in root.findall('.//w:p', ns):
        texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
        if texts:
            paras.append(''.join(texts))
    text = '\n\n'.join(paras)
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(text)
    pages = None
    try:
        app = z.read('docProps/app.xml')
        approot = ET.fromstring(app)
        pages_el = None
        for child in approot:
            if child.tag.lower().endswith('pages'):
                pages_el = child
                break
        if pages_el is not None:
            pages = pages_el.text
    except Exception:
        pages = None
    if pages is None:
        words = len(text.split())
        pages = max(1, (words // 450))
    with open(meta_file, 'w', encoding='utf-8') as m:
        m.write(f'PAGES:{pages}\nWORDS:{len(text.split())}\n')
    print('EXTRACT_OK')

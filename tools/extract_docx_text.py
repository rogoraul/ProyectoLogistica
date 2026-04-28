import zipfile,sys,os,xml.etree.ElementTree as ET

docx_file = 'mdp_report_rewritten_final_clean.docx'
out_file = 'mdp_report_text.txt'
meta_file = 'mdp_report_meta.txt'

if not os.path.exists(docx_file):
    print('DOCX_NOT_FOUND')
    sys.exit(2)

with zipfile.ZipFile(docx_file,'r') as z:
    # extract main document text
    try:
        xml = z.read('word/document.xml')
    except KeyError:
        print('NO_DOCUMENT_XML')
        sys.exit(3)
    root = ET.fromstring(xml)
    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paras = []
    for p in root.findall('.//w:p',ns):
        texts = [ t.text for t in p.findall('.//w:t',ns) if t.text ]
        if texts:
            paras.append(''.join(texts))
    text = '\n\n'.join(paras)
    with open(out_file,'w',encoding='utf-8') as f:
        f.write(text)
    # try to read page count from docProps/app.xml
    pages = None
    try:
        app = z.read('docProps/app.xml')
        approot = ET.fromstring(app)
        # try common namespace
        pages_el = None
        for child in approot:
            tag = child.tag
            if tag.lower().endswith('pages'):
                pages_el = child
                break
        if pages_el is not None:
            pages = pages_el.text
    except Exception:
        pages = None
    if pages is None:
        # fallback: estimate pages by word count (approx 450 words/page)
        words = len(text.split())
        pages = max(1, (words // 450))
    with open(meta_file,'w',encoding='utf-8') as m:
        m.write(f'PAGES:{pages}\nWORDS:{len(text.split())}\n')
    print('EXTRACT_OK')

import json, os, pyodbc
# Credential nam NGOAI repo - cam ghi vao bat ky file nao trong repo.
# Doi cho khac thi dat bien moi truong LEDGERREPORT_CONFIG.
CFG = os.environ.get('LEDGERREPORT_CONFIG',
                     r'D:\AI AGENT JOB\Nhat Ky Lam Viec LedgerReport\config.json')
conf = json.load(open(CFG, encoding='utf-8'))
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={conf["server"]};DATABASE={conf["database"]};UID={conf["uid"]};PWD={conf["pwd"]};Trusted_Connection=no;', timeout=5)
print([r.column_name for r in conn.cursor().columns(table='LEDGER') if 'CONTRA' in r.column_name.upper()])

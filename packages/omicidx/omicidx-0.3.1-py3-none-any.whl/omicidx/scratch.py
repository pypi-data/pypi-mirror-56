from calendar import monthrange
from omicidx import sra_parsers as s
import logging
s.logging.basicConfig(level=logging.INFO)

from sqlalchemy import Table, Column, String, MetaData, create_engine
from sqlalchemy.dialects.postgresql import JSONB, insert
import json
import datetime

def month_range(year, month):
    lastday = monthrange(year, month)[1]
    start = f"{year}-{month}-1"
    end = f"{year}-{month}-{lastday}"
    return((start,end,))

def _default(val):
    if isinstance(val, datetime.datetime):
        return str(val)
    raise TypeError()

def dumps(d):
    return json.dumps(d, default=_default)

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


engine = create_engine('postgresql://sdavis2@localhost/sdavis2', json_serializer = dumps)
metadata = MetaData()
tbl = Table('json_table', metadata,
            Column('accession', String(20), primary_key=True),
            Column('json', JSONB)
            )
try:
    metadata.create_all(engine)
except:
    pass

def main():
    conn = engine.connect()
    ins = insert(tbl)
    ins = ins.on_conflict_do_update(
        index_elements = ['accession'],
        set_ = dict(json=ins.excluded.json)
    )
    for y in range(2018,2020):
        for m in range(1,13):
            (from_date, to_date) = month_range(y, m)
            #from_date = f"{y}-{m}-{d}"
            #d = d+1
            #to_date = f"{y}-{m}-{d}"
            z = s.LiveList(from_date=from_date,to_date=to_date, count=5000, entity='EXPERIMENT', max_retries=10)
            inserts = []
            n = 0
            for h in z:
                n+=1
                if(h.accession is None):
                    continue
                inserts.append({"accession": h.accession, "json": h.dict()})
                if((n % 500) == 0):
                    conn.execute(ins, inserts)
                    inserts = []
            if(len(inserts)>0):
                conn.execute(ins, inserts)

if __name__ == '__main__':
    
    main()

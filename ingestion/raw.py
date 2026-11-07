import gzip
import os
import logging
from pathlib import Path
"""
    read from data all files
    in: data [directory]
    out: list of rows
"""
logger=logging.getLogger('raw')
handler=logging.FileHandler('raw.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

def to_rows(path:str):
    data_dir=Path(path)
    try:
        files= os.listdir(data_dir)
    except Exception as e:    
        logger.error('cannot list '+path+' : '+str(e))
        return 
    rows=[]
    for file in sorted(files):
        file_path=data_dir / file
        try:      
            open_type = gzip.open(file_path, mode='rt') if file.endswith('.gz') else open(file_path)
            with open_type as f:
                rows.extend(f.readlines())
        except Exception as e:
            logger.error('cannot read '+file+' : '+str(e))
    return rows
        
if __name__=='__main__':
    data=to_rows('./data')
    if data:
        print(data[:10])
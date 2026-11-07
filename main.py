from ingestion import raw 
from processing import extract_transforme

if __name__=='__main__':
    data=raw.to_rows('./data')
    if data:
        for row in data[:200]:
            result=extract_transforme.extract_from_row(row)
            if result:
                print(result)
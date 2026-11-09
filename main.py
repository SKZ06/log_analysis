from ingestion import raw 
from processing import extract_transforme
from processing import geo_location
from processing import dashboard

if __name__=='__main__':
    data=raw.to_rows('./data')
    if data:
        results=[]
        for row in data:
            result=extract_transforme.extract_from_row(row)
            if result:
                results.append(result)
        dashboard.failed_by_country(results, geo_location.get_country)
        dashboard.success_by_user(results)
        dashboard.failed_invalid_user(results)
        dashboard.show()
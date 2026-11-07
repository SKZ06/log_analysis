import os
import logging
import requests
"""
    in: ip
    out: location (country) of the ip
"""
logger=logging.getLogger('geo_location')
handler=logging.FileHandler('geo_location.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

URL_IPINFO = 'https://ipinfo.io'
cache={}
def get_location(ip):
    try:
        response=requests.get(URL_IPINFO+'/'+ip+'/json', params={'token': os.environ.get('IPINFO_TOKEN')}, timeout=10)
        if response.status_code==200:
            return response.json()
        logger.error('status '+str(response.status_code)+' for ip '+ip)
    except Exception as e:
        logger.error('cannot get location of '+ip+' : '+str(e))

def get_country(ip):
    if ip not in cache:
        location=get_location(ip)
        if location:
            cache[ip]=location.get('country', 'Unknown')
        else:
            cache[ip]='Unknown'
    return cache[ip]
    
if __name__=='__main__':
    print(get_country('138.199.39.186'))
import re
import logging
"""
    in: list of rows
    out:dateTime, ip, success, failed, invalid user
"""
logger=logging.getLogger('extract_transforme')
handler=logging.FileHandler('extract_transforme.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

pattern=re.compile(r'(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<server>\w+)\s+(?P<service>\w+)\[\d+\]:\s+(?P<message>.+)')
pattern_failed=re.compile(r'Failed password for (?P<invalid>invalid user )?(?P<user>\S*) from (?P<ip>\d+\.\d+\.\d+\.\d+)')
pattern_success=re.compile(r'Accepted \w+ for (?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)')

def extract_from_row(row):
    try:
        match=re.search(pattern,row)
        if match:
            row_data=match.groupdict()
            date_time=row_data['month']+' '+row_data['day']+' '+row_data['time']
            failed=re.search(pattern_failed,row_data['message'])
            if failed:
                return {'datetime': date_time, 'ip': failed.group('ip'), 'user': failed.group('user'), 'status': 'failed', 'invalid': failed.group('invalid') is not None}
            success=re.search(pattern_success,row_data['message'])
            if success:
                return {'datetime': date_time, 'ip': success.group('ip'), 'user': success.group('user'), 'status': 'success', 'invalid': False}
    except Exception as e:
        logger.error('cannot extract row '+row+' : '+str(e))
    return None
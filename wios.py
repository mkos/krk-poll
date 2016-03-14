import jsonimport urllibimport codecsimport requestsURL = 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz'HEADERS = {    'Accept': 'application/json, text/javascript, */*; q=0.01',    'Accept-Encoding': 'gzip, deflate',    'Accept-Language': 'pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4',    'Connection': 'keep-alive',    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',    'Host': 'monitoring.krakow.pios.gov.pl',    'Origin': 'http://monitoring.krakow.pios.gov.pl',    'Referer': 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/stacja/5/parametry/31-36-34-30-32/dzienny/16.05.2015',    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',    'X-Requested-With': 'XMLHttpRequest'}stations = {    4: 'Tarnow',    5: 'Skawina',    6: 'Aleja Krasinskiego',    7: 'Nowa Huta',    8: 'Nowy Sacz',    9: 'Zakopane',    10: 'Olkusz',    11: 'Trzebinia',    12: 'Szymbark',    15: 'Szarow',    16: 'Krakow-Kurdwanow',    19: 'Limanowa P',    20: 'Szczawnica P',    21: 'Kety P',    23: 'Slomniki P',    24: 'Myslenice P',    25: 'Bukowno P',    29: 'Sucha Beskidzka II',    148: 'Szarow Spokojna'}channels = {'pl_PL': {        47: 'Tlenki Azotu',        49: 'Benzen',        50: 'Tlenek Wegla',        53: 'Tlenek Azotu',        54: 'Dwutlenek Azotu',        57: 'PM10',        61: 'Dwutlenek Siarki',        146: 'Ozon',        211: 'PM25'},    'en_US': {        47: 'Nitrogen Monoxides',        49: 'Benzene',        50: 'Carbon Monoxide',        53: 'Nitrogen Monoxide',        54: 'Nitrogen Dioxide',        57: 'PM10',        61: 'Sulfur Dioxide',        146: 'Ozone',        211: 'PM25'    }}skip = ('avg', 'data', 'thresholds', 'thresholdsForAvg')labels = (    'timestamp', 'value', 'aggType', 'chartTooltipContent', 'count', 'coverageRate', 'decimals', 'extStartTime',    'interval',    'isAvgValid', 'label', 'ord', 'paramCode', 'paramId', 'paramLabel', 'paramPostfix', 'retroCount',    'scaleMax', 'scaleMin', 'startTime', 'unit', 'unitLabel')def blank(size):    return [None] * sizedef index_of(label):    return labels.index(label)def flatten(data, separator='.', prefix=''):    """    Flattens multilevel dicts into single level dicts combining keys for subsequent levels using specified separator.    If dictionary contains element with empty dictionary as a value, it will be removed from the result    Args:        data: dictionary to flatten        separator: used when creating flattened key identifiers        prefix: optional prefix for all key identifiers    Returns:        flattened dict if 'data' parameter was dict or empty dict otherwise    """    storage = {}    if isinstance(data, dict):        for key, value in data.items():            new_prefix = key if prefix == '' else prefix + separator + key            if isinstance(value, dict):                storage.update(flatten(value, separator=separator, prefix=new_prefix))            else:                storage[new_prefix] = value    return storageclass ResponseError(Exception):    """    Thrown when problems with server response occur.    """    passdef get_raw_data(encoded_query):    """    Sends request to WIOS server and retrieves data    Args:        encoded_query: of query parameters    Returns:        dict of JSON response from page    Raises:        ResponseError if couldn't retrieve valid data    """    raw_result = requests.post(URL, headers=HEADERS, data=encoded_query)    if raw_result.status_code != 200:        raise ResponseError('Server returned error {}: {}'.format(raw_result.status_code, raw_result.text))    result = json.loads(raw_result.content)    if not result['success']:        raise ResponseError('Server returned error \'{}\''.format(result['error']))    return resultdef prepare_query(year, month, day, station, channels, meas_type='Auto', view_type='Station', date_range='Day'):    """    Prepares encoded JSON query to retrieve data    Args:        year: integer year        month: integer month        day: integer day        station: integer        channels: list of integers representing pollution types        meas_type: type of measurement TODO: check other types of measurement        view_type: type of view TODO: check other types of view        date_range: daily or hourly reports TODO: check types od date range    Returns:        string of encoded JSON query    """    header = {        "measType": meas_type,        "viewType": view_type,        "dateRange": date_range,        "date": "{}.{}.{}".format(day, month, year),        "viewTypeEntityId": station,        "channels": channels    }    return "query=" + urllib.quote(json.dumps(header, separators=(",", ":")))if __name__ == '__main__':    from pprint import pprint    #from samples import SAMPLE_RESPONSE    # storage = flatten(SAMPLE_RESPONSE['data'])    # pprint(storage)    # if SAMPLE_RESPONSE['success']:    #    print "\n".join([str(x) for x in flatten(SAMPLE_RESPONSE['data'])])    # else:    #    print "Data retrieval failed"    prepared_query = prepare_query(2015, 5, 17, 5, [31, 36, 34, 30, 32])    #pprint(prepared_query)    result = get_raw_data(prepared_query)    pprint(result)
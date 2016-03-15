import jsonimport urllibimport codecsimport requestsDATA_URL = 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz'CONFIG_URL = 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/wczytaj-konfiguracje'HEADERS = {    'Accept': 'application/json, text/javascript, */*; q=0.01',    'Accept-Encoding': 'gzip, deflate',    'Accept-Language': 'pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4',    'Connection': 'keep-alive',    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',    'Host': 'monitoring.krakow.pios.gov.pl',    'Origin': 'http://monitoring.krakow.pios.gov.pl',    'Referer': 'http://monitoring.krakow.pios.gov.pl',    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',    'X-Requested-With': 'XMLHttpRequest'}stations = {    4: 'Tarnow',    5: 'Skawina',    6: 'Aleja Krasinskiego',    7: 'Nowa Huta',    8: 'Nowy Sacz',    9: 'Zakopane',    10: 'Olkusz',    11: 'Trzebinia',    12: 'Szymbark',    15: 'Szarow',    16: 'Krakow-Kurdwanow',    19: 'Limanowa P',    20: 'Szczawnica P',    21: 'Kety P',    23: 'Slomniki P',    24: 'Myslenice P',    25: 'Bukowno P',    29: 'Sucha Beskidzka II',    148: 'Szarow Spokojna'}channels = {'pl_PL': {        47: 'Tlenki Azotu',        49: 'Benzen',        50: 'Tlenek Wegla',        53: 'Tlenek Azotu',        54: 'Dwutlenek Azotu',        57: 'PM10',        61: 'Dwutlenek Siarki',        146: 'Ozon',        211: 'PM25'},    'en_US': {        47: 'Nitrogen Monoxides',        49: 'Benzene',        50: 'Carbon Monoxide',        53: 'Nitrogen Monoxide',        54: 'Nitrogen Dioxide',        57: 'PM10',        61: 'Sulfur Dioxide',        146: 'Ozone',        211: 'PM25'    }}class MeasPeriod:    DAY = 'day'    MONTH = 'month'    YEAR = 'year'class ViewType:    STATION = 'station'    PARAM = 'parameter'skip = ('avg', 'data', 'thresholds', 'thresholdsForAvg')labels = (    'timestamp', 'value', 'aggType', 'chartTooltipContent', 'count', 'coverageRate', 'decimals', 'extStartTime',    'interval',    'isAvgValid', 'label', 'ord', 'paramCode', 'paramId', 'paramLabel', 'paramPostfix', 'retroCount',    'scaleMax', 'scaleMin', 'startTime', 'unit', 'unitLabel')def flatten(data, separator='.', prefix=''):    """    Flattens multilevel dicts into single level dicts combining keys for subsequent levels using specified separator.    If dictionary contains element with empty dictionary as a value, it will be removed from the result    Args:        data: dictionary to flatten        separator: used when creating flattened key identifiers        prefix: optional prefix for all key identifiers    Returns:        flattened dict if 'data' parameter was dict or empty dict otherwise    """    storage = {}    if isinstance(data, dict):        for key, value in data.items():            new_prefix = key if prefix == '' else prefix + separator + key            if isinstance(value, dict):                storage.update(flatten(value, separator=separator, prefix=new_prefix))            else:                storage[new_prefix] = value    return storageclass ResponseError(Exception):    """    Thrown when problems with server response occur.    """    passdef xml_http_request(url, headers, data):    """    Sends XMLHttpRequest to given address with header and data    Args:        url: to send request to        headers: JSON formatted header, HTTP encoded        data: JSON formatted data, HTTP encoded    Returns:        dict of JSON response from page    Raises:        ResponseError if couldn't retrieve valid data    """    raw_result = requests.post(url=url, headers=headers, data=data)    if raw_result.status_code != 200:        raise ResponseError('Server returned error {}: {}'.format(raw_result.status_code, raw_result.text))    result = json.loads(raw_result.content)    if not result['success']:        raise ResponseError('Server returned error \'{}\''.format(result['error']))    return resultclass Config:    def __init__(self, url):        self.config = None        self.url = url        self.update()    def update(self):        """        Sends request to WIOS server and updates instance with new data (they are originally        used to configure web page)        Returns:            dict with retrieved raw config        Raises:            ResponseError if couldn't retrieve valid data        """        self.config = xml_http_request(CONFIG_URL, headers=HEADERS, data={'measType': 'auto'})['config']        return self.config    def get_raw_config(self):        """        Returns internally stored (with update() method) config from WIOS server        Returns:            dict with raw config        Raises:            ResponseError if couldn't retrieve valid data        """        return self.config    def get_raw_channels(self):        return self.config['channels']    def get_raw_stations(self):        return self.config['stations']    def get_raw_params(self):        return self.config['params']    def get_raw_thresholds(self):        return self.config['thresholds']def get_raw_data(encoded_query):    """    Sends request to WIOS server and retrieves data    Args:        encoded_query: of query parameters    Returns:        dict of JSON response from page    Raises:        ResponseError if couldn't retrieve valid data    """    raw_result = requests.post(DATA_URL, headers=HEADERS, data=encoded_query)    if raw_result.status_code != 200:        raise ResponseError('Server returned error {}: {}'.format(raw_result.status_code, raw_result.text))    result = json.loads(raw_result.content)    if not result['success']:        raise ResponseError('Server returned error \'{}\''.format(result['error']))    return resultdef prepare_query(year, month, day, station, channels, meas_type='Auto', view_type=ViewType.STATION, meas_period=MeasPeriod.DAY):    """    Prepares encoded JSON query to retrieve data    Args:        year: integer year        month: integer month        day: integer day        station: integer        channels: list of integers representing pollution types        meas_type: type of measurement TODO: check other types of measurement        view_type: whether server has to return data by pollution parameter for all of the stations or for one station            with all parameters. Available defines are in class ViewType        meas_period: can be one of defined in class MeasPeriod and defines period of measurements which can be daily,            monthly and yearly    Returns:        string of encoded JSON query    """    header = {        "measType": meas_type,        "viewType": view_type,        "dateRange": meas_period,        "date": "{}.{}.{}".format(day, month, year),        "viewTypeEntityId": station,        "channels": channels    }    return "query=" + urllib.quote(json.dumps(header, separators=(",", ":")))if __name__ == '__main__':    from pprint import pprint    #from samples import SAMPLE_RESPONSE    # storage = flatten(SAMPLE_RESPONSE['data'])    # pprint(storage)    # if SAMPLE_RESPONSE['success']:    #    print "\n".join([str(x) for x in flatten(SAMPLE_RESPONSE['data'])])    # else:    #    print "Data retrieval failed"    #prepared_query = prepare_query(2015, 5, 17, 5, [31, 36, 34, 30, 32])    #pprint(prepared_query)    #result = get_raw_data(prepared_query)    config = Config(CONFIG_URL)    result = config.get_raw_stations()    pprint(result)
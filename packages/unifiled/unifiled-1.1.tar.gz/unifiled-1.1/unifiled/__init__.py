import json
import time
from datetime import datetime

import requests
import urllib3

# fix cert warnigns
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class unifiled:
    _ip = None
    _port = None
    _debug = False
    _authorization = None
    _headers = None
    _cache = None
    _cache_max_age = None
    _cache_devices_last_change = 0
    _cache_devices_data = None
    _cache_groups_last_change = 0
    _cache_groups_data = None

    def __init__(self, _ip, _port, username, password, debug=False, autologin=True, cache=True, cache_max_age=15):
        self._ip = _ip
        self._port = _port
        self._debug = debug
        self._cache = cache
        self._cache_max_age = cache_max_age
        if autologin:
            self.login(username, password)

    def debug_log(self, text):
        if self._debug:
            print(f"{datetime.now()}: {text}")

    def login(self, username, password):
        self.debug_log(f"Logging in: {username}")
        _json = {
            'username': username,
            'password': password
        }

        try:
            login_req = requests.post('https://' + self._ip + ':' + self._port + '/v1/login', data=_json, verify=False, timeout=5)
        except:
            return False

        if login_req.status_code == 200:
            self._authorization = login_req.json()['access_token']
            self._headers = {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Authorization': 'Bearer ' + self._authorization,
            }
            return True
        else:
            return False

    def get_devices(self):
        self.debug_log('Getting devices')
        if (self._cache == True):
            self.debug_log('Getting devices using caching')
            if(self._cache_devices_last_change < (time.time() - self._cache_max_age)):
                self.debug_log('Getting devices cache is expired')
                try:
                    getdevices_req = requests.get('https://' + self._ip + ':' + self._port + '/v1/devices', headers=self._headers, verify=False, timeout=5)
                except:
                    return None
                if getdevices_req.status_code == 200:
                    self._cache_devices_last_change = time.time()
                    self._cache_devices_data = getdevices_req.json()
                    return self._cache_devices_data
                else:
                    raise ValueError('Could not get devices')
            else:
                self.debug_log('Getting devices cache is valid')
                return self._cache_devices_data
        else:
            try:
                getdevices_req = requests.get('https://' + self._ip + ':' + self._port + '/v1/devices', headers=self._headers, verify=False, timeout=5)
            except:
                return None
            if getdevices_req.status_code == 200:
                return getdevices_req.json()
            else:
                raise ValueError('Could not get devices')

    def get_groups(self):
        self.debug_log('Getting groups')
        if(self._cache == True):
            self.debug_log('Getting groups using caching')
            if(self._cache_groups_last_change < (time.time() - self._cache_max_age)):
                self.debug_log('Getting groups cache is expired')
                try:
                    getgroups_req = requests.get('https://' + self._ip + ':' + self._port + '/v1/groups', headers=self._headers, verify=False, timeout=5)
                except:
                    return None
                if getgroups_req.status_code == 200:
                    self._cache_groups_last_change = time.time()
                    self._cache_groups_data = getgroups_req.json()
                    return self._cache_groups_data
                else:
                    raise ValueError('Could not get groups')
            else:
                self.debug_log('Getting groups cache is valid')
                return self._cache_groups_data
        else:
            try:
                getgroups_req = requests.get('https://' + self._ip + ':' + self._port + '/v1/groups', headers=self._headers, verify=False, timeout=5)
            except:
                return None
            if getgroups_req.status_code == 200:
                return json.loads(getgroups_req.content)
            else:
                raise ValueError('Could not get groups')

    def set_device_brightness(self, id, brightness):
        self.debug_log(f"Setting brightness to {brightness} for device {id}")
        data = '{"command":"sync","value":' + str(brightness) + '}'
        setdeviceoutput_req = requests.put('https://' + self._ip + ':' + self._port + '/v1/devices/' + str(id), data=data, headers=self._headers, verify=False, timeout=5)
        self._cache_devices_last_change = 0
        if setdeviceoutput_req.status_code == 200:
            return True
        else:
            raise ValueError('Could not set brightness')

    def set_device_output(self, id, output):
        self.debug_log(f"Setting output to {output} for device {id}")
        data = '{"command":"config-output","value":' + str(output) + '}'
        setdeviceoutput_req = requests.put('https://' + self._ip + ':' + self._port + '/v1/devices/' + str(id), data=data, headers=self._headers, verify=False, timeout=5)
        self._cache_devices_last_change = 0
        if setdeviceoutput_req.status_code == 200:
            return True
        else:
            raise ValueError('Could not set output')

    def set_group_output(self, id, output):
        self.debug_log(f"Setting output to {output} for group {id}")
        data = '{"command":"config-output","value":' + str(output) + '}'
        setdeviceoutput_req = requests.put('https://' + self._ip + ':' + self._port + '/v1/group/' + str(id), data=data, headers=self._headers, verify=False, timeout=5)
        self._cache_devices_last_change = 0
        self._cache_groups_last_change = 0
        if setdeviceoutput_req.status_code == 200:
            return True
        else:
            raise ValueError('Could not set output')

    def get_login_state(self):
        self.debug_log('Checking login states')
        devices = self.get_devices()
        if devices != None:
            return True
        else:
            return False

    def convert_from_255_to_100(self,value):
        self.debug_log(f"Converting {value} from 0-255 scale to 0-100 scale")
        oldmin = 0
        oldmax = 255
        newmin = 0
        newmax = 100
        oldrange = (oldmax - oldmin)
        newrange = (newmax - newmin)
        convertedvalue = (((int(value) - oldmin) * newrange) / oldrange) + newmin
        return int(convertedvalue)

    def convert_from_100_to_255(self,value):
        self.debug_log(f"Converting {value} from 0-100 scale to 0-255 scale")
        oldmin = 0
        oldmax = 100
        newmin = 0
        newmax = 255
        oldrange = (oldmax - oldmin)
        newrange = (newmax - newmin)
        convertedvalue = (((int(value) - oldmin) * newrange) / oldrange) + newmin
        return int(convertedvalue)

    def get_lights(self):
        lights = []
        devices = self.get_devices()
        for device in devices:
            if device['type'] == 'LED':
                lights.append(device)
        return lights

    def get_sensors(self):
        sensors = []
        devices = self.get_devices()
        for device in devices:
            if device['type'] != 'LED':
                sensors.append(device)
        return sensors

    def get_light_state(self, id):
        devices = self.get_devices()
        for device in devices:
            if device['id'] == str(id):
                if device['status']['output'] == 1:
                    return True
                else:
                    return False
        return False

    def get_light_brightness(self, id):
        devices = self.get_devices()
        for device in devices:
            if device['id'] == str(id):
                return int(device['status']['led'])
        return False

    def get_light_available(self, id):
        devices = self.get_devices()
        for device in devices:
            if device['id'] == str(id):
                if device['isOnline'] == True:
                    return True
                else:
                    return False
        return False

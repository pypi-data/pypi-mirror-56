from request import CityAirRequest
TAKE_COUNT = 5

r = CityAirRequest('ek', 'Oracle23')

"""if True:
    devices_df= r.get_devices(format = 'raw', include_children = True)
    devices_dicts = r.get_devices(format = 'dicts', include_children = True)
    print(devices_df.tail(2))
    print(devices_dicts[:2])

"""
devices_list = r.get_devices(format = 'list', include_children = True)
print(devices_list[:2])
serial_number  = 'CA01PM000105'#devices_list[80]
print(f"getting data for the {serial_number} device")
assert isinstance(serial_number, str), f'Serial number should be string got {type(serial_number)} instead'

device_data_df = r.get_device_data(serial_number, take_count=TAKE_COUNT)
print(f"-----------------device data____________\n{device_data_df}")

device_data_df = r.get_device_data(serial_number, take_count=TAKE_COUNT, all_cols=True)
print(f"-----------------device data all cols____________\n{device_data_df}")



device_data_dicts = r.get_device_data(serial_number, separate_device_data=True, take_count=TAKE_COUNT)

print(device_data_df.head(2))
for d in device_data_dicts:
    print(device_data_dicts[d].head(2))

for station_info in r.get_stations(format = 'dicts')[:2]:
    print(station_info)

station_ids = r.get_stations()
print(f"first station_ids: {station_ids[:5]}")
print(f"---------------------packets from station--------------\n{r.get_station_data(station_ids[3]).head(5)}")


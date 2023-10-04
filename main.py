from map import Map


# Change path to save html file (absolute or relative path)
path_to_save = './map.html'
# Change path to Records.json (absolute or relative path)
path_to_data = r'C:\Users\User\Downloads\Records.json'


if __name__ == '__main__':
    map = Map(path_to_save, path_to_data)
    map.analysis()
    map.create_map()
    map.open()

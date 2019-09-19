import os


def append_to_file(path, response):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    tmp_path = os.path.realpath(script_directory).split('/')
    tmp_path = '/'.join(tmp_path[:(len(tmp_path) - 1)])
    path = '/'.join([tmp_path, path])
    with open(file=path, mode='a') as f:
        f.write(response.url)
        f.write('\n')
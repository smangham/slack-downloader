import os
import sys
import json
from urllib import request


def parse_messages(messages, folder, log):
    """
    Parses the messages and saves them to a subfolder

    Args:
        messages (list): List of json messages
        folder (string): Name of the channel folder
        log (list): List of error messages
    """
    for message in messages:
        if 'file' in message:
            if 'image' in message['file']['mimetype']:
                try:
                    os.makedirs(os.path.join(folder), exist_ok=True)
                    f = open(os.path.join(folder, message['file']['name']), 'wb')
                    f.write(request.urlopen(message['file']['url_private']).read())
                    f.close()
                except Exception as exception:
                    log.append("{}: {1}: {2!r}".format(
                        folder, type(exception).__name__, exception.args))


log = []
folders = []

assert len(sys.argv) > 1, \
    'Usage: python {} [downloaded data directory] [any number of subfolders]'.format(sys.argv[0])
root_path = sys.argv[1]
assert os.path.isdir(root_path), 'Error: {} is not a directory!'.format(root_path)
for arg in sys.argv[2:]:
    assert os.path.isdir(os.path.join(root_path, arg)), \
        "Error: {}/{} is not a directory!".format(root_path, arg)
    folders.append(arg)

for folder in folders:
    try:
        for file in os.listdir(os.path.join(root_path, folder)):
            if file.endswith('.json'):
                with open(os.path.join(root_path, folder, file)) as data_file:
                    parse_messages(json.load(data_file),
                                   os.path.join(root_path, 'save_slack_images', folder), log)
    except OSError as exception:
        log.append("{}: {1}: {2!r}".format(
            folder, type(exception).__name__, exception.args))

for entry in log:
    print(entry)

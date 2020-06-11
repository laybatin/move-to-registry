import subprocess
import requests
import json

host='registry.host.com'
port='16443'
url_addr='{}:{}/v2'.format(host,port)

print(url_addr)

r = requests.get('https://{}/_catalog'.format(url_addr))

js = json.loads(r.content)

#print(js)

tag_format='https://' + url_addr + '/{IMAGE_NAME}/tags/list'

new_port = ''  #ex) :5000
if js['repositories'] != None:
    for v in js['repositories']:
        tag_request = json.loads(requests.get(tag_format.format(IMAGE_NAME=v)).content)
        if tag_request['tags']:
            for tag in tag_request['tags']:
                image_path = '{HOST}:{PORT}/{IMAGE_NAME}:{TAG}'.format(HOST=host, PORT=port, IMAGE_NAME=v, TAG=tag)
                change_image_path = '{HOST}{PORT}/{IMAGE_NAME}:{TAG}'.format(HOST=host, PORT=new_port, IMAGE_NAME=v, TAG=tag)
                print(image_path + "-->" + change_image_path)

                subprocess.check_output(['docker', 'pull', image_path], universal_newlines=True)
                subprocess.check_output(['docker', 'tag', image_path, change_image_path], universal_newlines=True)
                subprocess.check_output(['docker', 'push', change_image_path], universal_newlines=True)

import cv2

import detect
import camera, img
import cStringIO
import numpy as np


detector = detect.Detector()

def process_image(image):
	opencv_img = img.create_opencv_image_from_stringio(image)
	if (opencv_img is None):
		return ':('
	lastUserId, lastUserName = detector.detect_face(opencv_img)
	return (lastUserId, lastUserName)

lastUserName = ''
lastUserId = 0

def app(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	resp = ''

	if (request_body_size == 0 and environ.get('PATH_INFO') == '/lastuser'):
		resp = json.dumps({'user_name': lastUserName, 'user_id': lastUserId})
	else:
		print 'req size: %d' % request_body_size
		request_body = environ['wsgi.input'].read(request_body_size)
		user_name, user_id = process_image(cStringIO.StringIO(request_body))
		resp = user_name
	
	data = "%s" % resp

	start_response("200 OK", [
	  ("Content-Type", "text/plain"),
	  ("Content-Length", str(len(data)))
	])
	return iter([data])

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', detector.conf_json['port'], app)
    print('running on port %d' % detector.conf_json['port'])
    srv.serve_forever()

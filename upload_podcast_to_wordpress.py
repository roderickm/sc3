#!/usr/bin/python
# This script requires the python-wordpress-xmlrpc module. To install, run the following:
#			sudo easy_install python-wordpress-xmlrpc
# Module docs at:
# http://python-wordpress-xmlrpc.readthedocs.org/en/latest/overview.html#installation
# http://sourceforge.net/projects/sox/files/latest/download?source=files

# Run from launchd?
#  http://hints.macworld.com/article.php?story=20080423051638134

#Take optional arguments:
#upload_podcast_to_wordpress.py <local_file_to_be_uploaded> <uploaded_name>
# Example:
#   upload_podcast_to_wordpress.py \
#			'/Users/Summit/Music/Nicecast Broadcast Archive/Nicecast Archived Audio 20130428 1120.mp3' \
#			'2013.04.28_madison_whaley.mp3'
# If no uploaded_name provided, generate one based on the file create time
# If no local_filename provided, look for most recent mp3 file over 9MB in size.


### Configuration settings (edit these as needed)
xmlrpc_url  = 'http://example.com/wp/xmlrpc.php'
xmlrpc_user = 'wordpressuser'
xmlrpc_pass = 'wordpresspass'

### These default settings can be overridden with command-line switches
campus = 'madison'
speaker = 'whaley'

# If input file is not specified, get the latest MP3 file in this directory...
path = '/Users/summit/Music/Nicecast Broadcast Archive/'

# ...that is at least this many bytes in size:
min_size = 9 * 1024 * 1024

import os, sys, time, argparse, mimetypes
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts


def get_recent_file(path=os.getcwd(),exten='.mp3',min_size=min_size):
	"""return the filename of the latest file in <path> with filename ending in <exten> and a size of at least <min_size> bytes"""
	os.chdir(path)
	filelist = os.listdir('.')
	filelist = filter(lambda x: not os.path.isdir(x), filelist)
	filelist = filter(lambda x: x.endswith(exten), filelist)
	filelist = filter(lambda x: os.stat(x).st_size > min_size, filelist)
	recent_file = max(filelist, key=lambda x: os.stat(x).st_mtime)
	return recent_file

def gen_filename(inputfile,campus='madison',speaker='whaley'):
	"""generate a filename using the convention (yyyy.mm.dd_campus_speaker.mp3)"""
	try:
		# We expect to see a filename of the form "Nicecast Archived Audio 20130428 1120.mp3"
		inputfile_list = inputfile.split()
		gen_date = time.strptime(inputfile_list[3] + inputfile_list[4],'%Y%m%d%H%M.mp3')
	except Exception, e:
		# Couldn't create a datetime object from filename, using current datetime.
		# Proceed silently or raise e?
		gen_date = time.gmtime()
	return '_'.join([time.strftime("%Y.%m.%d",gen_date),campus,speaker]) + '.mp3'

def upload_to_wordpress(xmlrpc_url,xmlrpc_user,xmlrpc_pass,inputfile,name):
	"""upload to <xmlrpc_url> as <xmlrpc_user>, <xmlrpc_pass> the <inputfile> as <name>"""
	global path
	metadata = {
		'name': name,
		'type': mimetypes.guess_type(inputfile)[0] or 'audio/mpeg',
	}
	try:
		print xmlrpc_url,xmlrpc_user,xmlrpc_pass
		wpclient = Client(xmlrpc_url,xmlrpc_user,xmlrpc_pass)
		fh = open('/'.join([path,inputfile]))
		# Read input file and encode as base64
		with open(filename, 'rb') as fh:
			data['bits'] = xmlrpc_client.Binary(fh.read())
		response = wpclient.call(media.UploadFile(metadata))
		# Expected response:
		#	response == {
		#		'id': 6,
		#		'name': '2013.04.28_madison_whaley.mp3',
		#		'url': 'http://summitcrossing.org/wp-content/uploads/2013/04/28/2013.04.28_madison_whaley.mp3',
		#		'type': 'audio/mpeg',
		#	}
		if response['id']:
			# If upload succeeded, rename input file:
			os.rename(inputfile,name)
	except IOError as e:
		print("({})".format(e))
	return response

def main():
	"""Parse arguments, then upload a file to wordpress"""
	global campus, speaker, inputfile, path, xmlrpc_url, xmlrpc_user, xmlrpc_pass
	parser = argparse.ArgumentParser(description='Upload a file to Wordpress. If no file specified, use a recent MP3.')
	parser.add_argument('-i','--input',help='filename to be uploaded')
	parser.add_argument('-n','--name',help='name of file after uploading')
	parser.add_argument('-c','--campus',help='name of campus')
	parser.add_argument('-s','--speaker',help='name of speaker')
	args = parser.parse_args()
	
	if not args.input:
		inputfile = get_recent_file(path,'.mp3',min_size)
	else:
		inputfile = os.path.basename(args.input)
		path = os.path.dirname(args.input)

	if isinstance(args.campus, str):
		campus = args.campus
	if isinstance(args.speaker, str):
		speaker = args.speaker
	if isinstance(args.name,str):
		name = args.name
	else:
		name = gen_filename(inputfile,campus,speaker)

#	print "IN:  " + inputfile
#	print "OUT: " + name

	try:
		upload_to_wordpress(xmlrpc_url,xmlrpc_user,xmlrpc_pass,inputfile,name)
	except IOError as e:
		print("({})".format(e))

if __name__ == "__main__":
	main()
	exit()

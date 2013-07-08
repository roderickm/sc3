#!/usr/bin/python
# This script requires the python-wordpress-xmlrpc module. 
# To install, first run the following:
#	sudo easy_install python-wordpress-xmlrpc

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts

xmlrpc_url  = 'http://example.com/wp/xmlrpc.php'
xmlrpc_user = ''
xmlrpc_pass = ''

client = Client(xmlrpc_url,xmlrpc_user,xmlrpc_pass)

posts = client.call(posts.GetPosts())
print posts

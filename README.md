sc3
===

## Tools and scripts for SC3

### upload_podcast_to_wordpress.py

Upload a file to Wordpress. If no file specified, use a recent MP3.

Be sure to edit the script to include the XML-RPC URL, username, and password for your Wordpress site.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        filename to be uploaded
  -n NAME, --name NAME  name of file after uploading
  -c CAMPUS, --campus CAMPUS
                        name of campus
  -s SPEAKER, --speaker SPEAKER
                        name of speaker

### getposts.py

Just a little test script to read the Wordpress posts via XML-RPC. I use it to be sure that Wordpress is responding properly over XML-RPC.

## Tools and scripts for SC3

### upload_podcast_to_wordpress.py

This script uploads a file to Wordpress. I wrote it so the weekly recordings could be sent to Wordpress automatically rather than emailed or sent to someone for manual uploading. 

If run with no arguments, it will look for a recent MP3 file larger than a certain size (9MB default), generate a name for the uploaded file, and then upload the file to Wordpress.

The generated filename is in the format YYYY.MM.DD_campus_speaker.mp3.

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

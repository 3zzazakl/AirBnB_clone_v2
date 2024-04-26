#!/usr/bin/env bash
# setting environment for web_static
sudo apt -y update
sudo apt -y upgrade
sudo apt -y install nginx

sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

# creating a fake html for testing
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# setting Nginx congs files
config_file="/etc/nginx/sites-available/default"

if ! grep -q "hbnb_static" $config_file; then
  sudo sed -i '/server_name _;/a\\n\tlocation /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}\n' "$config_file"
fi

sudo service nginx restart

exit 0

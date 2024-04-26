# configure web static

$nginx_config = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header 'X-Served-By' ${hostname};
    root /var/www/html;
    index index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current;
        autoindex on;
    }
    location /redirect_me {
        return 301 https://www.youtube.com;
    }
    error_page 404 /404.html;
    location = /404 {
        root /var/www/html;
        internal;
    }
}"

package { 'nginx':
    ensure => installed;
}

-> file { '/data/':
    ensure => directory;
}

-> file { '/data/web_static/':
    ensure => directory;
}

-> file { '/data/web_static/releases':
    ensure => directory;
}

-> file { '/data/web_static/releases/test':
    ensure => directory;
}

-> file { '/data/web_static/releases/test/index.html':
    ensure => file;
    content => "Holberton School\n";
}

-> file { '/data/web_static/shared':
    ensure => directory;
}

-> file { '/data/web_static/current':
    ensure => link;
    target => '/data/web_static/releases/test';
}

-> exec { 'chown_data':
    command => 'chown -R ubuntu:ubuntu /data';
}

-> file { '/var/www':
    ensure => directory;
}

-> file { '/var/www/html':
    ensure => directory;
}

-> file { '/var/www/html/index.html':
    ensure => file;
    content => "Holberton School\n";
}

-> file { '/var/www/html/404.html':
    ensure => file;
    content => "Ceci n'est pas la page\n";
}

-> file { '/etc/nginx/sites-available/default':
    ensure => file;
    content => $nginx_config;
}

-> service { 'nginx':
    ensure => running;
}

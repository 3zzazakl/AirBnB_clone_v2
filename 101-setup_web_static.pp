# configure web static

package { 'nginx':
    ensure   => 'installed',
    provider => apt
}

-> file { '/data':
    ensure => 'directory'
}

-> file { '/data/web_static':
    ensure => 'directory'
}

-> file { '/data/web_static/releases':
    ensure => 'directory'
}

-> file { '/data/web_static/current':
    ensure => 'link',
    target => '/data/web_static/releases/test'
}

-> file { '/data/web_static/releases/test':
    ensure => 'directory'
}


-> file { '/data/web_static/releases/test/index.html':
    ensure  => 'present',
    content => "<!DOCTYPE html>
        <html>
            <head> 
            </head>
            <body>
                <p>Nginx server test</p>
            </body>
        </html>"
}

-> file { '/data/web_static/shared':
    ensure => 'directory'
}


-> exec { 'chown_data':
    path        => ['/usr/bin/', '/usr/local/bin', '/bin/'],
    command     => 'chown -R ubuntu:ubuntu /data',
    logoutput   => true,
    refreshonly => true
}

-> file { '/var/www':
    ensure => 'directory'
}

-> file { '/var/www/html':
    ensure => 'directory'
}

-> file { '/var/www/html/index.html':
    ensure  => 'present',
    content => "<!DOCTYPE html>
        <html>
            <head> 
            </head>
            <body>
                <p>Nginx server test</p>
            </body>
        </html>",
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644'
}

exec { 'nginx_config':
    environment =>   ['data=\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n'],
    command     => 'sed -i "39i $data" /etc/nginx/sites-enabled/default',
    path        => '/usr/bin:/usr/sbin:/bin:/usr/local/bin'
}

service { 'nginx':
    ensure    => running,
    subscribe => Exec['nginx_config'],
}

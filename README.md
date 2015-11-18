# layer-nginx
> NGINX layer

# usage

Include `layer:nginx` in your `layer.yaml`

## adding Vhosts

To proxy request through NGINX create a file named `site.toml` with the following:

```toml
"server_name" = "mybouncer.example.com"
"packages" = ["php5-fpm", "php5-mysql"]
"app_path" = "/srv/myapp"
```

Those variables will be available when configuring your `templates/vhost.conf`. The
configuration for a vhost is pretty open depending on your needs.

## events

* **nginx.available** - emitted once nginx is installed and ready
* **website.available** - emitted from the http interface bound to this layer.

Configure your web application once `nginx.available` is emitted:

```python
from nginxlib import configure_site
@when('nginx.available')
def configure_webapp():
    configure_site('mywebsite', 'vhost.conf', app_path='/srv/app')
```

## interface

This layer exposes the [http interface](http://interfaces.juju.solutions/interface/http/)
which can be used in the application layer that consumes this layer.

An example:

```python
@when('nginx.available', 'website.available')
def configure_website(website):
    website.configure(port=config['port'])
```

# license

The MIT License (MIT)

Copyright (c) 2015 Adam Stokes <adam.stokes@ubuntu.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

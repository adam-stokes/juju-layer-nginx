# layer-nginx
> NGINX layer

# usage

Include `layer:nginx` in your `layer.yaml`

## adding Vhosts

To proxy request through NGINX create a file named `sites.toml` with the following:

```toml
[default]
server_name = "mybouncer.example.com"
proxy_pass = "http://127.0.0.1:3000"

[www.joespoolhall.com]
server_name = "email.example.com"
proxy_pass = "http://127.0.0.1:3001"
```

## events

**nginx.available** - emitted once nginx is installed and ready
**nginx.start** - emit to start nginx
**nginx.stop** - emit to stop nginx service
**nginx.restart** - emit to restart nginx

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

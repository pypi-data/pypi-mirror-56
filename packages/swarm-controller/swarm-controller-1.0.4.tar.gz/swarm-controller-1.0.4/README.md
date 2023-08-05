# Swarm Controller

![](https://github.com/jaredvacanti/swarm-controller/workflows/Publish%20to%20PyPI/badge.svg)
![PyPI](https://img.shields.io/pypi/v/swarm-controller?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/swarm-controller?style=flat-square)

This is a simple command line program to manage the bootstrapping 
and maintenance of a Docker Swarm Cluster.

Currently only AWS is supported (requiring access to the 
metadata service). Eventually we will allow other metadata
stores like etcd or Consul.

## Installation

```
pip install swarm-controller
```

## Usage

Bootstrap a node:
```
swarm-ctl bootstrap
```

Cleanup & Maintenance
```
swarm-ctl cleanup
swarm-ctl relabel
```

## Tests

```
poetry run tox
```

## License
 
MIT License

Copyright (c) 2019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

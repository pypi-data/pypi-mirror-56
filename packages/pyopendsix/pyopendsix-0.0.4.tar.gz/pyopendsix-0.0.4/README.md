![](https://ogc.rpglibrary.org/images/c/c8/OpenD6_logo.png)
[![MIT license][mitl-btn]][mitl]
[![Open Game license][ogl-btn]][ogl]
[![PyPI][pypi-btn]][pypi]

# PyOpenD6 
Restful Python API based on [OpenD6][od6].

## License

Resource categories are as follows:

- All source code is licensed the [MIT license][mitl].

- All documentation is licensed under a [Creative Commons License][ccl].

- All OpenD6 content is licensed under the [Open Game License][ogl].

## Installing

### From Source Code

```sh
git clone https://gitlab.com/HexGearInc/pyopendsix.git
cd pyopendsix
```

#### Virtualenv

```sh
virtualenv venv
source venv/bin/activate
python setup.py install
```

#### Docker-compose

```sh
docker-compose build
```

### PyPI

```sh
pip install pyopendsix
```

## Running

### Flask

After installing on the local system,

```sh
python -m pyopendsix
```

### Gunicorn

Running directly from the git repository,

```sh
gunicorn -b0.0.0.0:6000 wsgi:api
```

### Docker

#### Docker Hub

Images can be run directly from Docker Hub,

```sh
docker run hexgearinc/pyopendsix
```

#### Docker-compose

Running directly from the git repository,

```sh
docker-compose up
```

[ccl]: http://creativecommons.org/licenses/by-sa/4.0
[mitl]: https://mit-license.org
[mitl-btn]: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[od6]: https://ogc.rpglibrary.org/index.php?title=OpenD6
[ogl]: http://www.opengamingfoundation.org/ogl.html
[ogl-btn]: https://img.shields.io/badge/license-OGL-green.svg?style=flat-square
[pypi]: https://pypi.python.org/pypi/PyOpenD6
[pypi-btn]: https://img.shields.io/pypi/v/PyOpenD6.svg?style=flat-square

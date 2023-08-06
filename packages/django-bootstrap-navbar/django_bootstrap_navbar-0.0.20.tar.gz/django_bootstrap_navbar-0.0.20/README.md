# django-bootstrap-navbar

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![coverage report](https://gitlab.com/BradleyKirton/django-bootstrap-navbar/badges/master/coverage.svg?job=test)](https://gitlab.com/BradleyKirton/django-bootstrap-navbar/)

A code based navbar with great ambitions.

![django-navbar](./example.png "made with django-bootstrap-navbar and <3")

# Usage

django-bootstrap-navbar lets you create a bootstrap 4 navbar with a Python class. It then takes care of setting the active class on the appropriate link based on the current path.

## Install

The library is available on PyPi.

```bash
pip install django-bootstrap-navbar
```

Once you have created a navbar class there are two ways of making it available in your template context:

1. Using the provided context processor

```python
BOOTSTRAP_NAVBAR = "showcase.navbar:ExampleNavBar"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        ...
            "context_processors": [
                "django.template.context_processors.debug",
                ...
                "bootstrap_navbar.navbars.context_processors.navbar",
            ]
        },
    }
]
```

2. Using the provided mixin
```python
class ContextProcessorView(BootstrapNavBarViewMixin, TemplateView):
    template_name = "index.html"
    navbar_class = AppNavBar
```

Finally the navbar can be rendered within your templates by calling the navbar.render method.

```html
{{ navbar.render }}
```

A full [example](./bootstrap_navbar/examples/) is available within the repo.

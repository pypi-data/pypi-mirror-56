# DNRY-Config

A multi-source configuration library. 

The goal of DNRY-Config is to simplify configuration
loading and overriding.  With DNRY-Config you can 
easily specify several configuration sources and use them
from your application without dealing with the details.

DNRY-Config resolve conflicts and provides namespaced
access to keys to support well organized configuration files.

## Quick Start

Install DNRY-Config

```bash
pip install dnry_config
```

Read a Yaml file in your program.

```python
from dnry.config import ConfigFactory
from dnry.config.yaml import YamlSource

conf = ConfigurationFactory([
    YamlSource("./config1.yaml")
]).build()

config_value = conf.get("app:message")
```

There are many examples in the `samples/` directory.

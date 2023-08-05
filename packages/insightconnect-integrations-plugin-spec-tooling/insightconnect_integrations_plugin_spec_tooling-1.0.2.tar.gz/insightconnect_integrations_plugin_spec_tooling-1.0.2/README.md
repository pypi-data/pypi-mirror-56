
# InsightConnect Integrations Plugin Spec

## What this is

A tool for parsing a
[Rapid7 InsightConnect](https://www.rapid7.com/products/insightconnect/) integration
plugin spec file _(plugin.spec.yaml)_ and interacting with it programmatically.

## Installation

### Install the module via `pip`

```
$ pip install insightconnect-integrations-plugin-spec-tooling
```

## Okay great, but how do I use it

Simple!

```
from typing import Any
from icon_plugin_spec.plugin_spec import KomandPluginSpec, PluginComponent

spec: KomandPluginSpec = KomandPluginSpec(directory="path_to_my_plugin")
raw_connection: {str: Any} = spec.connection()  # Dictionary of connection properties

print(raw_connection)  # Prints out list of inputs on the connection

# or, do the following
connection: PluginComponent = PluginComponent.new_connection(raw=raw_connection)
print(connection.inputs)
```


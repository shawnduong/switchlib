# switchlib

Python library for interacting with Cisco and Brocade network switches\*. Written and documented for the average network engineer.

**This project is currently in BETA and is considered unstable!**

\* More may become available in the future.

## Installation

TODO: *Write installation scripts and index the library on PyPI. The following instructions listed below will not work. Beta developers, use switchlib as you would use a module for now.*

To install switchlib, you will need **Python version 3.9.5 or higher.** This library is not guaranteed to work with older versions of Python. You may install switchlib from the PyPI using the following command:

```
$ pip install switchlib
```

## Supported Devices

This list of devices can be considered incomplete, and is subject to expansion.

In development:
- Brocade ICX 7450

Awaiting development:
- Brocade ICX 7250
- Brocade ICX 7750
- Cisco Catalyst 2960
- Cisco Catalyst 9300
- Cisco Catalyst 9400

## Quick Start Guide

All programs that use switchlib must first import the library. If the library is not installed, see the [installation instructions](#installation). This is typically done towards the beginning of the program during initialization.

```python
import switchlib
```

The switchlib library treats individual switches are discrete objects. To start, instantiate a switch of the desired model. Please refer to the [documentation](#documentation) for a full list of switch classes and their respective constructor arguments.

```python
mySwitch = switchlib.VENDOR_MODEL(ARGS)
```

Initialization during instantiation is not required. This may be useful if instantiating a large quantity of switches at the same time. Initialization can later be done using the `init` method.

```python
mySwitch.init(ARGS)
```

Connection during initialization is not required. This may be useful if instantiating a large quantity of switches at the same time. Connecting to a switch can later be done using the `connect` method.

```python
mySwitch.connect(ARGS)
```

Depending on your use case, you may pass credentials in via function arguments, the command-line interface (secrets non-echoing), or a wordlist file. **It is highly encouraged that you pass credentials via the command-line interface for security reasons. Secrets are securely transmitted using a secure encrypted tunnel (SSH) and are not stored in the object after connecting.**

After connecting, the `connected` attribute of the object will be updated to either `True` or `False`.

```python
print(mySwitch.connected)
```

This connection may be updated by running the `poll_connection` method.

```python
mySwitch.poll_connection(ARGS)
```

For a full list of functionalities, please refer to the [documentation](#documentation).

## Documentation

For comprehensive documentation, please refer to the [wiki](https://github.com/shawnduong/switchlib/wiki).

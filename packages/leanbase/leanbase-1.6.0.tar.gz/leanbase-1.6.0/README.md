# leanbase-python

A client for the [Leanbase](https://leanbase.io/) API in python.

## Usage

```python
import leanbase as lb

lb.configure(api_key='api_key')

lb.await_initialisation(timeout=0.25) # optional

if lb.user(user).can_access('quarter_pounds'):
  # Do this
else:
  # Do that.

lb.user(user).completed('arduous_goal') # optional, recommended.
```

## Architecture

The code and the runtime is divided into the following modules. Storage, Client, Models and API.

Using the client is effectively using the API provided with it. At configuration, 
1. a client and stores are created
1. stores are connected to the client (for auto-updates)
1. the client requests for the first payload and updates the store accordingly.

During usage, 
1. the stores are queried for the feature along with its segments definitions
1. the evaluation algorithm is invoked.
1. the client and stores ensure that the feature definition is always up-to-date
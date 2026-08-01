# shadeDB

<p align="center">
  <img src="https://img.shields.io/pypi/v/shadedb-api?style=flat-square&logo=pypi&logoColor=white" alt="PyPI Version" />
  <img src="https://img.shields.io/pepy/dt/shadedb-api?style=flat-square&label=Downloads" alt="Downloads" />
  <img src="https://img.shields.io/badge/Latency-Millisecond-00c853?style=flat-square&logo=lightning&logoColor=white" alt="Latency" />
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows%20%7C%20Android-5865F2?style=flat-square" alt="Platform" />
  <img src="https://img.shields.io/pypi/l/shadedb-api?style=flat-square" alt="License" />
</p>

<p align="center">
  <strong>The machine-native, semi-structured database built for autonomous agents, real-time pipelines, and sub-millisecond ingestion.</strong>
</p>

<p align="center">
  <a href="https://shadedb-production.up.railway.app"><b>Premium Server</b></a> •
  <a href="mailto:adesolasherifdeen3@gmail.com"><b>Contact / Support</b></a>
</p>

<p align="center">
  <a href="https://facebook.com/harkerbyte"><img src="https://img.shields.io/badge/Facebook-%231877F2.svg?style=flat-square&logo=Facebook&logoColor=white" alt="Facebook"/></a>
  <a href="https://youtube.com/@harkerbyte"><img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=flat-square&logo=YouTube&logoColor=white" alt="YouTube"/></a>
  <a href="https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=flat-square&logo=whatsapp&logoColor=white" alt="WhatsApp"/></a>
  <a href="https://instagram.com/harkerbyte"><img src="https://img.shields.io/badge/Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white" alt="Instagram"/></a>
</p>

---

## Key Pillars

* **Machine-Native** — Designed for AI agents and automated services, removing human-centric query overhead.
*  **Millisecond Execution** — Direct command-dispatch architecture built for extreme performance.
*  **Structured Native Language (SNL)** — An ultra-fast, command-based execution layer that drastically reduces parsing time.
*  **Deterministic Execution** — Predictable latency, sync execution models, and zero unexpected overhead.
*  **Minimal & Composable** — Zero bloat, low allocation footprints, and dead-simple multi-platform setup.

---

##  Quick Links & Navigation

- [Why shadeDB?](#-why-shadedb)
- [What is `shadedb-api`?](#-what-is-shadedb-api)
- [Installation](#-installation)
- [Connecting to a Partition Cluster](#-connecting-to-a-partition-cluster)
- [30-Second Quickstart](#-30-second-quickstart)
- [Basic Usage](#-basic-usage)
- [Structured Native Language (SNL)](#-structured-native-language-snl)
  - [Fetch Operations](#fetch)
  - [Where & Filtering](#where-filtering)
  - [Pagination & Sorting](#pagination--ordering)
  - [Data Lifecycle & Mutexes](#insert--update--lifecycle)
- [CLI Reference](#-cli)
- [Architecture & Error Handling](#-error-handling)
- [Vision](#-vision)

---

##  Why shadeDB?

Traditional databases were built for human queries, complex ORMs, and verbose text parsing. 

**shadeDB flips the script.** Autonomous AI agents, high-frequency execution engines, and real-time event streams don't need pretty syntax — they need **pure velocity, low memory footprints, and deterministic responses**. 

shadeDB uses **Structured Native Language (SNL)** to bypass heavy parsing cycles, yielding near-instant operations across cloud, edge, and embedded runtime environments.

---

##  What is `shadedb-api`?

`shadedb-api` is the official **synchronous subcommunicator** layer interfacing your Python environment directly with remote shadeDB instances.

```text
┌────────────────────────┐      Direct Command Pipeline       ┌────────────────────────┐
│  Application / Agent   │ ─────────────────────────────────> │   shadedb-api Client   │
└────────────────────────┘                                    └────────────────────────┘
                                                                          │
                                                                   Sync Network Shift
                                                                          │
                                                                          ▼
                                                              ┌────────────────────────┐
                                                              │ Remote shadeDB Engine  │
                                                              └────────────────────────┘

```
##  Installation
```bash
pip install shadedb-api

```
##  Connecting to a Partition Cluster

Before using `shadedb-api`, obtain the following credentials from your shadeDB dashboard:

- **Partition Endpoint** – The unique endpoint assigned to your partition.
- **Connection Token** – Authenticates your client.
- **Cluster Token** – Grants access to the target partition cluster.

> **Keep both tokens secret.** Never expose them in public repositories or client-side applications.

### Temporary Connection

To connect without saving the configuration:

```bash
shadedb-api CONNECTION_ENDPOINT CONNECTION_TOKEN CLUSTER_TOKEN
```

Example:

```bash
shadedb-api http://host.com/connect/sdb7f585246acf1480b9caac05f811c3 
8da846a452f13d1d4cf4ddfac656a115 
8c2ff6b8c408f68
```

The connection is valid only for the current session. You'll need to provide the credentials again the next time you connect.

### Persistent Initialization

To save the connection details for future sessions:

```bash
shadedb-api-init CONNECTION_ENDPOINT CONNECTION_TOKEN CLUSTER_TOKEN
```

Example:

```bash
shadedb-api-init http://host.com/connect/sdb7f585246acf1480b9caac05f811c3 
8da846a452f13d1d4cf4ddfac656a115 
8c2ff6b8c408f68
```

This stores the endpoint and authentication tokens locally.

### Reconnecting

After initialization, simply run:

```bash
shadedb-api
```

The client automatically loads the previously saved connection details and opens an interactive session.

##  30-Second Quickstart
```python
from shadedb_api.frame.sync import syncFrame

# Initialize the synchronized DB engine
db = syncFrame(
    endpoint="https://your_database_endpoint",
    connection_token="YOUR_CONNECTION_TOKEN",
    inspection=False,
    query_timeout=0.5
)

```
##  Basic Usage
### Insert Record
```python
result = db.snlComplexQuery(
    command="Insert",
    context={"username": "shade", "age": 12}
)
print(result)

```
### Full Overwrite
```python
result = db.snlComplexQuery(
    command="Overwrite;id::int(1)",
    context={"username": "zeus", "age": 56, "email": "zeus@mail.com"}
)
print(result)

```
### Direct String Query
```python
result = db.snlQuery("Fetch;id::int(1)")
print(result)

```
##  Structured Native Language (SNL)
SNL is shadeDB’s core execution dialect. It reduces syntax parsing to simple instruction.
### Fetch
Retrieve records instantly via indexed fields:
```snl
Fetch;username::sherifdeen

```
Verify field values directly on fetch:
```snl
Fetch;username::sherifdeen;verify(field='value')

```
Select or exclude specific fields:
```snl
Fetch;username::sherifdeen;get(username,role)
Fetch;username::sherifdeen;exclude(password,auth_token)

```
Atomic update on target key:
```snl
Fetch;username::sherifdeen;update(age='int(21)');
Fetch;username::sherifdeen;strict(age='int(21)');

```
### Where (Filtering)
Filter non-unique fields with precision:
```snl
Where;gender::male;get(username,role)
Where;gender::male;exclude(password,auth_token)

```
### Pagination & Ordering
Fine-tune record sets without heavy query wrappers:
 * start X, limit Y — Offset and page limits
 * order(ascend) — Sort ascending
 * order(descend) — Sort descending
 * order(random) — Shuffle returned records
```snl
Where;status::active;start 1, limit 50;order(descend);

```
### Insert / Update / Lifecycle
```snl
# Insert record (JSON payload required)
Insert;jsonString({ "username":"admin", "id":56 });

# Atomic Field Update
Fetch;username::sherifdeen;update(age='int(43)');

# Full Record Overwrite
Overwrite;username::sherifdeen;jsonString({ "username":"shade", "role":"admin" });

```
#### Lifecycle Controls
```snl
Freeze;id::int(17);     # Soft delete (Reversible)
Unfreeze;id::int(17);   # Restore soft-deleted record
Delete;id::int(17);     # Hard delete (Storage reclaimed on compaction)

```
##  Interactive CLI
shadeDB provides a fully functional shell for interactive session management, telemetry, and quick debugging.
```bash
# Initialize persistent configuration
shadedb-api-init [https://your-endpoint.com](https://your-endpoint.com) (connection_token) (cluster_token)

# Launch interactive CLI session
shadedb-api

```
### Session Example
```text

Active


[sdb4e74facf8711447b9e33e6dc83a07] >> fetch;id::int(2)
{'id': 2, 'username': 'sherifdeen'}
[sdb4e74facf8711447b9e33e6dc83a07] >> insert;{"username":"john","age":26,"account_type":"user","disabled":false}
{'account_type': 'user', 'age': 26, 'disabled': False, 'id': 3, 'username': 'john'}
[sdb4e74facf8711447b9e33e6dc83a07] >> fetch;username::john;exclude(account_type);
{'age': 26, 'disabled': False, 'id': 3, 'username': 'john'}
[sdb4e74facf8711447b9e33e6dc83a07] >>*;
[{'id': 1, 'username': 'shade'}, {'id': 2, 'username': 'sherifdeen'}]
[sdb4e74facf8711447b9e33e6dc83a07] >> exit
Exiting shadedb-api Console.

```
##  Error Handling
Catch predictable exceptions safely with built-in error modules:
```python
from shadedb_api.frame.excepts import (
    ShadeDBError,
    URLEndpointMissingError, 
    SNLMissingError, 
    SNLContextMissingError,
    ConnectionTokenMissingError,
    ClusterTokenMissingError
)

try:
    db.snlQuery("fetch;id::int(23)")
except TokenMissingError as e:
    print(f"[shadeDB Security Alert]: Authentication failed -> {e}")
except SNLMissingError as e:
    print(f"[shadeDB Command Error]: Invalid SNL query string -> {e}")

```
##  Vision
> The future of software isn't human-facing dashboards or verbose SQL query builders.
> **The future is machine agents operating, reasoning, and transacting data at lightspeed.**
> 
shadeDB provides the raw execution layer necessary to power that transition.
<p align="center">
<i>Maintained by <a href="https://instagram.com/harkerbyte"><b>Harkerbyte</b></a>.
</p>

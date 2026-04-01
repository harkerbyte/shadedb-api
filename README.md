
> The fastest way to interact with **shadeDB** — a machine-native, semi-structured database built for real-time systems, autonomous agents, and sub-millisecond ingestion.


[shadedb mvp 1](https://web-production-865de.up.railway.app/mvp)
[ shadedb mvp 2 (active)](https://mvp-n2g5.onrender.com/mvp)

<p align="left">
  <strong>🧠 Agent-native</strong><br>
  <strong>📡 Ultra-low latency</strong><br>
  <strong>🧩 Minimal & composable</strong><br>
  <strong>⚙️ Sync execution model</strong><br>
  <strong>🐧 Structured Native Language (SNL)</strong>
</p>

![PyPI - Version](https://img.shields.io/pypi/v/shadedb-api?color=blue&label=PyPI)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/shadedb-api?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=BLUE&left_text=downloads)](https://pepy.tech/projects/shadedb-api)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows%20%7C%20android-lightgrey)
![License](https://img.shields.io/pypi/l/shadedb-api?color=yellow)
<a href = "https://facebook.com/harkerbyte">![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?style=flat&logo=Facebook&logoColor=white)</a>
<a href ="https://youtube.com/@harkerbyte" >![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=flat&logo=YouTube&logoColor=white)</a>
<a href="https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S">![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat&logo=whatsapp&logoColor=white)</a>
<a href="https://instagram.com/harkerbyte" >
![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&amp;logo=instagram&amp;logoColor=white) </a>


---

## Table of contents

- [Why shadeDB?](#why-shadedb)
- [What is `shadedb-api`?](#what-is-shadedb-api)
- [Installation](#installation)
- [30‑Second Quickstart](#30-second-quickstart)
- [Basic Usage](#basic-usage)
  - [Insert](#insert)
  - [Update (Full Overwrite)](#update-full-overwrite)
  - [Query (SNL)](#query-snl)
- [Structured Native Language (SNL)](#structured-native-language-snl)
  - [Fetch](#fetch)
  - [Where (Filtering)](#where-filtering)
  - [Pagination & Ordering](#pagination--ordering)
  - [Insert / Update / Lifecycle](#insert--update--lifecycle)
  - [Unique Fields](#unique-fields)
- [Architecture](#architecture)
- [Module Overview](#module-overview)
- [CLI](#cli)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Performance Philosophy](#performance-philosophy)
- [Use Cases](#use-cases)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Vision](#vision)
---

## Why shadeDB?

Traditional databases were built for **humans**.  
shadeDB is built for **machines**.

Modern systems — AI agents, real-time pipelines, autonomous services — require:
- deterministic execution  
- minimal parsing overhead  
- high-frequency ingestion  
- predictable latency  

shadeDB introduces a **command-based execution model** optimized for speed, not syntax.

---

## What is `shadedb-api`?

`shadedb-api` is a **synchronous subcommunicator** between your application and a remote shadeDB instance.

It is designed to:
- relay commands efficiently  
- minimize transport overhead  
- preserve execution determinism  
- integrate cleanly into production systems  

---

## Installation

```bash
pip install shadedb-api
```

---

## 30‑Second Quickstart

```python
from shadedb_api.frame.sync import syncFrame

db = syncFrame(
    endpoint="https://your-endpoint",
    token="your-db-token",
    inspection=True,
    query_timeout=60
)
```

---

## Usage

Insert

```python
result = db.snlComplexQuery(
    command="insert",
    context={"username": "shade", "age": 12}
)
print(result)
```

Update (Full Overwrite)

```python
result = db.snlComplexQuery(
    command="update :: id :: int(1)",
    context={"username": "zeus", "age": 56, "email": "zeus@mail.com"}
)
print(result)
```

Query (SNL)

```python
result = db.snlQuery("Fetch :: id :: int(1)")
print(result)
```

---

## Structured Native Language (SNL)

SNL is a delimiter-based command language designed for:
- ⚡ Fast parsing
- 🔐 Safer execution
- 🧠 Machine-native interaction

Below are common SNL patterns and examples.

### Fetch

Direct record retrieval via indexed fields.

```snl
Fetch :: username :: sherifdeen
```

Record comparison/verification 
```snl
Fetch :: username :: sherifdeen :: verify :: field :: value
```

Selective fields

```snl
Fetch :: username :: sherifdeen :: get :: username,role
```

Atomic update
```snl 
Fetch :: username :: sherifdeen :: update :: age :: int(21)
```

### Where (Filtering)

Query non-unique fields.

```snl
Where :: gender :: male :: get :: username,role
```

### Pagination & Ordering

Modifiers:

- page(x,y) — slice results from index X to Y
- ascend — sort ascending
- descend — sort descending

Example:

```snl
Where :: status :: active :: page(1,50) :: descend
```

### Insert / Update / Lifecycle

Insert — requires a valid JSON string. No overwrites by default.

```snl
Insert :: jsonString({ "username":"admin", "id":56 })
```

Atomic field update:

```snl
Fetch :: username :: sherifdeen :: update :: age :: int(43)
```

Full record overwrite:

```snl
Update :: username :: sherifdeen :: jsonString({ "username":"shade", "role":"admin" })
```

Data lifecycle commands:

- Fold (soft delete, reversible)

```snl
Fold :: id :: int(17)
```

- Unfold (restore)

```snl
Unfold :: id :: int(17)
```

- Delete (permanent, storage reclaimed during compaction)

```snl
Delete :: id :: int(17)
```
⚠️Note : Fold and unfold are unavailable in mvp version.

### Unique Fields

Default unique keys:

```text
[id, username, email, phone]
```

---

## Architecture

```text
[ Application ]
       │
       ▼
[ shadedb-api (Sync Layer) ]
       │
       ▼
[ Network Transport ]
       │
       ▼
[ Remote shadeDB Instance ]
```

---

## Module Overview

- shadedb_api.frame.sync
  - Core execution engine: synchronous query dispatch, transport coordination, response handling
- shadedb_api.frame.excepts
  - Custom exception system: structured errors, predictable failure modes, debugging clarity

---

## CLI

```bash
# initialize with endpoint and token - saved as default config
shadedb-api-init https://endpoint YOUR_TOKEN

# Re-initialize with endpoint and token - not saved
shadedb-api https://endpoint YOUR_TOKEN

# start an interactive client / CLI with saved config
shadedb-api  

# run snl queries from api cli
[API] $/ fetch :: id :: int(12)

# navigate to console for robust options
[API] $/ console

# navigated to console 
CONSOLE $/ 

# change database name 
CONSOLE $/ name ::mydb
{'database name': 'mydb', 'message': 'database name changed', 'success': True}

# retrieve your database information
mydb $/ info
{'Default pagination': [1, 15], 'Name': 'mydb', 'Total size': '0.000000 / 2.0MB', 'Unique keys': ['id'], 'Use cache': True}

# check your database storage size
mydb $/ stat :: volume
0.000000 / 2.0MB

# check your database unique fields
mydb $/ stat :: unique
[server ~ console]: {'unique keys': ['id']}

# modify your database unique fields
mydb $/ stat ::unique ::username,email,phone number
{'message': "Unique keys updated : ['username', 'email', 'phone number', 'id']", 'success': True}

# modify default page size during filter queries
mydb $/ stat :: page :: 1,30
[server ~ console]: {'message': 'Paged resized'}

# insert to your database from console (snl) 
mydb $/ snl :: insert :: {"username":"shade","email":"test@gmail.com"}
Database latency: 0.0037282

{'email': 'test@gmail.com', 'id': 1, 'username': 'shade'}

# fetch from your database from console (snl
mydb $/ snl :: fetch :: id :: int(1)
Database latency: 0.0008728

{'email': 'test@gmail.com', 'id': 1, 'username': 'shade'}

# update to your database from console (snl)
mydb $/ snl :: update :: id :: int(1) :: {"username":"sherifdeen","email":"test2@gmail.com"}
Database latency: 0.0017347

{'email': 'test2@gmail.com', 'id': 1, 'username': 'sherifdeen'}
# deactivate your database cache system
mydb $/ stat :: cache :: deactivate
{'message': 'cache deactivated', 'success': True}

# activate your database cache system
mydb $/ stat :: cache :: activate
{'message': 'cache activated', 'success': True}

# delete your remote database instance
mydb $/ stat :: terminate
{'message': 'Deleted'}

# close session from console
mydb $/ exit 2
```
---

## Configuration

Example programmatic configuration:

```python
db = syncFrame(
    endpoint="https://your-endpoint",
    token="your-token",
    inspection=True,
    query_timeout=60
)
```

---

## Error Handling

Use the provided exception types to catch and inspect errors:

```python
from shadedb_api.frame.excepts import URLEndpointMissingError, TokenMissingError, SNLMissingError, SNLContextMissingError


try:
    db.snlQuery("fetch :: id :: int(23)")
except TokenMissingError as e:
    print(f"shadeDB error: {e}")
```

---

## Performance Philosophy

Execution speed scales with simplicity. shadeDB removes unnecessary abstraction layers:
- fewer allocations
- faster parsing
- deterministic execution
- increased uptime availability

Result: predictable, ultra-low latency at scale.

---

## Use Cases

- Autonomous AI agents  
- Real-time ingestion pipelines  
- High-frequency event systems  
- Edge data layers  
- Experimental database architectures

---

## Requirements

- Python 3.10+  
- A running shadeDB instance ( remote )

---

## Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feat/your-feature)
3. Make changes, add tests
4. Open a pull request and describe your changes

Please follow the repository's code style and include tests where applicable.

---

## Vision

shadeDB represents a shift from human-centric data systems.  
The future isn’t dashboards. The future is agents thinking and executing at lightning speed.

---
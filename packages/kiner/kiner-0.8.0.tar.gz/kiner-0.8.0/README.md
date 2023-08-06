<p align="center">
    <img width=35% src="https://user-images.githubusercontent.com/1682202/40414884-c84a4248-5e79-11e8-9df4-e7d1da89ed92.png">
</p>

<p align="center">
    <i>A simple Python AWS Kinesis Producer.</i>
</p>

&nbsp;&nbsp;&nbsp;&nbsp; 

[![Build Status](https://travis-ci.org/bufferapp/kiner.svg?branch=master)](https://travis-ci.org/bufferapp/kiner)
[![PyPI version](https://badge.fury.io/py/kiner.svg)](https://badge.fury.io/py/kiner)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)


### Features

- Error handling and retrying with exponential backoff
- Automatic batching and flush callbacks
- Threaded execution

Inspired by the AWS blog post [Implementing Efficient and Reliable Producers with the Amazon Kinesis Producer Library](https://aws.amazon.com/blogs/big-data/implementing-efficient-and-reliable-producers-with-the-amazon-kinesis-producer-library/).

## Installation

You can use `pip` to install Kiner.

```bash
pip install kiner
```

## Usage

To use Kiner, you'll need to have AWS authentication credentials configured
as stated in the [`boto3` documentation](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration)

```python
from kiner.producer import KinesisProducer

p = KinesisProducer('stream-name', batch_size=500, max_retries=5, threads=10)

for i in range(10000):
    p.put_record(i)

p.close()
```

To be notified when data is flushed to AWS Kinesis, provide a flush_callback
```python
from uuid import uuid4
from kiner.producer import KinesisProducer

def on_flush(count, last_flushed_at, Data=b'', PartitionKey='', Metadata=()):
    print(f"""
        Flushed {count} messages at timestamp {last_flushed_at}
        Last message was {Metadata['id']} paritioned by {PartitionKey} ({len(Data)} bytes)
    """)

p = KinesisProducer('stream-name', flush_callback=on_flush)

for i in range(10000):
    p.put_record(i, metadata={'id': uuid4()}, partition_key=f"{i % 2}")

p.close()

```
## Contributions

- Logo design by [@area55git](https://github.com/area55git)

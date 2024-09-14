# Dynamic Multi-level Caching System

## Overview

This project implements a dynamic multi-level caching system in Python 3. The system supports multiple cache levels, each with its own size and eviction policy (Least Recently Used - LRU and Least Frequently Used - LFU). 

## Features

- **Dynamic Cache Levels**: Add or remove cache levels dynamically.
- **Eviction Policies**: Supports LRU and LFU eviction policies.
- **Data Retrieval/Insertion**: Fetches data from higher levels and promotes data to higher caches.
- **Thread Safety**: Utilizes threading locks for safe concurrent access.
- **Display Functionality**: Ability to display the current state of all cache levels.

## Usage

```python
ml_cache = MultiLevelCache()
ml_cache.addCacheLevel(3, "LRU")
ml_cache.addCacheLevel(5, "LFU")

ml_cache.put("key1", "value1")
ml_cache.put("key2", "value2")
ml_cache.put("key3", "value3")
ml_cache.put("key4", "value4")  # This will evict "key1" from LRU

print(ml_cache.get("key2"))  # Should return "value2" and promote it
ml_cache.displayCache()  # Display current state of caches

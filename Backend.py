import threading
from collections import OrderedDict, defaultdict

class Cache:
    def __init__(self, size, eviction_policy):
        self.size = size
        self.eviction_policy = eviction_policy
        self.cache = OrderedDict()
        self.access_count = defaultdict(int)  # For LFU
        self.lock = threading.Lock()  # For thread safety

    def get(self, key):
        with self.lock:
            if key not in self.cache:
                return None
            
            # Promotion of key in LRU
            if self.eviction_policy == "LRU":
                self.cache.move_to_end(key)
            # Increment access count for LFU
            elif self.eviction_policy == "LFU":
                self.access_count[key] += 1
            
            return self.cache[key]

    def put(self, key, value):
        with self.lock:
            if key in self.cache:
                # Update existing value
                self.cache[key] = value
                # Promote in LRU
                if self.eviction_policy == "LRU":
                    self.cache.move_to_end(key)
                # Increment access count for LFU
                elif self.eviction_policy == "LFU":
                    self.access_count[key] += 1
            else:
                # Evict if necessary
                if len(self.cache) >= self.size:
                    self.evict()
                # Insert new value
                self.cache[key] = value
                self.access_count[key] = 1
    
    def evict(self):
        if self.eviction_policy == "LRU":
            self.cache.popitem(last=False)  # Removes the first item
        elif self.eviction_policy == "LFU":
            # Find the least frequently used key
            lfu_key = min(self.access_count, key=self.access_count.get)
            self.cache.pop(lfu_key)
            del self.access_count[lfu_key]

class MultiLevelCache:
    def __init__(self):
        self.caches = []
    
    def addCacheLevel(self, size, evictionPolicy):
        self.caches.append(Cache(size, evictionPolicy))

    def get(self, key):
        for cache in self.caches:
            value = cache.get(key)
            if value is not None:
                # If found, promote to the higher cache levels
                for higher_cache in self.caches[:self.caches.index(cache)]:
                    higher_cache.put(key, value)
                return value
        return None

    def put(self, key, value):
        # Always insert into L1 (the first cache level)
        if self.caches:
            self.caches[0].put(key, value)

    def removeCacheLevel(self, level):
        if 0 <= level < len(self.caches):
            del self.caches[level]

    def displayCache(self):
        for index, cache in enumerate(self.caches):
            print(f"Cache Level {index+1}: {cache.cache}")

# Example Usage
if __name__ == "__main__":
    ml_cache = MultiLevelCache()
    ml_cache.addCacheLevel(3, "LRU")
    ml_cache.addCacheLevel(5, "LFU")

    ml_cache.put("key1", "value1")
    ml_cache.put("key2", "value2")
    ml_cache.put("key3", "value3")
    ml_cache.put("key4", "value4")  # This will evict "key1" from LRU

    print(ml_cache.get("key2"))  # Should return "value2" and promote it
    ml_cache.displayCache()  # Display current state of caches

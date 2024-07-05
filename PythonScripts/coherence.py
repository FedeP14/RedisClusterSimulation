import rediscluster
import redis
import time
import threading

# Variabili globali per tracciare i dati riepilogativi
write_time = 0
records_written = 0
records_read = 0
records_not_found = 0

startup_nodes = [
    {"host": "172.28.0.2", "port": 7001},
    {"host": "172.28.0.3", "port": 7002},
    {"host": "172.28.0.4", "port": 7003}
]

def write_to_redis():
    global write_time, records_written
    # Connessione al cluster Redis
    r = rediscluster.RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    
    start_time = time.time()
    # Scrittura di dati nel cluster
    for x in range(100000):
        key = f'key{x}'
        value = f'value{x}'
        
        if r.set(key, value):
            records_written += 1
    
    write_time = time.time() - start_time

def read_from_redis():
    global records_read, records_not_found
    # Connessione al cluster Redis
    r = rediscluster.RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    
    # Lettura dei dati dal cluster
    for x in range(100000):
        key = f'key{x}'
            
        if r.get(key):
            records_read += 1
        else:
            records_not_found += 1

if __name__ == "__main__":
    # Creazione dei thread per scrittura e lettura
    writer_thread = threading.Thread(target=write_to_redis)
    reader_thread = threading.Thread(target=read_from_redis)
    
    # Avvio del thread di scrittura
    writer_thread.start()
    
    time.sleep(1)
    reader_thread.start()
    
    # Attesa che i thread terminino
    writer_thread.join()
    reader_thread.join()
    
    # Mostra i dati riepilogativi
    print(f"Write time elapsed: {write_time:.2f} seconds")
    print(f"Wrote records: {records_written}")
    print(f"Read records: {records_read}")
    print(f"Records not found: {records_not_found}")
    print(f"Skipped ratio: {records_not_found / records_written:.2f}")
    

import redis
import rediscluster

# Configurazione del cluster Redis
startup_nodes = [
    {"host": "127.0.0.2", "port": "7001"},
    {"host": "127.0.0.3", "port": "7002"},
    {"host": "127.0.0.4", "port": "7003"}
]

# Connessione al cluster Redis
rc = rediscluster.RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# Set per memorizzare le chiavi uniche
unique_keys = set()

# Funzione per ottenere tutte le chiavi e contare quelle uniche
def count_unique_keys():
    for key in rc.scan_iter():
        unique_keys.add(key)
    return len(unique_keys)

# Esegui la funzione e stampa il numero di chiavi uniche
num_unique_keys = count_unique_keys()
print(f"Numero di chiavi uniche: {num_unique_keys}")

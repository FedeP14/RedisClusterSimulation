import redis
import time

def simulate_master_failure(master_ip, master_port):
    try:
        r = redis.StrictRedis(host=master_ip, port=master_port)
        r.execute_command('DEBUG', 'SEGFAULT')
    except redis.exceptions.ConnectionError:
        print(f"Master node at {master_ip}:{master_port} is down.")

def check_cluster_status(any_node_ip, any_node_port):
    r = redis.StrictRedis(host=any_node_ip, port=any_node_port)
    cluster_nodes = r.execute_command('CLUSTER', 'NODES')
    print("\nCluster nodes status:")
    nodes = cluster_nodes.decode('utf-8').split('\n')
    for node in nodes:
        if node:
            if 'master' in node and 'fail' not in node:
                print(f"\nNew master node found: {node}")
            else:
                print(node)
                
                

def check_new_master(new_master_ip, new_master_port):
    r = redis.StrictRedis(host=new_master_ip, port=new_master_port)
    replication_info = r.info('replication')
    print("\nNew master replication info:")
    for key, value in replication_info.items():
        if key not in ['config_epoch', 'master_repl_offset', 'second_repl_offset']:
            print(f"{key}: {value}")

if __name__ == "__main__":
    master_ip = '172.28.0.3'
    master_port = '7002'
    any_node_ip = '172.28.0.2'
    any_node_port = '7001'
    new_master_ip = '172.28.0.7'
    new_master_port = '7006'

    # Simula la caduta di un nodo master
    simulate_master_failure(master_ip, master_port)
    
    # Attendi qualche secondo per permettere al cluster di eseguire il failover
    time.sleep(10)
    
    # Verifica lo stato del cluster
    check_cluster_status(any_node_ip, any_node_port)
    
    # Verifica che una replica sia stata promossa a master
    check_new_master(new_master_ip, new_master_port)

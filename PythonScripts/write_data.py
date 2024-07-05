import rediscluster
from time import sleep, time

def write_from_node1_write_to_node2():
    # Create a Redis Cluster connection
    startup_nodes = [
        {"host": "172.28.0.2", "port": "7001"},
        {"host": "172.28.0.3", "port": "7002"},
        {"host": "172.28.0.4", "port": "7003"}
    ]
    r = rediscluster.RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    # Initialize counters and start time
    num_writes = 0
    start_time = time()

    # Loop to write data to the cluster
    for i in range(2000):
        r.set(f'key{i}', f'value{i}')
        print(f'key{i}: value{i} written to cluster')
        num_writes += 1
        sleep(0.1)

    # Calculate elapsed time
    elapsed_time = time() - start_time - 0.1*num_writes

    # Print summary
    print("\nSummary:")
    print(f"Total number of writes: {num_writes}")
    print(f"Total time taken: {elapsed_time:.2f} seconds")
    print(f"Average time per write: {elapsed_time / num_writes:.2f} seconds")

if __name__ == "__main__":
    write_from_node1_write_to_node2()

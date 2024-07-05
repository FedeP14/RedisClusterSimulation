import subprocess
import time
import redis
'''
 The script creates a Redis cluster with six nodes and one replica per master node.
 The cluster creation command is executed using the redis-cli utility.
 The cluster state is verified by connecting to one of the nodes and checking the cluster info.
'''
def create_cluster():
    create_cluster_cmd = (
        "redis-cli --cluster create "
        "172.28.0.2:7001 172.28.0.3:7002 172.28.0.4:7003 172.28.0.5:7004 172.28.0.6:7005 172.28.0.7:7006 "
        "--cluster-replicas 1"
    )
    subprocess.run(create_cluster_cmd, shell=True, check=True)

def verify_cluster():
    # Connect to one of the nodes in the cluster
    r = redis.Redis(host='172.28.0.2', port=7001)
    cluster_info = r.cluster('info')
    if cluster_info['cluster_state'] == 'ok':
        print("Cluster was created successfully and is in a healthy state!")
    else:
        print("ERR: Cluster is not in a healthy state.")

if __name__ == "__main__":
    create_cluster()
    time.sleep(5)  
    verify_cluster()

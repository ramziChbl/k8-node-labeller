from kubernetes import client, config, watch
import sys, logging

WORKER_NODE_LABEL_BODY = {
            "metadata": {
                "labels": {
                    "node-role.kubernetes.io/worker-node": "",
                    }
            }
        }    

def main():
    logging.basicConfig(level=logging.INFO)

    try:
        # Access the API from inside the pod
        config.load_incluster_config()
    except Exception as e:
        sys.exit('Cannot access cluster config. Exiting')
    

    v1 = client.CoreV1Api()
    w = watch.Watch()

    # Watch for node events, past events like node created before running script are also handled
    for event in w.stream(v1.list_node):
        logging.debug("Event: %s %s %s" % (event['type'], event['object'].kind, event['object'].metadata.name))
        node = event['object']
        if event['type'] == 'ADDED':
            logging.info(f'Patching {node.metadata.name}')
            api_response = v1.patch_node(node.metadata.name, WORKER_NODE_LABEL_BODY)

if __name__ == '__main__':
    main()

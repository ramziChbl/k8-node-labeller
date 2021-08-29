#!/usr/local/bin/python

from kubernetes import client, config, watch
import sys, logging, os


def main():
    logging.basicConfig(level=logging.INFO)

    try:
        # Access the API from inside the pod
        config.load_incluster_config()
    except Exception as e:
        sys.exit('Cannot access cluster config. Exiting')

    # Get labels if defined as en env variable in Dockerfile or pod definition
    nodes_label = os.getenv('NODES_LABEL')
    if nodes_label == '':
        nodes_label = 'worker-node'

    worker_node_label_body = {
        "metadata": {
            "labels": {
                f"node-role.kubernetes.io/{nodes_label}": "",
            }
        }
    }    
    
    v1 = client.CoreV1Api()
    w = watch.Watch()

    # Watch for node events, past events like node created before running script are also handled
    for event in w.stream(v1.list_node):
        logging.debug("Event: %s %s %s" % (event['type'], event['object'].kind, event['object'].metadata.name))
        node = event['object']
        if event['type'] == 'ADDED':
            logging.info(f'Patching {node.metadata.name}')
            api_response = v1.patch_node(node.metadata.name, worker_node_label_body)

if __name__ == '__main__':
    main()

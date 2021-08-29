# k8 Node Labeller


This small application adds a Role to each node joining the cluster (as shown when executing `kubectl get nodes`).

The does so by adding the label `node-role.kubernetes.io/{nodes_label}` to the nodes. The role name can be changed by modifying the pod environment variable `NODES_LABEL`.

For the moment it adds the label to all nodes. That can be solved using different namespaces and assign a different role for each namespace nodes. Or it can be improved if the nodes have a meaningful name where it will be possible to extract the Role.

To deploy it only use : `kubectl apply -f manifest.yaml`
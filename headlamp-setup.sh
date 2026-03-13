helm install my-headlamp headlamp/headlamp --namespace kube-system
helm upgrade --install my-headlamp headlamp/headlamp --namespace kube-system --create-namespace -f config-ai-assistant.yaml
kubectl -n kube-system create serviceaccount headlamp-admin
kubectl create clusterrolebinding headlamp-admin --serviceaccount=kube-system:headlamp-admin --clusterrole=cluster-admin
kubectl create token headlamp-admin -n kube-system
kubectl port-forward -n kube-system service/my-headlamp 8080:80

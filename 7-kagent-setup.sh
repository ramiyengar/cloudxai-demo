kubectl create ns ollama
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: ollama
spec:
  selector:
    matchLabels:
      name: ollama
  template:
    metadata:
      labels:
        name: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - name: http
          containerPort: 11434
---
apiVersion: v1
kind: Service
metadata:
EOF targetPort: 11434
kubectl describe pod -l name=ollama -n ollama
kubectl describe pod -l name=ollama -n ollama
docker pull ollama/ollama:latest
helm install kagent-crds oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds \
  --namespace kagent \
  --create-namespace
helm install kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent \
  --namespace kagent
kubectl apply -f - <<EOF
apiVersion: kagent.dev/v1alpha2
kind: ModelConfig
metadata:
  name: local-llama-config
  namespace: kagent
spec:
  model: llama3.1
  provider: Ollama
  ollama:
    host: http://ollama.ollama.svc.cluster.local:80
EOF

kubectl port-forward svc/kagent-ui -n kagent 8080:8080

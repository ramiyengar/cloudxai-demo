curl -LO https://github.com/k8sgpt-ai/k8sgpt/releases/download/v0.3.40/k8sgpt_amd64.deb
sudo dpkg -i k8sgpt_amd64.deb
k8sgpt
ollama pull llama3.2
k8sgpt auth add --backend ollama --model llama3.2 --baseurl http://localhost:11434
k8sgpt auth default --provider ollama
k8sgpt auth list

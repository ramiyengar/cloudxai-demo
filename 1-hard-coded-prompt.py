import os
from smolagents import tool, CodeAgent, LiteLLMModel
from kubernetes import client, config

# 1. Define the Kubernetes Tool
@tool
def deploy_container(deployment_name: str, image: str, port: int) -> str:
    """
    Deploys a single-replica container to the default namespace in the local Kubernetes cluster.
    
    Args:
        deployment_name: The name of the deployment (e.g., 'nginx-deployment').
        image: The container image to use (e.g., 'nginx:latest').
        port: The container port to expose (e.g., 80).
    """
    try:
        # Load local kubeconfig (~/.kube/config) - works natively with kind/minikube
        config.load_kube_config()
        apps_v1 = client.AppsV1Api()
        
        # Define the container
        container = client.V1Container(
            name=deployment_name,
            image=image,
            ports=[client.V1ContainerPort(container_port=port)]
        )
        
        # Define the pod template
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": deployment_name}),
            spec=client.V1PodSpec(containers=[container])
        )
        
        # Define the deployment spec
        spec = client.V1DeploymentSpec(
            replicas=1,
            template=template,
            selector=client.V1LabelSelector(match_labels={"app": deployment_name})
        )
        
        # Instantiate the deployment object
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name),
            spec=spec
        )
        
        # Create deployment in the default namespace
        apps_v1.create_namespaced_deployment(
            namespace="default",
            body=deployment
        )
        return f"SUCCESS: Created deployment '{deployment_name}' using image '{image}' on port {port}."
        
    except Exception as e:
        return f"ERROR: Failed to deploy container. Details: {str(e)}"

# 2. Configure the Local LLM (Ollama)
# We use LiteLLMModel which acts as a bridge to local Ollama instances.
# The 'ollama_chat/' prefix tells LiteLLM how to route the request.
model = LiteLLMModel(
    model_id="ollama_chat/llama3.1", # Change this if you pulled a different model like qwen2.5-coder
    api_base="http://localhost:11434" # Default Ollama local port
)

# 3. Initialize the Agent
# CodeAgent is Smolagents' flagship agent type that thinks by writing Python code.
agent = CodeAgent(
    tools=[deploy_container],
    model=model,
    add_base_tools=False # Set to True if you want it to also be able to search the web, run arbitrary python, etc.
)

# 4. Run the Agent
if __name__ == "__main__":
    print("🤖 Agent initializing... sending request to Ollama.")
    
    # The prompt we are giving to our agent
    prompt = "Can you deploy an nginx server on the default port in the default namespace?"
    
    # Execute the run
    result = agent.run(prompt)
    
    print("\n--- Final Result ---")
    print(result)

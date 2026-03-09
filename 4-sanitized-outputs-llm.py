import os
import sys
from smolagents import tool, CodeAgent, LiteLLMModel
from kubernetes import client, config

@tool
def deploy_container(deployment_name: str, image: str, port: int) -> str:
    """
    Deploys a single-replica container to the default namespace in the local Kubernetes cluster.
    
    Args:
        deployment_name: The name of the deployment (e.g., 'nginx-deployment').
        image: The container image to use (e.g., 'nginx:latest').
        port: The container port to expose (e.g., 80).
    """
    # --- NEW: Sanitize the LLM's inputs ---
    # Strip any literal single/double quotes or stray spaces, and force lowercase
    image = image.strip("'\" ").lower()
    deployment_name = deployment_name.strip("'\" ").lower()
    
    # Print exactly what the tool is receiving to help with debugging
    print(f"\n[DEBUG] Tool executing -> Name: '{deployment_name}', Image: '{image}', Port: {port}")
    # --------------------------------------

    try:
        # Load local kubeconfig (~/.kube/config)
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
model = LiteLLMModel(
    model_id="ollama_chat/llama3.1", 
    api_base="http://localhost:11434" 
)

# 3. Initialize the Agent
agent = CodeAgent(
    tools=[deploy_container],
    model=model,
    add_base_tools=False 
)

# 4. Run the Agent with STDIN
if __name__ == "__main__":
    # Check if STDIN is interactive or being piped
    if sys.stdin.isatty():
        print("Waiting for input. Type your prompt and press Ctrl+D (or Ctrl+Z on Windows) when finished:")
        
    # Read everything from standard input
    prompt = sys.stdin.read().strip()
    
    # Exit gracefully if no prompt was provided
    if not prompt:
        print("\nERROR: No input provided. Please provide a prompt via STDIN.")
        sys.exit(1)
        
    print(f"\n🤖 Agent initializing... analyzing prompt: '{prompt}'\n")
    
    # Execute the run with the user's provided prompt
    result = agent.run(prompt)
    
    print("\n--- Final Result ---")
    print(result)

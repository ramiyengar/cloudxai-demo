import os
import argparse
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

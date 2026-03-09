from kubernetes import client, config

def deploy_container(deployment_name: str, image: str, port: int) -> str:
    """
    Deploys a container to the local Kubernetes cluster.
    
    Args:
        deployment_name: The name of the deployment (e.g., 'nginx-deployment')
        image: The container image to use (e.g., 'nginx:latest')
        port: The container port to expose.
    """
    try:
        # Load local kubeconfig (e.g., from Minikube or kind)
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
            selector=client.V1LabelSelector(
                match_labels={"app": deployment_name}
            )
        )
        
        # Instantiate the deployment object
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name),
            spec=spec
        )
        
        # Create deployment
        apps_v1.create_namespaced_deployment(
            namespace="default",
            body=deployment
        )
        return f"Successfully created deployment '{deployment_name}' using image '{image}'."
        
    except Exception as e:
        return f"Failed to deploy container. Error: {str(e)}"

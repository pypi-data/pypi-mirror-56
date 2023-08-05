from kubernetes import client, config  # NOQA: E402


def get_api():
    config.load_kube_config()
    return client.CoreV1Api()

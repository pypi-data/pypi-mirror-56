from kubernetes import client, config  # NOQA: E402

# For detailt on specific functions, check:
# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md


def get_api():
    config.load_kube_config()
    return client.CoreV1Api()

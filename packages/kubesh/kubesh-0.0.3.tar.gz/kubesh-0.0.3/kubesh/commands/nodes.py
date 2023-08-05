from collections import OrderedDict
from ..mapper import table_from_list


class Command_Nodes:
    callers = [".nodes", ".n"]
    description = "List the cluster nodes"

    default_fields = OrderedDict(
        {
            "Name": "metadata.name",
            "InternalIP": "status.addresses.[type=InternalIP].address",
            "Hostname": "status.addresses.[type=Hostname].address",
            "Ready": "status.conditions.[reason=KubeletReady].status",
            "Version": "status.node_info.kubelet_version",
        }
    )

    def run(self, console, api):
        response = api.list_node()
        response_data = table_from_list(response, self.default_fields)
        console.table(response_data)
        return "nodes"

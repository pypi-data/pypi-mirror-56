from collections import OrderedDict
from ..mapper import table_from_list, find_item


class Command:
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

    def run(self, console, api, argv):
        if len(argv) == 0:
            response = api.list_node()
            response_data = table_from_list(response, self.default_fields)
            console.table(response_data)
        else:
            node_args = argv[0]
            node_name = node_args
            node_property = None
            if "." in node_args:
                node_name, node_property = node_args.split(".", 1)
            response = api.read_node(node_name)
            try:
                response_data = (
                    response.to_dict()
                    if not node_property
                    else find_item(response, node_property)
                )
            except AttributeError:  # Attribute was not found
                console.error(f"Attributed {node_args} not found")
            else:
                console.print_yaml(response_data)

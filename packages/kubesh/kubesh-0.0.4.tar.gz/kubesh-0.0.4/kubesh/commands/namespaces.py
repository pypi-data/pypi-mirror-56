from collections import OrderedDict
from ..mapper import table_from_list


class Command:
    callers = [".namespaces", ".ns"]
    description = "List namespaces"

    default_fields = OrderedDict({"Name": "metadata.name", "Status": "status.phase"})

    def run(self, console, api, args, kwargs):
        response = api.list_namespace()
        response_data = table_from_list(response, self.default_fields)
        console.table(response_data)
        return "nodes"

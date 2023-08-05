from robot.api import ExecutionResult, ResultVisitor
import requests
import os


class CaseOwnerVistor(ResultVisitor):
    def __init__(self):
        self.owners = {}

    def _get_test_owner(self, test):
        owner = filter(lambda x: 'owner' in x, test.tags)
        if not owner:
            return 'unknown'
        return owner[0].replace("owner-", "")

    def visit_test(self, test):
        self.owners[test.longname] = self._get_test_owner(test)


def remove_file_safely(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def get_case_owner_map(output_xml):
    try:
        if output_xml.startswith("http"):
            resp = requests.get(output_xml)
            remove_file_safely("./output.xml")
            with open("./output.xml", "w") as f:
                f.write(resp.content)
            result = ExecutionResult("./output.xml")
        else:
            result = ExecutionResult(output_xml)
        visitor = CaseOwnerVistor()
        result.visit(visitor)
        remove_file_safely("./output.xml")
        return visitor.owners
    except:
        print("get case owner map from %s meet error" % output_xml)
        return {}

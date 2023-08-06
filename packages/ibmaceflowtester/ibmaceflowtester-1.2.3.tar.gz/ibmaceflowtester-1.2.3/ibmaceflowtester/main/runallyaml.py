import argparse
from ibmaceflowtester.util import io, log
from ibmaceflowtester.classes import mqtest, httptest
import os
import requests
import yaml
import re
import fnmatch

# Define arguments
parser = argparse.ArgumentParser()
parser.add_argument("test_dir", type=str, help="test dir with test-config.yaml and flow sub-dirs")
parser.add_argument("bar_dir", type=str, help="bar file directory from which bar files need to be deployed")
args = parser.parse_args()

test_config = os.path.join(args.test_dir, "test-config.yaml")
suite = yaml.load(io.read_file_string(test_config), Loader=yaml.FullLoader)

log.write_surround_asterisk("PREPARATION")

project_name = suite["project-name"]
ace_connection = suite["connection"]["ACE"]
for (_, _, files) in os.walk(args.bar_dir, topdown=True):
    for bar_file in [bar for bar in files if re.match(fnmatch.translate("*.bar"), bar)]:
        binary = io.read_file_binary(os.path.join(args.bar_dir, bar_file))
        url = f'http://{ace_connection["server-host"]}:{ace_connection["rest-admin-port"]}/apiv2/deploy'
        log.write(f"Deploying {bar_file} to ACE integration server ...{os.linesep}")
        response = requests.post(url, data=binary, headers={'Content-Type': 'application/octet-stream'}, verify=False)

flow_switch = {
    "MQ": mqtest.MQTest,
    "HTTP": httptest.HTTPTest
}

for i in range(len(suite["message-flows"])):
    flow_type = suite["message-flows"][i]["flow-type"]
    flow_switch[flow_type](suite, i, args.test_dir).execute()

log.write_surround_asterisk("CLEANUP")
log.write(f"Deleting project {project_name} from ACE integration server ...{os.linesep}")
url = f'http://{ace_connection["server-host"]}:{ace_connection["rest-admin-port"]}/apiv2/delete?names={project_name}'
response = requests.post(url, headers={'Content-Type': 'application/octet-stream'}, verify=False)

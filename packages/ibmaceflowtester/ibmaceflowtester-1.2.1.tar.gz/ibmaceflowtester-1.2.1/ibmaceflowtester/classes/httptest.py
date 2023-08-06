#!/usr/bin/python
import requests
import os
import re
import fnmatch
import shutil
from ibmaceflowtester.util import diff, file, log

__all__ = ["HTTPTest"]


class HTTPTest:

    def __init__(self, suite, i, test_dir):
        msgflow = suite["message-flows"][i]
        ace_connection = suite["connection"]["ACE"]
        self.flow_name = msgflow["flow-name"]
        self.project_name = suite["project-name"]
        self.base_uri = msgflow["base-uri"]
        self.file_filter = fnmatch.translate(msgflow.get("file-filter", "*"))
        self.use_https = msgflow["use-https"]
        if self.use_https:
            self.app_base = f'https://{ace_connection["server-host"]}:{ace_connection["https-port"]}{self.base_uri}'
        else:
            self.app_base = f'http://{ace_connection["server-host"]}:{ace_connection["http-port"]}{self.base_uri}'
        self.test_dir = test_dir
        self.ace_rest_base = f'http://{ace_connection["server-host"]}:{ace_connection["rest-admin-port"]}/apiv2'
        self.input_config = msgflow["input-config"]

    @staticmethod
    def __query_object_to_string(query_params):
        if len(query_params) == 0:
            return ''
        else:
            return f'?{"&".join([f"{param}={query_params[param]}" for param in query_params])}'

    def __subject_directory_files(self, input_dir, output_dir):
        for (_, _, input_files) in os.walk(input_dir, topdown=True):
            for input_file in [ipf for ipf in input_files if re.match(self.file_filter, ipf)]:
                abs_file = os.path.join(input_dir, input_file)
                headers = {}
                query_string = ''
                for config in self.input_config:
                    if re.match(fnmatch.translate(config["pattern"]), input_file):
                        headers = config.get("headers", {})
                        query_string = self.__query_object_to_string(config.get("query-params", {}))
                        break
                url = f'{self.app_base}{query_string}'
                log.write(f"Making a request to {url} with {input_file} ({str(os.path.getsize(abs_file))} bytes), "
                               f"headers: {headers}")
                request_content = file.read_file_string(abs_file)
                response = requests.post(url, data=bytes(request_content, 'utf-8'), headers=headers, verify=False)
                response_content = response.content.decode('utf-8')
                abs_file = os.path.join(output_dir, input_file)
                file.write_file(abs_file, response_content)
                log.write(f"\tSaved response {input_file} ({str(os.path.getsize(abs_file))} bytes) ...")

    def execute(self):
        log.write_surround_asterisk(self.flow_name)

        requests.packages.urllib3.disable_warnings()
        os.chdir(self.test_dir)

        input_dir = os.path.join(os.getcwd(), self.flow_name, "Input")
        output_dir = os.path.join(os.getcwd(), self.flow_name, "Output")
        output_backup_dir = os.path.join(os.getcwd(), "Output.old")

        # Backup the existing Output folder and create a new Output folder
        if os.path.isdir(output_backup_dir):
            shutil.rmtree(output_backup_dir)
        if os.path.isdir(output_dir):
            shutil.move(output_dir, output_backup_dir)
        os.mkdir(output_dir)

        log.write_underline("Subject files", "=")
        # For each input file in the Input folder, make the http request
        self.__subject_directory_files(input_dir, output_dir)
        log.write("")

        log.write_underline("Test report", "=")
        diff.compare_output_files(output_backup_dir, output_dir)
        shutil.rmtree(output_backup_dir)

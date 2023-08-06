#!/usr/bin/python
import requests
import os
import re
import fnmatch
import shutil
import time
from ibmaceflowtester.util import diff, io, log

__all__ = ["MQTest"]


class MQTest:

    def __init__(self, suite, i, test_dir):
        msgflow = suite["message-flows"][i]
        mq_connection = suite["connection"]["MQ"]
        ace_connection = suite["connection"]["ACE"]
        self.project_name = suite["project-name"]
        self.flow_name = msgflow["flow-name"]
        self.input_queue = msgflow["input-queue"]
        self.output_queues = msgflow["output-queues"]
        self.file_filter = fnmatch.translate(msgflow.get("file-filter", "*"))
        self.test_dir = test_dir
        self.queue_manager = mq_connection["queue-manager-name"]
        self.mq_rest_base = f'http://{mq_connection["host-port"]}/ibmmq/rest/v1'
        self.ace_rest_base = f'http://{ace_connection["server-host"]}:{ace_connection["rest-admin-port"]}/apiv2'
        self.extra_input_folders = []
        self.trailing_flows = []
        for other_mq_flow in [suite["message-flows"][ind] for ind in range(len(suite["message-flows"])) if
                              ind != i and suite["message-flows"][ind]["flow-type"] == "MQ"]:
            if other_mq_flow["input-queue"] in self.output_queues:
                self.trailing_flows += [other_mq_flow["flow-name"]]
            if self.input_queue in other_mq_flow["output-queues"]:
                self.extra_input_folders += [os.path.join(self.test_dir, other_mq_flow["flow-name"], "Output",
                                                          self.input_queue)]

    def __copy_queue_output(self, copy_queue, msgflow):
        src_folder = os.path.join(os.getcwd(), self.flow_name, "Output", copy_queue)
        dst_folder = os.path.join(os.getcwd(), msgflow, "Input")
        io.copy_dir_files(src_folder, dst_folder)

    def __toggle_flow(self, msgflow, toggle):
        url = f'{self.ace_rest_base}/applications/{self.project_name}/messageflows/{msgflow}/{toggle}'
        response = requests.post(url, verify=False)
        if response.status_code != 200:
            raise Exception(f"POST at {url} returned: {os.linesep}{response.content.decode('utf-8')}")

    # Method to save an output file fetched from queue
    def __save_queue_message(self, file, queue, content):
        queue_folder = os.path.join(os.getcwd(), self.flow_name, "Output", queue)
        if not os.path.isdir(queue_folder):
            os.mkdir(queue_folder)
        abs_file = os.path.join(queue_folder, file)
        io.write_file(abs_file, content)
        log.write(f"\tSaved output file from queue {queue}: {file} ({str(os.path.getsize(abs_file))} bytes) ...")

    def __put_file(self, path_to_file, file):
        abs_file = os.path.join(path_to_file, file)
        log.write(f"Putting {file} ({str(os.path.getsize(abs_file))} bytes) to input queue {self.input_queue} ...")
        content = io.read_file_string(abs_file)
        url = f'{self.mq_rest_base}/messaging/qmgr/{self.queue_manager}/queue/{self.input_queue}/message'
        response = requests.post(url, data=bytes(content, 'utf-8'),
                                 headers={'Content-Type': 'text/plain;charset=utf-8',
                                          'ibm-mq-rest-csrf-token': 'blank'}, verify=False)
        if response.status_code != 201:
            raise Exception(f"POST at {url} returned: {os.linesep}{response.content.decode('utf-8')}")

    def __get_messages(self, queue):
        result = []
        url = f'{self.mq_rest_base}/messaging/qmgr/{self.queue_manager}/queue/{queue}/message'
        while True:
            response = requests.delete(url, headers={'Accept': 'text/plain; charset=utf-8',
                                                     'ibm-mq-rest-csrf-token': 'blank'}, verify=False)
            content = response.content.decode('utf-8')
            if response.status_code not in [200, 204]:
                raise Exception(f'DELETE at {url} returned: {os.linesep}{content}')
            if len(content) > 0:
                result.append(content)
            else:
                break
        return result

    def __subject_directory_files(self, file_dir):
        for (_, _, input_files) in os.walk(file_dir, topdown=True):
            for input_file in [ipf for ipf in input_files if re.match(self.file_filter, ipf)]:
                self.__put_file(file_dir, input_file)
                time.sleep(1)
                for output_queue in self.output_queues:
                    output_data = self.__get_messages(output_queue)
                    output_amount = len(output_data)
                    if output_amount == 1:
                        self.__save_queue_message(input_file, output_queue, output_data[0])
                    else:
                        for j in range(output_amount):
                            output_message = output_data[j]
                            self.__save_queue_message(io.add_suffix(input_file, j + 1), output_queue,
                                                      output_message)

    def execute(self):
        log.write_surround_asterisk(self.flow_name)
        requests.packages.urllib3.disable_warnings()
        os.chdir(self.test_dir)

        input_dir = os.path.join(os.getcwd(), self.flow_name, "Input")
        output_dir = os.path.join(os.getcwd(), self.flow_name, "Output")
        output_backup_dir = os.path.join(os.getcwd(), self.flow_name, "Output.old")

        # Backup the existing Output folder and create a new Output folder
        if os.path.isdir(output_backup_dir):
            shutil.rmtree(output_backup_dir)
        if os.path.isdir(output_dir):
            shutil.move(output_dir, output_backup_dir)
        os.mkdir(output_dir)

        # Stop trailing flows
        if len(self.trailing_flows) > 0:
            log.write_underline("Stop trailing ACE flows", "=")
        for msgflow in self.trailing_flows:
            log.write(f"Stopping {msgflow} ...")
            self.__toggle_flow(msgflow, "stop")

        # Empty the output queues
        for queue in self.output_queues:
            discard = self.__get_messages(queue)
        log.write("")

        log.write_underline("Subject files", "=")

        # For each input file in the Input folder and extra input folders, write it to the input queue and get output
        for subject_dir in [input_dir] + self.extra_input_folders:
            self.__subject_directory_files(subject_dir)
        log.write("")

        # Start trailing flows
        if len(self.trailing_flows) > 0:
            log.write_underline("Start trailing ACE flows", "=")
        for msgflow in self.trailing_flows:
            log.write(f"Starting {msgflow} ...")
            self.__toggle_flow(msgflow, "start")
        log.write("")

        log.write_underline("Test report", "=")
        diff.compare_queues(output_backup_dir, output_dir)
        shutil.rmtree(output_backup_dir)

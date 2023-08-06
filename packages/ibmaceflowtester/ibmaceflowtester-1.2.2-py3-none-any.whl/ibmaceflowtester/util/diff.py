import filecmp
import difflib
import os
from ibmaceflowtester.util import log


def compare_queues(left, right):
    compare = filecmp.dircmp(left, right)
    left_only = compare.left_only
    right_only = compare.right_only
    common_dirs = compare.common_dirs

    if len(right_only) > 0:
        log.write(f"The following queues and their associated files have been added to output:{os.linesep}")
        for queue in right_only:
            log.write_underline(queue, "-")
            for file in os.listdir(os.path.join(right, queue)):
                log.write(f"{file}")
            log.write("")

    if len(left_only) > 0:
        log.write(f"The following queues and their associated files have been deleted from output:{os.linesep}")
        for queue in left_only:
            log.write_underline(queue, "-")
            for file in os.listdir(os.path.join(left, queue)):
                log.write(f"{file}")
            log.write("")

    if len(common_dirs) > 0:
        log.write(f"The following queues have the following changes in output:{os.linesep}")
        for queue in common_dirs:
            log.write_underline(queue, "-")
            compare_output_files(os.path.join(left, queue), os.path.join(right, queue))


def compare_output_files(left, right):
    compare = filecmp.dircmp(left, right)
    left_only = compare.left_only
    right_only = compare.right_only
    common_files = compare.common_files

    for file in left_only:
        log.write(f"{file} deleted")

    for file in right_only:
        log.write(f"{file} added")

    for file in common_files:
        left_lines = file.read_file_array(os.path.join(left, file))
        right_lines = file.read_file_array(os.path.join(right, file))
        if os.linesep.join(left_lines) == os.linesep.join(right_lines):
            log.write(f"{file} unchanged")
        else:
            log.write(f"{file} diff")
            unified_diff = difflib.unified_diff(left_lines, right_lines)
            for diff_line in unified_diff:
                strip = diff_line.strip(os.linesep)
                log.write(diff_line.strip(os.linesep))
            log.write("")
    log.write("")


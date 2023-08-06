import os
import sys
import subprocess
import shutil
import yaml
import csv

import logging

logger = logging.getLogger("main_logger")


def create_path(path_name):
    # Create path
    if not os.path.exists(path_name):
        os.makedirs(path_name)

    # Absolute path
    abs_temp_file_dir = os.path.abspath(path_name)
    return abs_temp_file_dir


def delete_path(path_name):
    if os.path.exists(path_name):
        try:
            shutil.rmtree(path_name)
        except:
            logger.debug("Could not delete directory")


def delete_file(file):
    if os.path.exists(file):
        try:
            os.remove(file)
        except:
            logger.debug("Could not delete file")


def load_yaml(stream):
    try:
        return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.error(exc)


def load_file_contents(path, strip=True):
    if not os.path.exists(path):
        logger.error(path + " not found")

    with open(path, "rb") as handle:
        to_return = handle.read().decode("utf-8")

    if strip:
        to_return = to_return.strip()

    return to_return


def run_cmd(cmd, envs=None):
    try:
        my_env = os.environ
        if envs:
            for env in envs:
                my_env[env[0]] = env[1]
        res = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=True,
            env=my_env,
            encoding="ISO-8859-2",
        )
        return res.returncode, res.stdout
    except subprocess.CalledProcessError as error:
        return error.returncode, error.stdout
    except FileNotFoundError as error:
        return 2, error
    except OSError as error:
        return 8, error
    except:
        return -1, sys.exc_info()[0]


def export_csv(rows, filename, delimiter="|"):
    try:
        csv_file = open(filename, "a", encoding="utf-8")
        for row in rows:
            csv_row = ""
            for i in range(len(row)):
                col = row[i]
                if col is None:
                    col = ""
                if col is True:
                    col = 1
                if col is False:
                    col = 0
                if i < len(row) - 1:
                    col = str(col).strip() + delimiter
                else:
                    col = str(col).strip()
                csv_row += col
            # Replace linebreaks if any
            csv_row = csv_row.replace("\n", " ")
            csv_row = csv_row.replace("\r", " ")
            csv_file.write(csv_row + "\n")
        csv_file.close()
        rowcount = len(rows)
        # logger.info(str(rowcount) + " rows added to " + filename)
        return rowcount
    except Exception as e:
        logger.error(e)
        return 0

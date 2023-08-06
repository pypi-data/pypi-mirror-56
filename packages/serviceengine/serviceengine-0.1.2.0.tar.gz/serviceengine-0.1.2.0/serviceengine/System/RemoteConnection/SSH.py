#!/usr/bin/python3
import paramiko


def ConnectAndPerformCommands(hostname, port, username, password, commands, logger):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname=hostname, port=port, username=username, password=password)
        logger.INFO(f"Successfully established ssh connection to {hostname}")
        if commands and len(commands) > 0:
            for command in commands:
                logger.INFO(f"Running command remotely: {command}")
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.read().strip().decode().splitlines()
                responseText = "Command Executed, remote machine response:\n"
                for line in output:
                    responseText = f"{responseText}\n" \
                                   f"       {line}"
                logger.INFO(f"{responseText}\n")
    except Exception as ex:
        logger.ERROR(f"Failed attempting to connect to remote host, exception encountered:\n"
                       f"       {ex}\n")
    finally:
        logger.DEBUG(f"Finished running commands, close connection")
        client.close()
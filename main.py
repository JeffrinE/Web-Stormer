import os
import platform
import toml

with open('pyproject.toml', 'r') as cfg:
    config = toml.load(cfg)
    
if platform.system() == 'Windows':
    log_path = config['path']['WINDOWS_LOG_PATH']
elif platform.system() == 'Linux':
    log_path = config['path']['LINUX_LOG_PATH']
else:
    log_path = config['path']['WINDOWS_LOG_PATH']


def platform_path():
    if platform.system() == 'Windows':
        hosts_path = config['path']['WINDOWS_HOST_PATH']
        redirect = '127.0.0.1'
        return (hosts_path, redirect)
    
    elif platform.system() == 'Linux':
        hosts_path = config['path']['LINUX_HOST_PATH']
        redirect = '127.0.0.1'
        return (hosts_path, redirect)
    
    else:
        print("Unsupported operating system.")
        return "unsupported"


def show_host_log():
    with open(log_path, 'r') as f:
        logs = f.read()
    return logs


def write_to_host_log(url: str):
    with open(log_path, 'a') as f:
        logs = f.write(f"{url}\n")


def block_website(website):
    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    if os.path.exists(hosts_path):
        if is_website_blocked(website):
            print(f'{website} is already blocked.')
            return
        
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(f'\n{redirect} {website}\n')
            write_to_host_log(website)
        print(f'{website} is now blocked.')
    else:
        print(f'Hosts file {hosts_path} not found.')


def unblock_website(website):
    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    if os.path.exists(hosts_path):
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()
        
        with open(hosts_path, 'w') as hosts_file:
            for line in lines:
                if not line.strip().endswith(f' {website}'):
                    hosts_file.write(line)

    if os.path.exists(log_path):

        with open(log_path, 'r') as log_file:
            lines = log_file.readlines()
        
        with open(log_path, 'w') as log_file:
            for line in lines:
                if not line.strip().endswith(f'{website}'):
                    log_file.write(line)

        print(f'{website} is now unblocked.')
    else:
        print(f'Hosts file {hosts_path} not found.')


def is_website_blocked(website):
    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    if os.path.exists(hosts_path):
        with open(hosts_path, 'r') as hosts_file:
            for line in hosts_file:
                if line.strip().endswith(f' {website}'):
                    return True
    return False


def show_blocked():
    host_logs = []

    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    if os.path.exists(hosts_path):
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()
        for line in lines:
            host_logs.append(line)

    return host_logs


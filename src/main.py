import os
import platform
import toml
import datetime
import dbcreator as db

with open('..\\pyproject.toml', 'r') as cfg:
    config = toml.load(cfg)
    
if platform.system() == 'Windows':
    log_path = config['path']['WINDOWS_HOST_PATH']
elif platform.system() == 'Linux':
    log_path = config['path']['LINUX_HOST_PATH']


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


def block_website(row_id: str, website: str):
    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    if is_website_blocked(website):
        print(f'{website} is already blocked.')
        return
    
    with open(hosts_path, 'a') as hosts_file:
        hosts_file.write(f'\n{redirect} {website}\n')
        db.add_to_db(row_id=row_id, url=website, date=datetime.datetime.now().date())
        
    print(f'{website} is now blocked.')
    # else:
    #     print(f'Hosts file {hosts_path} not found.')


def unblock_website(row_id):

    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    if os.path.exists(hosts_path):
        url = db.show_from_id(row_id)[0]
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()
        
        with open(hosts_path, 'w') as hosts_file:
            for line in lines:
                if not line.strip().endswith(f' {url}'):
                    hosts_file.write(line)

    db.remove_from_db(row_id=row_id)
    print(f"{url} is no unblocked")

def is_website_blocked(website):
    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    urls = db.show_blocked()
    for url in urls:
        if website in url[1]:
            return True
        
    return False


def show_blocked():
    logs = []

    paths = platform_path()
    if paths == "unsupported":
        return
    else:
        hosts_path, redirect =  paths 
    
    urls = db.show_blocked()

    return urls


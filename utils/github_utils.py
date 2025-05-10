import os
import shutil
import zipfile
import io
import requests

def download_repo_as_zip(repo_url, temp_folder):
    zip_url = f"{repo_url}/archive/refs/heads/main.zip"
    print(f"Downloading repository from {zip_url}...")
    
    try:
        response = requests.get(zip_url)
        response.raise_for_status()  # Raise an error for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Failed to download repository: {e}")
        raise
    
    print(f"Extracting ZIP file to {temp_folder}...")
    
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(temp_folder)
    except zipfile.BadZipFile as e:
        print(f"Failed to extract ZIP file: {e}")
        raise
    
    print(f"Repository extracted to {temp_folder}.")

def extract_functions_folder(temp_folder, target_folder, repo_temp):
    repo_folder = os.path.join(temp_folder, repo_temp)
    functions_folder = os.path.join(repo_folder, "functions")
    if not os.path.exists(functions_folder):
        raise FileNotFoundError(f"'functions' folder not found in {repo_folder}.")
    if os.path.exists(target_folder):
        print(f"Removing existing target folder: {target_folder}")
        shutil.rmtree(target_folder)
    print(f"Copying 'functions' folder to {target_folder}...")
    os.makedirs(target_folder, exist_ok=True)
    for item in os.listdir(functions_folder):
        source = os.path.join(functions_folder, item)
        destination = os.path.join(target_folder, item)
        if os.path.isdir(source):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)

def load_github(config):
    if config and config.get('use_Git', False):
        print("Pulling repository from GitHub...")
        repo_url = config.get('repo_url', '')
        temp_folder = "repository_contents"
        target_folder = "functions"
        if repo_url:
            try:
                download_repo_as_zip(repo_url, temp_folder)
                extract_functions_folder(temp_folder, target_folder, config['repo_temp'])
            finally:
                if os.path.exists(temp_folder):
                    print(f"Cleaning up temporary folder: {temp_folder}")
                    shutil.rmtree(temp_folder)
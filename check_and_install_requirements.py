import subprocess
import pkg_resources

def install(package):
    subprocess.check_call(["pip", "install", package])

def check_and_install_requirements(requirements_file='requirements.txt'):
    with open(requirements_file, 'r') as file:
        required_packages = file.readlines()

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for requirement in required_packages:
        requirement = requirement.strip()
        if requirement:
            package_name = requirement.split('==')[0]
            if package_name not in installed_packages:
                print(f"Package {requirement} not found. Installing...")
                install(requirement)
            else:
                print(f"Package {requirement} is already installed.")

if __name__ == "__main__":
    check_and_install_requirements()

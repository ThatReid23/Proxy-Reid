import importlib.util
import os
import sys
import subprocess

def check_dependencies():
    """
    Reads requirements.txt and checks if the dependencies are installed.
    """
    print("Checking required packages...")
    missing_packages = []
    try:
        with open('requirements.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Basic parsing of package name
                    package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].split('>')[0].split('<')[0]
                    # The gunicorn package is for linux, so it is not checked
                    if package_name == "gunicorn":
                        print(f"  - {package_name}: Skipped (not for Windows)")
                        continue

                    # Handle cases where import name differs from package name
                    import_name = package_name
                    if package_name == 'beautifulsoup4':
                        import_name = 'bs4'

                    spec = importlib.util.find_spec(import_name)
                    if spec is None:
                        print(f"  - {package_name}: Not Found")
                        missing_packages.append(package_name)
                    else:
                        print(f"  - {package_name}: Found")
    except FileNotFoundError:
        print("Error: requirements.txt not found.")
        return

    if missing_packages:
        print(f"\nFound {len(missing_packages)} missing package(s): {', '.join(missing_packages)}")
        
        # Ask the user if they want to install the packages
        try:
            response = input("Would you like to install the missing packages now? (y/n): ")
        except (EOFError, KeyboardInterrupt):
            # This can happen if the script is run in a non-interactive environment or if the user cancels
            response = 'n'

        if response.lower() == 'y':
            print("Installing missing packages...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])
                print("\nPackages installed successfully.")
                print("You can now run the application by typing: python app.py")
                # We can re-run the check to confirm
                print("\nRe-running check...")
                check_dependencies()
            except subprocess.CalledProcessError as e:
                print(f"\nAn error occurred during installation: {e}")
        else:
            print("\nInstallation skipped. Please install the missing packages manually.")
            print(f"You can use the following command:")
            print(f"pip install {' '.join(missing_packages)}")
    else:
        print("\nAll required packages are installed.")
        print("You can now run the application by typing: python app.py")

if __name__ == "__main__":
    check_dependencies()
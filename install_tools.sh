# This script is used to set up a server environment with necessary dependencies and tools.

# Update the APT package list and install necessary dependencies.
# curl, nginx, git, supervisor, gpg, and sudo are installed.
apt-get update && apt-get install -y curl nginx git gpg gettext

# Install the 1Password CLI.
./external_tools/1password_cli.sh

# Install cloudflared
./external_tools/cloudflared.sh

# Install Python dependencies.
# The Python dependencies are installed from the requirements.txt file.
pip install --no-cache-dir -r requirements.txt


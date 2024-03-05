# This script is used to set up a server environment with necessary dependencies and tools.

# Update the APT package list and install necessary dependencies.
# curl, nginx, git, supervisor, gpg, and sudo are installed.
apt-get update && apt-get install -y curl nginx git supervisor gpg sudo

# Install the 1password CLI.
# The 1password public key is downloaded and added to the system keyring.
# The 1password APT repository is added to the system's APT sources list.
# The 1password policy is downloaded and added to the system's debsig policies.
# The 1password public key is downloaded and added to the system's debsig keyrings.
# The APT package list is updated again and the 1password CLI is installed.
#sudo -s \
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/$(dpkg --print-architecture) stable main" |
tee /etc/apt/sources.list.d/1password.list
mkdir -p /etc/debsig/policies/AC2D62742012EA22/
curl -sS https://downloads.1password.com/linux/debian/debsig/1password.pol | \
tee /etc/debsig/policies/AC2D62742012EA22/1password.pol
mkdir -p /usr/share/debsig/keyrings/AC2D62742012EA22
curl -sS https://downloads.1password.com/linux/keys/1password.asc | \
gpg --dearmor --output /usr/share/debsig/keyrings/AC2D62742012EA22/debsig.gpg
apt update && apt install 1password-cli

# Install Python dependencies.
# The Python dependencies are installed from the requirements.txt file.
pip install --no-cache-dir -r requirements.txt

# Install the cloudflared tunnel.
# The cloudflared package is downloaded from the GitHub releases page.
#check the current architecture and download the appropriate package
if [ $(uname -m) = "x86_64" ]; then
  curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
if [ $(uname -m) = "arm64" ]; then
  curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
# The downloaded package is installed using dpkg.
dpkg -i cloudflared.deb
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')

# Install Redis
print("Installing Redis...")
return_code, stdout, stderr = run_command("sudo yum install redis -y")
print(stdout)
print(stderr)
if return_code != 0:
    print(f"Error installing Redis: {stderr}")
    exit(1)

# Enable and start Redis service
print("Enabling and starting Redis service...")
return_code, stdout, stderr = run_command("sudo systemctl enable redis && sudo systemctl start redis")
print(stdout)
print(stderr)
if return_code != 0:
    print(f"Error enabling and starting Redis service: {stderr}")
    exit(1)


    # Allow the specified port in firewall
return_code, stdout, stderr = run_command("sudo firewall-cmd --permanent --add-port=6379/tcp && sudo firewall-cmd --reload")
print(stdout)
print(stderr)
if return_code != 0:
    print(f"Error enabling and starting Redis service: {stderr}")
    exit(1)
# Install PHP dependencies
print("Installing PHP dependencies...")
return_code, stdout, stderr = run_command("sudo yum install php-pear php-devel -y")
print(stdout)
print(stderr)
if return_code != 0:
    print(f"Error installing PHP dependencies: {stderr}")
    exit(1)

# Install igbinary and redis extensions
print("Installing igbinary and redis extensions...")
return_code, stdout, stderr = run_command("echo 'yes' | pecl install igbinary igbinary-devel redis")
print(stdout)
print(stderr)
if return_code != 0:
    print(f"Error installing igbinary and redis extensions: {stderr}")
    exit(1)

# Update Redis configuration
print("Updating Redis configuration...")
redis_conf_path = "/etc/redis/redis.conf"
with open(redis_conf_path, 'a') as file:
    file.write("\nmaxmemory 256mb\n")
    file.write("maxmemory-policy allkeys-lru\n")
# Update Redis configuration
print("Updating Redis configuration...")
redis_conf_path = "/etc/redis/redis.conf"
with open(redis_conf_path, 'r') as file:
    lines = file.readlines()

updated_lines = []
for line in lines:
    if line.startswith("bind"):
        updated_lines.append("bind 0.0.0.0\n")
    else:
        updated_lines.append(line)

with open(redis_conf_path, 'w') as file:
    file.writelines(updated_lines)

print("Configuration updated successfully.")

return_code, stdout, stderr = run_command("sudo systemctl restart redis")

# Update PHP configuration
print("Updating PHP configuration...")
php_ini_path = "/etc/php.ini"
with open(php_ini_path, 'a') as file:
    file.write("\nextension=igbinary.so\n")
    file.write("extension=redis.so\n")

print("PHP configuration updated successfully.")


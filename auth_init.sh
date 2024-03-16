 #!/bin/sh

echo "Checking if authentication should be setup..."

. ./load_azd_env.sh

if [ -z "$AZURE_USE_AUTHENTICATION" ]; then
  echo "AZURE_USE_AUTHENTICATION is not set, skipping authentication setup."
  exit 0
fi

echo "AZURE_USE_AUTHENTICATION is set, proceeding with authentication setup..."

. ./load_python_env.sh

./.venv/bin/python ./auth_init.py

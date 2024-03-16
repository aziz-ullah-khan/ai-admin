 #!/bin/sh

. ./load_azd_env.sh

if [ -z "$AZURE_USE_AUTHENTICATION" ]; then
  exit 0
fi

. ./load_python_env.sh

./scripts/.venv/bin/python ./auth_update.py --appid "$AUTH_APP_ID" --uri "$BACKEND_URI"

#!/bin/bash
set -e

# 1. Define OpenBao Endpoint
BAO_API="https://openbao.exampledomain.com/v1"

# 2. Authenticate to OpenBao using AppRole
echo "Authenticating to OpenBao..."
LOGIN_RESPONSE=$(curl -sS --request POST \
  --data "{\"role_id\":\"$BAO_ROLE_ID\",\"secret_id\":\"$BAO_SECRET_ID\"}" \
  "$BAO_API/auth/approle/login")

# Extract the temporary client token from the JSON response
BAO_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.auth.client_token')

# 3. Use the temporary token to fetch necessary secrets
BAO_URL="$BAO_API/secretmount/secret"
BAO_RESPONSE=$(curl -sS --request GET \
  --header "X-Vault-Token: $BAO_TOKEN" \
  "$BAO_URL")

# 4. Create secure temporary variables file
TMP_VARS="/tmp/.bao_vars_$$.yml"
touch "$TMP_VARS"
chmod 600 "$TMP_VARS"

# 5. Populate file with OpenBao values
cat <<EOF > "$TMP_VARS"
ansible_user: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.local_priv_user')"
ansible_ssh_pass: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.local_priv_user_cred')"
ansible_become_pass: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.local_priv_user_cred')"
scanner_automation_access_key: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.scanner_automation_access_key')"
scanner_automation_secret: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.scanner_automation_secret')"
local_sat_user: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.local_sat_user')"
local_sat_pass: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.local_sat_pass')"
splunk_hec_token: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.splunk_hec_token')"
splunk_hec_url: "$(echo "$BAO_RESPONSE" | jq -r '.data.data.splunk_hec_url')"
EOF

# 6. Navigate to playbooks directory
cd "$WORKSPACE/playbooks"

# 7. Run playbook with injected OpenBao variables
export ANSIBLE_SSH_CONTROL_PATH_DIR=/tmp/jenkins-ansible-cp
mkdir -p /tmp/jenkins-ansible-cp

# Temporarily disable immediate failure on error
set +e

ansible-playbook -i ../inventories/automation_targets.yml -e @"$TMP_VARS" scanner_patcher.yml
PLAYBOOK_RC=$?

# Re-enable immediate failure on error
set -e

# Handle the exit code. We allow:
# - 0: Pure success
# - 2: Host failed (handled gracefully, report still sent)
# - 3: Failed on unreachable (older Ansible versions)
# - 4: Unreachable host (Ansible 2.x specific)
if [ $PLAYBOOK_RC -eq 0 ] || [ $PLAYBOOK_RC -eq 2 ] || [ $PLAYBOOK_RC -eq 3 ] || [ $PLAYBOOK_RC -eq 4 ]; then
  echo "Ansible playbook execution finished (Exit Code: $PLAYBOOK_RC). Treating as SUCCESS."
else
  echo "Ansible playbook encountered a CRITICAL error (Exit Code: $PLAYBOOK_RC). Failing build."
  rm -f "$TMP_VARS"
  exit $PLAYBOOK_RC
fi

# 8. Clean up
rm -f "$TMP_VARS"

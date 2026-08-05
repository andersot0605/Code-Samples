import json
import sys
import re

def rpm_version_compare(ver_a, ver_b):
    """
    Compares two RPM version strings.
    Returns:
    -1 if ver_a < ver_b
     0 if ver_a == ver_b
     1 if ver_a > ver_b
    """
    def parse_ver(v_str):
        # Split epoch from version-release
        epoch = 0
        if ':' in v_str:
            e, v_str = v_str.split(':', 1)
            epoch = int(e)
        
        # Replace non-alphanumeric characters with spaces to split into components
        # This handles characters like '.', '-', '_' correctly
        parts = re.split(r'[^a-zA-Z0-9]+', v_str)
        
        parsed = []
        for part in parts:
            if part.isdigit():
                parsed.append(int(part))
            else:
                # Keep strings as is for lexicographical comparison
                parsed.append(part)
        return [epoch] + parsed

    a_parts = parse_ver(ver_a)
    b_parts = parse_ver(ver_b)

    # Pad the shorter list with zeros for equal comparison
    max_len = max(len(a_parts), len(b_parts))
    a_parts.extend([0] * (max_len - len(a_parts)))
    b_parts.extend([0] * (max_len - len(b_parts)))

    for i in range(max_len):
        # Standard Python 2/3 compatible type checking for string vs int
        is_a_str = isinstance(a_parts[i], str)
        is_b_str = isinstance(b_parts[i], str)

        if is_a_str and not is_b_str: return 1 # string > int
        if not is_a_str and is_b_str: return -1 # int < string

        if a_parts[i] > b_parts[i]: return 1
        if a_parts[i] < b_parts[i]: return -1

    return 0

def main():
    try:
        ansible_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps([{"error": "Invalid JSON input from Ansible"}]))
        sys.exit(1)

    master_vuln_list = ansible_data.get('master_vuln_list', [])
    sat_lookup = ansible_data.get('sat_lookup', {})
    hostvars = ansible_data.get('hostvars', {})
    reboot_packages_regex = ansible_data.get('reboot_packages_regex', '^()$')
    cv_promoted_hosts = ansible_data.get('cv_promoted_hosts', [])

    grouped_vulns = {}
    for item in master_vuln_list:
        key = f"{item.get('plugin_id', 'Unknown')}-{item.get('fix_version', 'Unknown')}"
        if key not in grouped_vulns:
            grouped_vulns[key] = []
        grouped_vulns[key].append(item)

    final_report_rows = []
    for key, vulns_group in grouped_vulns.items():
        first_vuln = vulns_group[0]
        hosts = sorted(list(set(v.get('host') for v in vulns_group)))
        
        sat_status = sat_lookup.get(first_vuln.get('fix_version'), False)
        reboot_req = "Yes" if re.search(reboot_packages_regex, first_vuln.get('base_pkg', '')) else "No"
        
        upgrade_available_hosts, patched_hosts, needs_rescan_hosts, cv_promoted_for_vuln = [], [], [], []

        for host in hosts:
            host_data = hostvars.get(host, {})
            base_pkg = first_vuln.get('base_pkg', '')
            fix_version_full = first_vuln.get('fix_version', '')
            
            if base_pkg in host_data.get('dnf_upgrades_result', {}).get('stdout', ''):
                upgrade_available_hosts.append(host)
            
            if host_data.get('dnf_update_output', {}).get('changed', False):
                if base_pkg in host_data.get('remediation_targets', []):
                    patched_hosts.append(host)

            installed_packages = host_data.get('dnf_installed_result', {}).get('stdout', '')
            is_already_installed = False
            try:
                search_regex = re.compile(f"^{re.escape(base_pkg)}\\..*\\s+((?:[0-9]+:)?.*)")
                fix_ver_str = re.sub(f'^{re.escape(base_pkg)}-', '', fix_version_full)

                for line in installed_packages.splitlines():
                    match = search_regex.match(line.strip())
                    if match:
                        installed_ver_str = match.group(1).strip().split()[0]
                        if rpm_version_compare(installed_ver_str, fix_ver_str) >= 0:
                            is_already_installed = True
                            break
            except Exception:
                is_already_installed = False

            if is_already_installed and host not in patched_hosts:
                 needs_rescan_hosts.append(host)
            
            if host in cv_promoted_hosts:
                cv_promoted_for_vuln.append(host)

        item_dict = {
            'name': first_vuln.get('vuln_name', 'Unknown'),
            'id': first_vuln.get('plugin_id', 'Unknown'),
            'sev': first_vuln.get('severity', 'Unknown'),
            'first_seen': first_vuln.get('first_seen', 'Unknown'),
            'patch_pub': first_vuln.get('patch_pub', 'Unknown'),
            'aff': first_vuln.get('affected_version', 'Unknown'),
            'fix': first_vuln.get('fix_version', 'Unknown'),
            'sat': 'Yes' if sat_status else 'No',
            'upgrade_available': f"Yes ({len(upgrade_available_hosts)} hosts)" if upgrade_available_hosts else 'No',
            'cv_promoted': f"Yes ({len(cv_promoted_for_vuln)} hosts)" if cv_promoted_for_vuln else 'No',
            'reboot_req': reboot_req,
            'patched': f"Yes ({len(patched_hosts)} hosts)" if patched_hosts else 'No',
            'needs_rescan': f"Yes ({len(needs_rescan_hosts)} hosts)" if needs_rescan_hosts else 'No',
            'acas_hosts': ", ".join(hosts)
        }
        final_report_rows.append(item_dict)
    
    print(json.dumps(final_report_rows))

if __name__ == '__main__':
    main()

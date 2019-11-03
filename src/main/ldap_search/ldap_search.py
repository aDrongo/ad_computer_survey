from ldap3 import Server, Connection, ALL, NTLM


def ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable):
    # Establish connection
    server = Server(server_EnvVariable, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=user_name_EnvVariable, password=user_pass_EnvVariable, authentication=NTLM)
    conn.bind()

    # Search OU
    conn.search(search_base=search_base_EnvVariable, search_filter='(objectclass=computer)', attributes=['cn', 'distinguishedName', 'dNSHostName', 'lastLogon', 'operatingSystem', 'operatingSystemServicePack', 'operatingSystemVersion', 'description', 'lastLogonTimestamp', 'telephoneNumber', 'location'])
    return conn.entries

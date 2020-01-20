from ldap3 import Server, Connection, ALL, NTLM, MODIFY_REPLACE

def search(server_Env, user_name_Env, user_pass_Env, search_base_Env, search_attributes, search_filter):
    # Establish connection
    server = Server(server_Env, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=user_name_Env, password=user_pass_Env, authentication=NTLM)
    conn.bind()
    # Search OU
    conn.search(search_base=search_base_Env, search_filter=search_filter, attributes=search_attributes)
    return conn.entries

def update(server_Env, user_name_Env, user_pass_Env, search_base_Env, search_attributes, search_filter, ldap_attribute, data):
    # Establish connection
    server = Server(server_Env, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=user_name_Env, password=user_pass_Env, authentication=NTLM)
    conn.bind()
    # Search OU for device
    conn.search(search_base=search_base_Env, search_filter=search_filter, attributes=search_attributes)
    # Now modify the found object
    if len(conn.entries) == 0:
        return conn.result
    device = conn.entries[0]
    conn.modify(f'{device.distinguishedname}',{f'{ldap_attribute}': [(MODIFY_REPLACE, [f'{data}'])]})
    return conn.result

def move(server_Env, user_name_Env, user_pass_Env, search_base_Env, search_attributes, search_filter, new_ou):
    # Establish connection
    server = Server(server_Env, use_ssl=True, get_info=ALL)
    conn = Connection(server, user=user_name_Env, password=user_pass_Env, authentication=NTLM)
    conn.bind()
    # Search OU for device
    conn.search(search_base=search_base_Env, search_filter=search_filter, attributes=search_attributes)
    # Now move the found object
    if len(conn.entries) == 0:
        return conn.result
    device = conn.entries[0]
    name = str(device.distinguishedname).split(',')[0]
    conn.modify_dn(f'{device.distinguishedname}',f'{name}', new_superior=f'{new_ou}')
    return conn.result
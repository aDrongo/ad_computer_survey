from ldap_search.ldap_search import ldap_search

server_EnvVariable = "nwmsdc400.internal.northwestmotorsportinc.com"
database_EnvVariable = "database.sqlite"
user_name_EnvVariable = "nwms\\ben.gardner"
user_pass_EnvVariable = "jumPingmotorsport1"
search_base_EnvVariable = 'OU=NWMS Computers,DC=internal,DC=northwestmotorsportinc,DC=com'
search_filter_EnvVariable = 'OU=Retired Computers'



ldap_result = ldap_search(server_EnvVariable, user_name_EnvVariable, user_pass_EnvVariable, search_base_EnvVariable)

for device in ldap_result:
    if not search_filter_EnvVariable in str(device.distinguishedName):
        print(device.distinguishedName)

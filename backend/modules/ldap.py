from ldap3 import Server, Connection, ALL, NTLM
from modules.logger import logging
import modules.config as Config

config = Config.load()

def search(search_name=None):
    """Connect to LDAP with search filter and return Results"""
    logging.debug("Scanning LDAP")
    # Establish connection
    server = Server(config['server'], use_ssl=True, get_info=ALL)
    conn = Connection(server, user=config['user_name'], password=config['user_pass'], authentication=NTLM)
    conn.bind()
    # Search OUs
    if search_name:
        search_filter = f"(&(objectClass=computer)(cn={search_name}))"
    else:
        search_filter = "(objectClass=computer)"
    conn.search(search_base=config['search_base'], search_filter=search_filter, attributes=config['search_attributes'])
    logging.debug(f"found {len(conn.entries)} devices")
    # Filter results
    results = []
    for d in conn.entries:
        if compare(config['search_filter'], d.distinguishedName):
            results.append(d)
    logging.debug(f"Returning {len(results)} devices")
    return results


def compare(filters, data):
    """Return True if data is in filters else return False """
    for f in filters:
        if str(f) not in str(data):
            pass
        else:
            return False
    return True
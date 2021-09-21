import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

LDAP_BASE_DN = "dc=bos,dc=de"
LDAP_USER_DN = "dc=users," + LDAP_BASE_DN
LDAP_LIST_DN = "dc=lists," + LDAP_BASE_DN
LDAP_GROUP_DN = "dc=groups," + LDAP_BASE_DN

EVODATA_IP = "192.168.1.35"

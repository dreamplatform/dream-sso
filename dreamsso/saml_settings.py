
import os
import os.path
import saml2

SAMLDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'djangosaml2')

SAML_CONFIG = {
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',

  # your entity id, usually your subdomain plus the url to the metadata view
  'entityid': 'http://localhost:8001/saml/metadata/',

  # directory with attribute mapping
  'attribute_map_dir': os.path.join(SAMLDIR, 'attributemaps'),

  # this block states what services we provide
  'service': {
      # we are just a lonely SP
      'sp' : {
          'name': 'Dream SSO',
          'endpoints': {
              # url and binding to the assetion consumer service view
              # do not change the binding or service name
              'assertion_consumer_service': [
                  ['http://localhost:8001/saml/acs/',
                   saml2.BINDING_HTTP_POST],
                  ],
              # url and binding to the single logout service view
              # do not change the binding or service name
              'single_logout_service': [
                  ['http://localhost:8001/saml/ls/',
                   saml2.BINDING_HTTP_REDIRECT],
                  ],
              },

           # attributes that this project need to identify a user
          'required_attributes': ['id'],

           # attributes that may be useful to have but not required
          #'optional_attributes': ['eduPersonAffiliation'],

          # in this section the list of IdPs we talk to are defined
          #'idp': ['xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata'],
          },
      },

  # where the remote metadata is stored
  'metadata': {
      'local': [os.path.join(SAMLDIR, 'remote_idp_metadata_test.xml')],
      },

  # set to 1 to output debugging information
  'debug': 1,

  # certificate
  'key_file': os.path.join(SAMLDIR, 'keys', 'private-key.pem'),  # private part
  'cert_file': os.path.join(SAMLDIR, 'keys', 'certificate.pem'),  # public part

  # own metadata settings
  'contact_person': [
      {'given_name': '',
       'sur_name': '',
       'company': 'Haltu Oy',
       'email_address': 'support@haltu.fi',
       'contact_type': 'technical'},
  ],
  # you can set multilanguage information here
  #'organization': {
  #    'name': [('', 'es'), ('', 'en')],
  #    'display_name': [('', 'es'), ('', 'en')],
  #    'url': [('', 'es'), ('', 'en')],
  #    },
  'valid_for': 0,  # how long is our metadata valid
  }

SAML_CREATE_UNKNOWN_USER = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#NOTE IDP-end of the SAML system also uses session
#thus breaking the cookie if same name is used
#this is not needed when the services are operating on different domains
SESSION_COOKIE_NAME = "ssospsessionid"

#NOTE this overrides SAML_CONFIG['valid_for']
SAML_VALID_FOR = 0


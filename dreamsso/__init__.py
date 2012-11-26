
"""
Dream single sign-on
====================

This package provides facilities to services which want to integrate to
Dream system and its user database.

Functionality::

  * SSO
  * Userdb client

It has several Django authentication backends.

One implements direct access to Userdb without any API use. Then
dream-userdb egg has to be installed to the same Django project.

Second implements SSO over SAML. It also overrides Django User
object with one which transparently uses the userdb API.

Installation happens simply by changing the authbackend which is in use.
"""


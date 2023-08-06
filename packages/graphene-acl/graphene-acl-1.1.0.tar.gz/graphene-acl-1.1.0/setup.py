# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['graphene_acl', 'graphene_acl.tests', 'graphene_acl.tests.unit']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=2.1,<3.0']

setup_kwargs = {
    'name': 'graphene-acl',
    'version': '1.1.0',
    'description': 'Graphene Field ACL',
    'long_description': "# graphene-acl\n\nThe motivation for this library is to simplify access control protection for Graphene Fields. A common approach to ACL protection is through the use of a reusable permissions validation decorator. The problem is this is cumbersome for Graphene Fields that use the standard resolver. You are forced to write an unnecessary resolver function just to annotate it with your permissions validator. The second cumbersome problem this library addresses is ACL role based resolvers. Depending on the users role you might want to perform different business logic in order to retrieve the data they requested for a Graphene Field.\n\n## Installation\n\n```bash\n$ pip install graphene-acl\n```\n\n## Usage\n\n### acl_classifier\n\nThe purpose of the classifier is to return a route key that will be used to determine which resolver function is used for resolving the field. The classifier function has access to all the arguments from the field resolver.\n\n### acl_validator\n\nThe purpose of the validator is to authorize access to the field. This validation will occurr before classification routing happens. If authorization validation is different per classification route then you should not use this validator to enforce authorization access. Instead you should authorize at the specific classifier resolver definition.\n\n### Example\n\n```python\nfrom graphene_acl import AclField\nimport graphene\n\ndef classifier(root, info, *args, **kwargs):\n    permissions = info.context.jwt.permissions\n\n    if 'admin' in permissions:\n        return 'admin'\n    if 'perm1' in permissions and not 'perm2' in permissions:\n        return 'perm1'\n    if 'perm2' in permissions and not 'perm1' in permissions:\n        return 'perm2'\n    if 'perm2' in permissions and 'perm1' in permissions:\n        return ['perm1', 'perm2']\n    if 'perm3' in permissions:\n        return 'perm3'\n    if 'perm4' in permissions:\n        return 'perm4'\n    return None\n\ndef has_permissions(permissions):\n    def validator(root, info, *args, **kwars):\n        if (any([permission in info.context.jwt.permissions for permission in permissions])):\n            return True\n        raise AuthorizationError(f'Not authorized to query field {info.field_name}')\n\n    return validator\n\nclass Foo(graphene.ObjectType):\n    # Demonstrates simple routing based on an Admin classifier route key\n    admin_field = AclField(graphene.String, acl_classifier=classifier)\n    restricted_name = AclField(graphene.String, acl_validator=has_permissions(['foo:name:read', 'admin']))\n\n    tenant_field = AclField(graphene.String, acl_classifier=classifier)\n\n@Foo.admin_field.resolve('admin')\ndef resolve_admin_field(root, info, *args, **kwargs):\n    pass\n\n@Foo.admin_field.resolve()\ndef resolve_default_admin_field(root, info):\n    raise Error('Not Authorized')\n\n@Foo.tenant_field.resolve('perm1')\ndef resolve_perm1_field(root, info, *args, **kwargs):\n    pass\n\n@Foo.tenant_field.resolve('perm2')\ndef resolve_perm2_field(root, info, *args, **kwargs):\n    pass\n\n@Foo.tenant_field.resolve(['perm1', 'perm2'])\ndef resolve_perm1_and_perm2_field(root, info, *args, **kwargs):\n    # Uses sorted() + tuple hashing to register function\n    pass\n\n@Foo.tenant_field.resolve('perm3')\n@Foo.tenant_field.resolve('perm4')\ndef resolve_perm3_or_perm4_field(root, info, *args, **kwargs):\n    # Registers function for both 'perm3' and 'perm4' route keys\n    pass\n```\n\nACL Connection Fields\n\n```python\nfrom graphene_django.filter import DjangoFilterConnectionField\nfrom graphene_acl import acl_field_type\n\nBarConnectionField = acl_field_type('BarConnectionField', DjangoFilterConnectionField)\n\nclass Foo(graphene.ObjectType):\n    bar = BarConnectionField(MyNode, acl_permissions=has_permission('FOO'))\n\n```\n\n## Development\n\n### First time setup\n\n-   Install Precommit hooks\n-   `brew install pre-commit && pre-commit install && pre-commit install --install-hooks`\n-   Install poetry: https://github.com/sdispater/poetry#installation\n-   `curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`\n-   Install dependencies\n-   `poetry install`\n",
    'author': 'Nick Harris',
    'author_email': 'nick.harris@cybergrx.com',
    'url': 'https://github.com/CyberGRX/graphene-acl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

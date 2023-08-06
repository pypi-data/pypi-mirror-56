# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='collective.csaml2',
    version='1.2',
    description="SAML2",
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='Plone Python',
    author='Hai Bui',
    author_email='hai.bui@kkday.com',
    url='https://github.com/hai-bui-kkday/collective.saml2',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'dm.saml2 > 2.0.4',
        'dm.zope.saml2 > 2.0b7',
        'PyXB == 1.2.3',
        'dm.xmlsec.binding > 1.1',
        'zope.app.component'
    ],
    extras_require={'test': ['plone.app.testing']},
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)

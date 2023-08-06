# pylint: disable=W0622
"""cubicweb-sioc application packaging information"""

modname = 'sioc'
distname = 'cubicweb-sioc'

numversion = (0, 2, 2)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'Specific views for SIOC (Semantically-Interlinked Online Communities)'
web = 'http://www.cubicweb.org/project/%s' % distname
classifiers = [
           'Framework :: CubicWeb',
           'Programming Language :: Python',
    ]

__depends__ =  {'cubicweb': '>= 3.17.0',
                'six': '>= 1.4.0',}
__recommends__ = {}

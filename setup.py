#from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup

PACKAGE = "buildbotstatus"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Displays Buildbot status for a review",
    author="Andrew Thigpen",
    packages=["buildbotstatus"],
    entry_points={
        'reviewboard.extensions':
            '%s = buildbotstatus.extension:Buildbotstatus' % PACKAGE,
    },
    package_data={
        'buildbotstatus': [
            'templates/buildbotstatus/*.txt',
            'templates/buildbotstatus/*.html',
        ],
    }
)

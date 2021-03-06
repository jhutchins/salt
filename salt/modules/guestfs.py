'''
Interact with virtual machine images via libguestfs

:depends:   - libguestfs
'''

# Import Python libs
import os
import tempfile
import hashlib
import random

# Import Salt libs
import salt.utils

def __virtual__():
    '''
    Only load if libguestfs python bindings are installed
    '''
    if salt.utils.which('guestmount'):
        return 'guestfs'
    return False


def mount(location, access='rw'):
    '''
    Mount an image
    '''
    root = os.path.join(
            tempfile.gettempdir(),
            'guest',
            location.lstrip(os.sep).replace('/', '.')
            )
    if not os.path.isdir(root):
        try:
            os.makedirs(root)
        except OSError:
            # somehow the directory already exists
            pass
    while True:
        if os.listdir(root):
            # Stuf is in there, don't use it
            rand = hashlib.md5(str(random.randint(1, 1000000))).hexdigest()
            root = os.path.join(
                tempfile.gettempdir(),
                'guest',
                location.lstrip(os.sep).replace('/', '.') + rand
                )
        else:
            break
    cmd = 'guestmount -i -a {0} --{1} {2}'.format(location, access, root)
    __salt__['cmd.run'](cmd)
    return root

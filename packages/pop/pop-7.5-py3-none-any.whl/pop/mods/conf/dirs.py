'''
Used to take care of the options that end in `_dir`. The assumption is that
`_dir` options need to be treated differently. They need to verified to exist
and they need to be rooted based on the user, root option etc.
'''
# Import python libs
import os


def roots(hub, default_root, opts, home_root):
    '''
    Detect the root dir data and apply it
    '''
    # TODO: Make this safe for Windows
    os_root = '/'
    root = os_root
    change = False
    anchor = ''
    if hasattr(os, 'geteuid'):
        if not os.geteuid() == 0:
            root = os.path.join(os.environ['HOME'], f'.{home_root}')
            change = True
            anchor = home_root
    if opts.get('root_dir', root) != default_root:
        root = opts.get('root_dir', root)
        change = True
    if not root.endswith(os.sep):
        root = f'{root}{os.sep}'
    if change:
        for key in opts:
            if key == 'root_dir':
                continue
            if key.endswith('_dir'):
                if anchor:
                    if anchor in opts[key]:
                        a_len = len(anchor) + 1
                        opts[key] = f'{os_root}{opts[key][opts[key].index(anchor)+a_len:]}'
                opts[key] = opts[key].replace(
                        os_root, root, 1)


def verify(hub, opts):
    '''
    Verify that the environment and all named directories in the
    configuration exist
    '''
    for key in opts:
        if key == 'root_dir':
            continue
        if key == 'config_dir':
            continue
        if key.endswith('_dir'):
            if not os.path.isdir(opts[key]):
                os.makedirs(opts[key])

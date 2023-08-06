import os
import guang.version as version

def get_version(update=True):
    v= version.version
    v += 1
    if update:
        with open(os.path.join('guang','version.py'),'w') as fo:
            fo.write('version= '+ str(v))
    return '.'.join(list(str(v)))


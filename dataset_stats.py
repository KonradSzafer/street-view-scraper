import glob

if __name__ == '__main__':

    directories = glob.glob('data/**/')
    for path in directories:
        if 'coor' not in path:
            print(path, ' images count: ', end='')
            print(len(glob.glob(path + '/*')))

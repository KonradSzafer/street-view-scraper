import glob

if __name__ == '__main__':

    total_count = 0
    directories = glob.glob('data/**/')
    for path in directories:
        if 'coor' not in path:
            print(path, ' images count: ', end='')
            count = len(glob.glob(path + '/*'))
            print(count)
            total_count += count

    print('Total images count:', total_count)

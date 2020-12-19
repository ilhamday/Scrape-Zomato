import os, glob

def del_file():
    os.chdir('./result_html')

    extension = 'html'

    # for i in file that have html extension
    # put the i in files list
    files = [i for i in glob.glob(f'*.{extension}')]

    for f in files:
        os.remove(f)

# comment for testing the 2nd commit
import os


def parent_dir_of_this_py():
    '''
    Locate the file by the script you running.
    -+-example/
     |
     +-+-basedir/
       |
       +-+-demodir/
         | 
         +-demo.py <- your code is here 


    In your demo.py call parent_dir_of_this_py() return a path:

    '''
    return os.path.abspath(
        os.path.dirname(__file__))


def brother_path_of_this_py(file_name):
    '''
    Locate the file by the script you running.
    -+-example/
     |
     +-+-basedir/
       |
       +-+-demodir/
         | 
         +-demo.py <- your code is here 
         |
         +-cfg.txt


    In your demo.py call brother_path('cfg.txt') return a path.

    '''
    return os.path.join(os.path.abspath(
        os.path.dirname(__file__)), file_name)

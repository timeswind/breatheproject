import argparse
from datetime import datetime
import os.path

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def getDataSystemPath(filename):
    data_folder = os.path.join("results")
    return

def getWriteFilePath(filename, resultpath):
    if (resultpath == "None"):
        return os.path.join(os.getcwd(), filename)
    else:
        return os.path.join(resultpath, filename)
    return

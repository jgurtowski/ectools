
from misc import passFunc


def logger(output_fh):
    
    if not output_fh:
        return passFunc

    def _log(msg):
        '''Logs to output_fh'''
        output_fh.write(msg)
        output_fh.write("\n")
    
    return _log

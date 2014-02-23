

def logger(output_fh):
    
    def dnull(x):
        pass
    
    if not output_fh:
        return dnull

    def _log(msg):
        '''Logs to output_fh'''
        output_fh.write(msg)
        output_fh.write("\n")
    
    return _log

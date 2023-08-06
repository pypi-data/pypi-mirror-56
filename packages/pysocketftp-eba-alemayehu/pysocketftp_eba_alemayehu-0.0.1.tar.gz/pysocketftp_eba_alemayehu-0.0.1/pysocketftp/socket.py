import ctypes, sys, pysocketftp

class Socket: 
    port = 8877
    lib = None 
    
    def __init__(self, port): 
        self.port = port 
        lib_path = pysocketftp.__path__[0] +"/socket_ftp_c/build/libsocket_ftp.so"
        self.lib = ctypes.CDLL(lib_path)
        

    def accept(self): 
        self.lib.receive_file(self.port)

    def send(self, to, file_path): 
        self.lib.send_file(file_path, to)
        print("\n")

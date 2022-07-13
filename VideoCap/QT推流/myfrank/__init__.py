import cv2
import threading

class FFPlayer(threading.Thread):
    '''
    function __init__
        address: URI of the video source, such as 'test.mp4' or 'rtsp://example.com:554/live/channel0'
        callback: the callback function when receiving a frame. Note that it follows 'callback(frame)', and the frame is storaged as opencv_mat format.
        err_handle: the handler function when an error is raised. Note that it follows 'err_handle(exception)'.
    Since it's a thread, you should later use start() to run it and surround it with try catch!
    '''
    def __init__(self, address, callback, err_handle):
        super(FFPlayer,self).__init__()
        self.addr = address
        self.__callback = callback
        self.__errhnd = err_handle
        self.__cancelled = threading.Event()
        self.__cancelled.clear()
    
    def run(self):
        try:
            cap = cv2.VideoCapture(self.addr)
            if not cap.isOpened():
                raise StreamOpenFailedException(self.addr)
            ret, frame = cap.read()
            while ret and not self.__cancelled.isSet():
                self.__callback(frame)
                ret, frame = cap.read()
            cap.release()
        except Exception as e:
            self.__errhnd(e)
    
    '''
    function stop(): send a signal to stop the thread. Note that the thread won't stop immediately!
                    It will stop after the current frame is processed.
    '''
    def stop(self):
        self.__cancelled.set()

class StreamOpenFailedException(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
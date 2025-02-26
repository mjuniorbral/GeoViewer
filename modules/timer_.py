from time import time

if __name__=="__main__":
    from log import log
else:
    from .log import log

class Timer():
    def __init__(self):
        self.time_markers:dict = {}
        self.recent_time_marker = "timer_marker"
        pass
    def set_time_marker(self,name_marker:str=""):
        if name_marker == "":
            name_marker = self.recent_time_marker
        if name_marker in self.time_markers.keys():
            name_marker.rstrip("|")
            for i in range(len(self.time_markers)):
                if f"{name_marker}{'|'*(i+1)}" in self.time_markers.keys():
                    continue
                name_marker = f"{name_marker}{'|'*(i+1)}"
                break
        self.time_markers[name_marker] = time()
        self.recent_time_marker = name_marker
    def get_time_marker(self,name_marker:str=""):
        if name_marker == "":
            name_marker = self.recent_time_marker
        return self.time_markers[name_marker]
    def get_delta_time_from_time_marker(self,name_marker:str="",to_print:bool=True):
        if name_marker == "":
            name_marker = self.recent_time_marker
        if name_marker not in self.time_markers.keys():
            log.error(f"name_marker:{name_marker} não é uma chave de Timer.time_markers")
        delta = time()-self.time_markers[name_marker]
        if to_print:
            log.info(f"Timer: Tempo de execução do marcador '{name_marker}' foi de {delta:.3f}s")
        return delta
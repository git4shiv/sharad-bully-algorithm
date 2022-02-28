
def find_index_of_process(process_list, pid):
    i = 0
    for p in process_list:
        if p.get_process_id() == pid:
            return i
        i = i + 1

class Process:
    def __init__(self, pid, process_list):
        self.pid = pid
        self.process_list = process_list

    def get_process_id(self):
        return self.pid

    def add_new_process_info(self, process):
        self.process_list.append(process)

    def remove_process_info(self, pid):
        process_index = find_index_of_process(self.process_list, pid)
        del self.process_list[process_index]

    def update_process_list(self):
        for p in self.process_list:
            p.add_new_process_info(self)



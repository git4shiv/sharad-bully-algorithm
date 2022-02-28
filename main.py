GENERAL_SIGNAL = "general"
ELECTION_SIGNAL = "election"
PING_SIGNAL = "ping"
RESPONSE_OK = "Ok"


def find_index_of_process(process_list, pid):
    # return the index of the given process id in the processes list. return -1 if not found,
    i = 0
    for p in process_list:
        if p.get_process_id() == pid:
            return i
        i = i + 1
    return -1


def create_distribution_network(process_required_count):
    process_created_count = 0
    last_created_process = False
    while process_created_count < process_required_count:
        process_list = [] if last_created_process == False else last_created_process.get_process_list()
        pid = process_created_count
        last_created_process = Process(pid, process_list)
        process_created_count += 1
    last_created_process.become_coordinator()
    return last_created_process


class Process:
    def __init__(self, pid, process_list):
        self.online = True
        self.is_coordinator = False
        self.coordinator_process_id = False
        self.pid = pid
        self.process_list = process_list
        self.update_process_list()

    def get_process_id(self):
        # get the process id
        return self.pid

    def add_new_process_info(self, process):
        # add new process if not already present in the list
        if find_index_of_process(self.process_list, process.get_process_id()) < 0:
            self.process_list.append(process)

    def remove_process_info(self, pid):
        process_index = find_index_of_process(self.process_list, pid)
        del self.process_list[process_index]

    def update_process_list(self):
        self.process_list.append(self)
        for p in self.process_list:
            if p != self:
                p.add_new_process_info(self)

    def get_process_list(self):
        return self.process_list

    def receive_signal(self, signal_type, from_pid, message):
        if signal_type == GENERAL_SIGNAL:
            print("Receive signal from pid: {} , message: {} ".format(from_pid, message))
            return "received"
        if signal_type == ELECTION_SIGNAL and self.pid > from_pid and self.online == True:
            self.hold_election()
            return RESPONSE_OK
        if signal_type == PING_SIGNAL and self.online == True:
            return RESPONSE_OK
        return False

    def register_coordinator(self, pid):
        self.is_coordinator = self.pid == pid
        self.coordinator_process_id = pid

    def become_coordinator(self):
        self.is_coordinator = True
        for p in self.process_list:
            p.register_coordinator(self.pid)

    def hold_election(self):
        cancel_election = False
        for p in self.process_list:
            if p.get_process_id() > self.pid and cancel_election == False:
                response = self.send_signal(ELECTION_SIGNAL, p.get_process_id(), "")
                if response == RESPONSE_OK:
                    cancel_election = True
        if not cancel_election:
            self.become_coordinator()

    def send_signal(self, signal_type, pid, message):
        process_index = find_index_of_process(self.process_list, pid)
        p = self.process_list[process_index]
        response = p.receive_signal(signal_type, self.pid, message)
        return response

    def ping_coordinator(self):
        response = self.send_signal(PING_SIGNAL, self.coordinator_process_id, "")
        return response


coordinator = create_distribution_network(10)

process3 = coordinator.process_list[3]

# turning coordinator down
coordinator.online = False

if not process3.ping_coordinator():
    process3.hold_election()

coordinator = process3.process_list[process3.coordinator_process_id]
# turning coordinator down again
coordinator.online = False

if not process3.ping_coordinator():
    process3.hold_election()

print(process3.coordinator_process_id)


# coordinator.send_signal("general", 4, "hello world")

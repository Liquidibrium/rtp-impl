import sys
import getopt

import Checksum
import BasicSender

import time


"""
This is a skeleton sender class. Create a fantastic transport protocol here.
"""

MAX_PACKET_SIZE = 1472
PACKET_WINDOW_SIZE = 7
RETRANSMISSION_TIME = 0.5
MAX_TIME_TO_WAIT = 10
SYN_NUMBER = 0


class Sender(BasicSender.BasicSender):
    def __init__(self, dest, port, filename, debug=False, sackMode=False):
        super(Sender, self).__init__(dest, port, filename, debug)
        self.sackMode = sackMode
        self.debug = debug

    # Main sending loop.
    def start(self):
        # add things here
        self.packet_index = SYN_NUMBER  # maybe chosen randomly
        self.packet_end_index = self.packet_index + 1

        self.partition_file()
        if not self.init_connection():
            return

        self.main_sending_loop()
        self.end_connection()

    def check_fast_retransmit(self, index):
        if index > self.packet_index:
            self.packet_index = index
            if self.packet_index > self.packet_end_index:
                return True
            return False
        elif index == self.packet_index:
            self.packets[index][1] += 1
            if self.packets[index][1] >= 3:
                return True
            return False
        return True

    def receive_packets(self):
        while True:
            received_msg = self.receive(RETRANSMISSION_TIME)
            if received_msg:
                if Checksum.validate_checksum(received_msg):
                    splitted_packet = self.split_packet(received_msg)
                    if splitted_packet[0] == "ack":
                        index = int(splitted_packet[1])
                        if self.check_fast_retransmit(index):
                            return
                    elif splitted_packet[0] == "sack":
                        cum_ack, already_received_packets = splitted_packet[1].split(
                            ";"
                        )
                        index = int(cum_ack)
                        if self.check_fast_retransmit(index):
                            return

                        already_received_packets = (
                            already_received_packets.strip().split(",")
                        )
                        for i in already_received_packets:
                            if i == "":
                                break
                            self.packets[int(i)][2] = True
            else:
                return

    def main_sending_loop(self):
        while True:
            if self.packet_index > self.packet_end_index:
                return
            for index in xrange(
                self.packet_index, self.packet_index + PACKET_WINDOW_SIZE
            ):
                if index > self.packet_end_index:
                    break
                if not self.packets[index][2]:
                    self.send(self.packets[index][0])
            self.receive_packets()

    def partition_file(self):
        file_to_send = self.infile.read()
        self.infile.close()
        chunked_packet_number = len(file_to_send) // MAX_PACKET_SIZE
        # {index : [generated packet , number of receives ack after sended, if packet is delivered]}
        self.packets = {}
        index = 0
        for index in xrange(0, chunked_packet_number):
            starting_index = index * MAX_PACKET_SIZE
            packet_to_send = self.make_packet(
                "dat",
                self.packet_end_index + index,
                file_to_send[starting_index : starting_index + MAX_PACKET_SIZE],
            )
            self.packets[self.packet_end_index + index] = [packet_to_send, 0, False]

        self.packet_end_index += index
        packet_to_send = self.make_packet(
            "dat", self.packet_end_index, file_to_send[index * MAX_PACKET_SIZE :]
        )
        self.packets[self.packet_end_index] = [packet_to_send, 0, False]

    def send_one_packet(self, msg_type):
        seconds = time.time()
        msg_to_send = self.make_packet(msg_type, self.packet_index, "")
        while True:
            if seconds + MAX_TIME_TO_WAIT < time.time():
                return False
            self.send(msg_to_send)
            received_msg = self.receive(RETRANSMISSION_TIME)
            if received_msg:
                if Checksum.validate_checksum(received_msg):
                    splitted_packet = self.split_packet(received_msg)
                    next_index = self.packet_index + 1
                    if splitted_packet[0] == "ack":
                        if int(splitted_packet[1]) == next_index:
                            self.packet_index = next_index
                            return True
                    elif splitted_packet[0] == "sack":
                        cum_ack, _ = splitted_packet[1].split(";")
                        if int(cum_ack) == next_index:
                            self.packet_index = next_index
                            return True

    def init_connection(self):
        return self.send_one_packet("syn")

    def end_connection(self):
        self.send_one_packet("fin")


"""
This will be run if you run this script from the command line. You should not
change any of this; the grader may rely on the behavior here to test your
submission.
"""
if __name__ == "__main__":

    def usage():
        print("BEARS-TP Sender")
        print("-f FILE | --file=FILE The file to transfer; if empty reads from STDIN")
        print("-p PORT | --port=PORT The destination port, defaults to 33122")
        print(
            "-a ADDRESS | --address=ADDRESS The receiver address or hostname, defaults to localhost"
        )
        print("-d | --debug Print debug messages")
        print("-h | --help Print this usage message")
        print("-k | --sack Enable selective acknowledgement mode")

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "f:p:a:dk", ["file=", "port=", "address=", "debug=", "sack="]
        )
    except:
        usage()
        exit()

    port = 33122
    dest = "localhost"
    filename = None
    debug = False
    sackMode = False

    for o, a in opts:
        if o in ("-f", "--file="):
            filename = a
        elif o in ("-p", "--port="):
            port = int(a)
        elif o in ("-a", "--address="):
            dest = a
        elif o in ("-d", "--debug="):
            debug = True
        elif o in ("-k", "--sack="):
            sackMode = True

    s = Sender(dest, port, filename, debug, sackMode)
    try:
        s.start()
    except (KeyboardInterrupt, SystemExit):
        exit()

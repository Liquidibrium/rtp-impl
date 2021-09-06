# Assignment-3-RTP

CS 168 Fall 2015
Project 2

In this folder you'll find the sample receiver, code for computing and
validating checksums, as well as example sender code.

Quick! What do I have to write?
===============================
Sender.py is the file in which you will implement your reliable sender. You do
not need to modify any other included files to complete this project. 
Sender.py provides all the scaffolding you need to handle the
command line arguments we will use in the grading of your project.

The Receiver
============
Receiver.py is the sample receiver. The version of Receiver.py here is largely
identical to what we will use for grading your projects (what we actually use
may include additional instrumentation to assist in grading, but should not vary
significantly in functionality). Feel free to modify it, but keep in mind that
we will be testing against our own version of the sender, not yours. 
If bugs are found or changes made to the sample receiver, we'll notify you and
post an updated copy.

BasicSender and Friends
=======================
The BasicSender class in BasicSender.py provides a skeleton upon which to build
your reliable sender. It provides the following methods:

    __init__(self,dest,port,filename,debug=False,sackMode=False): Creates a 
        BasicSender. Specify the destination's hostname, the port at which 
        the receiver is listening, and a filename to transmit. If no filename
        is provided, it will read from STDIN.

    receive(self, timeout): Receive a packet. Waits for a packet before
        returning. Optionally you can specify a maximum timeout to wait for a
        packet. Returns the received packet as a string, or None if receive
        times out.

    send(self,message): Sends message to the receiver specified when you
        created the sender.

    make_packet(self,msg_type,seqno,message): Creates a BEARS-TP packet from
        the specified message type, sequence number, and message. Generates the
        appropriate checksum, and returns the full BEARS-TP packet with
        checksum appended.

    split_packet(self,packet): Given a BEARS-TP packet, splits a packet into a
        tuple of the form (msg_type, seqno, data, checksum). For packets
        without a data field, the data element will be the empty string.

In addition, it defines one method which you must implement:

    start(self): Starts the Sender.



Checksums
=========
Checksum.py includes two functions for validating and generating checksums for
your packets:

    validate_checksum(message): Returns true if the message's checksum matches
        the message, and false otherwise. This function assumes the last field
        of the message the checksum.

    generate_checksum(message): Returns the checksum string for a message. This
        function assumes the message includes the trailing delimiter. The
        checksum is ONLY valid if you simply append this function's result to
        the message you pass in.

Testing
=======
You are expected to write test cases for your own code to ensure compliance
with the project specifications. To assist you, we've given you a simple test
harness (TestHarness.py). The test harness is designed to intercept all packets
sent between your sender and the receiver. It can modify the stream of packets
and check to ensure the stream meets certain conditions. This is very similar
to the grading script that we will use to evaluate your projects.

We have provided three test cases (BasicTest, DropRandomPackets, and 
SackDropRandomPackets) as examples of how to use the test harness. These test 
cases send this README file using the specified sender implementation to the 
specified receiver implementation, either passing all packets through the 
forwarder unmodified or dropping random packets. They both then verify that 
the file received by the receiver matches the input.

To run a test using this test harness, do the following:

    python TestHarness.py -s Sender.py -r Receiver.py

where "YourSender.py" is the path to your sender implementation, "Receiver.py"
is the path to the receiver implementation. Inside TestHarness.py, you need to
modify the function "tests_to_run" at the top of the script to include any test
cases you add.

Passing the basic test cases we provide is a necessary but not sufficient
condition for doing well on this project; there are still many edge cases that
they do not cover. In addition, there are other correctness conditions beyond
simply producing an identical copy of the input file (for instance, you should
not unnecessarily re-transmit data, nor should you re-transmit data that has
already been acknowledged). You should think about what these edge cases might
be and write appropriate test cases to cover them.

Problems and Questions
======================
Direct any problems or questions you have to your recitation section GSI.


#include <iostream>

#include "controller.hh"
#include "timestamp.hh"

using namespace std;

/* Default constructor */
Controller::Controller(const bool debug)
        : debug_(debug), cwnd_(1.0), thresh_(10000.0) {}

/* Get current window size, in datagrams */
unsigned int Controller::window_size() {

    unsigned int window = cwnd_;

    if (debug_) {
        cerr << "At time " << timestamp_ms()
             << " window size is " << window << endl;
    }

    return window;
}

/* A datagram was sent */
void Controller::datagram_was_sent(const uint64_t sequence_number,
        /* of the sent datagram */
                                   const uint64_t send_timestamp,
        /* in milliseconds */
                                   const bool after_timeout
        /* datagram was sent because of a timeout */ ) {
    if (after_timeout) {
        thresh_ = cwnd_ / 2;
        cwnd_ = 1;
    }

    if (debug_) {
        cerr << "At time " << send_timestamp
             << " sent datagram " << sequence_number << " (timeout = " << after_timeout << ")\n";
    }
}

/* An ack was received */
void Controller::ack_received(
        const uint64_t sequence_number_acked, /* what sequence number was acknowledged */
        const uint64_t send_timestamp_acked, /* when the acknowledged datagram was sent (sender's clock) */
        const uint64_t recv_timestamp_acked, /* when the acknowledged datagram was received (receiver's clock)*/
        const uint64_t timestamp_ack_received)/* when the ack was received (by sender) */
{
    uint64_t diff = timestamp_ack_received - send_timestamp_acked;
    if (diff > timeout_ms()) {
        thresh_ = cwnd_ / 2;
        cwnd_ = 1;
    }

    if (cwnd_ < thresh_) {
        cwnd_++;
    } else {
        cwnd_ += 1.0 / cwnd_;
    }

    if (debug_) {
        cerr << "At time " << timestamp_ack_received
             << " received ack for datagram " << sequence_number_acked
             << " (send @ time " << send_timestamp_acked
             << ", received @ time " << recv_timestamp_acked << " by receiver's clock)"
             << endl;
    }
}

/* How long to wait (in milliseconds) if there are no acks
   before sending one more datagram */
unsigned int Controller::timeout_ms() {
    return 100; /* timeout of one second */
}

#!/usr/bin/env python
"""
Queue Configuration test case.
Similar to test_queue_config in the Perl OpenFlow-1.0 testsuite.

"""

import logging
import unittest
import random

import oftest.controller as controller
import oftest.cstruct as ofp
import oftest.message as message
import oftest.dataplane as dataplane
import oftest.action as action
import oftest.parse as parse
import basic
from pktact import BaseMatchCase, supported_actions_get

from testutils import *
from time import sleep

#@var port_map Local copy of the configuration map from OF port
# numbers to OS interfaces
pa_port_map = None
#@var pa_logger Local logger object
pa_logger = None
#@var pa_config Local copy of global configuration data
pa_config = None

# a random queue_id
QUEUE_ID = 0

def test_set_init(config):
    """
    Set up function for packet action test classes

    @param config The configuration dictionary; see oft
    """

    global pa_port_map
    global pa_logger
    global pa_config

    pa_logger = logging.getLogger("pkt_act")
    pa_logger.info("Initializing test set")
    pa_port_map = config["port_map"]
    pa_config = config

class QueueForward(BaseMatchCase):
    """
    Forward packet to a specific queue.
    """
    def runTest(self):
        queue_id = QUEUE_ID
        #sup_acts = supported_actions_get(self)
        #if not (sup_acts & 1<<ofp.OFPAT_SET_QUEUE):
            #skip_message_emit(self, "Forward to queue test")
            #return

        pkt = simple_tcp_packet()
        queue_act = action.action_set_queue()
        queue_act.queue_id = queue_id
        flow_match_test(self, pa_port_map, pkt=pkt, apply_action_list = [queue_act])

class QueueConfig(basic.SimpleDataPlane):
    """
    Verify queue configuration messages are properly reported.
    """
    def runTest(self):
        of_ports = pa_port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 1, "Not enough ports for test")
        
        request = message.queue_get_config_request()
        request.port = of_ports[0]
        pa_logger.info("Querying switch for queue configuration")
        ofmsg_send(self, request)

        (response, raw) = self.controller.poll(ofp.OFPT_QUEUE_GET_CONFIG_REPLY, 2)

        self.assertTrue(response is not None, 'Did not receive queue config reply')

'''
class QueueStats(basic.SimpleDataPlane):
    """
    Verify that queue statistics are properly updated and reported.
    """
    def runTest(self):
        queue_id = QUEUE_ID
        #sup_acts = supported_actions_get(self)
        #if not (sup_acts & 1<<ofp.OFPAT_SET_QUEUE):
            #skip_message_emit(self, "Forward to queue test")
            #return
        of_ports = pa_port_map.keys()
        of_ports.sort()
        self.assertTrue(len(of_ports) > 2, "Not enough ports for test")

        pkt = simple_tcp_packet()
        queue_act = action.action_set_queue()
        queue_act.queue_id = queue_id
        flow_match_test_port_pair(parent=self, ing_port=of_ports[0], egr_port=of_ports[1], pkt=pkt, exp_pkt=pkt, apply_action_list = [queue_act])


        stat_req = message.queue_stats_request()
        stat_req.port_no = ofp.OFPP_ANY
        stat_req.queue_id = ofp.OFPQ_ALL

        pa_logger.info("Sending stats request")
        do_barrier(self.controller)
        (response, raw) = self.controller.transact(stat_req)
        self.assertTrue(response,"Got no queue stats reply")
        self.assertTrue(len(response.stats)==0,
                         "Expected stats reply")
        #queue_stats = response.stats[0]
        #self.assertTrue(queue_stats.tx_bytes == 0,"Queue Stats Incorrect")
'''

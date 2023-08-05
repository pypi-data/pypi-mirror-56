# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from spinn_utilities.progress_bar import ProgressBar
from spinn_utilities.log import FormatAdapter
from spinn_front_end_common.utilities.utility_objs import ProvenanceDataItem

logger = FormatAdapter(logging.getLogger(__name__))


class RouterProvenanceGatherer(object):
    """ Gathers diagnostics from the routers.
    """

    __slots__ = [
        # int for how many packets were sent
        '_total_sent_packets',

        # how many new packets were received
        '_total_new_packets',

        # how many dropped packets
        '_total_dropped_packets',

        # total missed dropped packets
        '_total_missed_dropped_packets',

        # total lost dropped packets
        '_total_lost_dropped_packets',

        # machine
        '_machine',
        # placements
        '_placements',
        # transceiver
        '_txrx',
    ]

    def __call__(
            self, transceiver, machine, router_tables,
            extra_monitor_vertices=None, placements=None):
        """
        :param transceiver: the SpiNNMan interface object
        :type transceiver: ~spinnman.transceiver.Transceiver
        :param machine: the SpiNNaker machine
        :type machine: ~spinn_machine.Machine
        :param router_tables: the router tables that have been generated
        :param has_ran: token that states that the simulation has ran
        :param provenance_data_objects: other provenance data items
        :param extra_monitor_vertices: \
            vertices which represent the extra monitor code
        :param placements: the placements object
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=attribute-defined-outside-init
        self._total_sent_packets = 0
        self._total_new_packets = 0
        self._total_dropped_packets = 0
        self._total_missed_dropped_packets = 0
        self._total_lost_dropped_packets = 0
        self._txrx = transceiver
        self._machine = machine
        self._placements = placements

        prov_items = list()

        prov_items.extend(self._write_router_provenance_data(
            router_tables, extra_monitor_vertices))

        prov_items.append(ProvenanceDataItem(
            ["router_provenance", "total_multi_cast_sent_packets"],
            self._total_sent_packets))
        prov_items.append(ProvenanceDataItem(
            ["router_provenance", "total_created_packets"],
            self._total_new_packets))
        prov_items.append(ProvenanceDataItem(
            ["router_provenance", "total_dropped_packets"],
            self._total_dropped_packets))
        prov_items.append(ProvenanceDataItem(
            ["router_provenance", "total_missed_dropped_packets"],
            self._total_missed_dropped_packets))
        prov_items.append(ProvenanceDataItem(
            ["router_provenance", "total_lost_dropped_packets"],
            self._total_lost_dropped_packets))

        return prov_items

    def _write_router_provenance_data(
            self, router_tables, extra_monitor_vertices):
        """ Writes the provenance data of the router diagnostics

        :param router_tables: the routing tables generated by PACMAN
        :param extra_monitor_vertices: list of extra monitor vertices
        """
        # pylint: disable=too-many-arguments
        progress = ProgressBar(self._machine.n_chips*2,
                               "Getting Router Provenance")

        # acquire diagnostic data
        items = list()
        seen_chips = set()

        # get all extra monitor core data if it exists
        reinjection_data = None
        if extra_monitor_vertices is not None:
            monitor = extra_monitor_vertices[0]
            reinjection_data = monitor.get_reinjection_status_for_vertices(
                placements=self._placements,
                extra_monitor_cores_for_data=extra_monitor_vertices,
                transceiver=self._txrx)

        for router_table in progress.over(sorted(
                router_tables.routing_tables,
                key=lambda table: (table.x, table.y)), False):
            self._write_router_table_diagnostic(
                router_table.x, router_table.y, seen_chips,
                router_table, items, reinjection_data)

        for chip in progress.over(sorted(
                self._machine.chips, key=lambda c: (c.x, c.y))):
            self._write_router_chip_diagnostic(
                chip, seen_chips, items, reinjection_data)
        return items

    def _write_router_table_diagnostic(
            self, x, y, seen_chips, router_table, items, reinjection_data):
        # pylint: disable=too-many-arguments, bare-except
        if not self._machine.get_chip_at(x, y).virtual:
            try:
                router_diagnostic = self._txrx.get_router_diagnostics(x, y)
                seen_chips.add((x, y))
                reinjection_status = None
                if reinjection_data is not None:
                    reinjection_status = reinjection_data[(x, y)]
                items.extend(self._write_router_diagnostics(
                    x, y, router_diagnostic, reinjection_status, True,
                    router_table))
                self._add_totals(router_diagnostic, reinjection_status)
            except:  # noqa: E722
                logger.warning(
                    "Could not read routing diagnostics from {}, {}",
                    x, y, exc_info=True)

    def _write_router_chip_diagnostic(
            self, chip, seen_chips, items, reinjection_data):
        # pylint: disable=too-many-arguments, bare-except
        if not chip.virtual and (chip.x, chip.y) not in seen_chips:
            try:
                diagnostic = self._txrx.get_router_diagnostics(chip.x, chip.y)

                if (diagnostic.n_dropped_multicast_packets or
                        diagnostic.n_local_multicast_packets or
                        diagnostic.n_external_multicast_packets):
                    reinjection_status = None
                    if reinjection_data is not None:
                        reinjection_status = reinjection_data[chip.x, chip.y]
                    items.extend(self._write_router_diagnostics(
                            chip.x, chip.y, diagnostic, reinjection_status,
                            False, None))
                    self._add_totals(diagnostic, reinjection_status)
            except:  # noqa: E722
                # There could be issues with unused chips - don't worry!
                pass

    def _add_totals(self, router_diagnostic, reinjection_status):
        self._total_sent_packets += (
            router_diagnostic.n_local_multicast_packets +
            router_diagnostic.n_external_multicast_packets)
        self._total_new_packets += router_diagnostic.n_local_multicast_packets
        self._total_dropped_packets += (
            router_diagnostic.n_dropped_multicast_packets)
        if reinjection_status is not None:
            self._total_missed_dropped_packets += (
                reinjection_status.n_missed_dropped_packets)
            self._total_lost_dropped_packets += (
                reinjection_status.n_dropped_packet_overflows)
        else:
            self._total_lost_dropped_packets += (
                router_diagnostic.n_dropped_multicast_packets)

    @staticmethod
    def _add_name(names, name):
        new_names = list(names)
        new_names.append(name)
        return new_names

    def _write_router_diagnostics(
            self, x, y, router_diagnostic, reinjection_status, expected,
            router_table):
        """ Stores router diagnostics as a set of provenance data items

        :param x: x coordinate of the router in question
        :param y: y coordinate of the router in question
        :param router_diagnostic: the router diagnostic object
        :param reinjection_status: \
            the data gained from the extra monitor re-injection subsystem
        :param router_table: the router table generated by the PACMAN tools
        """
        # pylint: disable=too-many-arguments
        names = list()
        names.append("router_provenance")
        if expected:
            names.append("expected_routers")
        else:
            names.append("unexpected_routers")
        names.append("router_at_chip_{}_{}".format(x, y))

        items = list()

        items.append(ProvenanceDataItem(
            self._add_name(names, "Local_Multicast_Packets"),
            str(router_diagnostic.n_local_multicast_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "External_Multicast_Packets"),
            str(router_diagnostic.n_external_multicast_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "Dropped_Multicast_Packets"),
            str(router_diagnostic.n_dropped_multicast_packets),
            report=(
                router_diagnostic.n_dropped_multicast_packets > 0 and
                reinjection_status is None),
            message=(
                "The router on {}, {} has dropped {} multicast route packets. "
                "Try increasing the machine_time_step and/or the time scale "
                "factor or reducing the number of atoms per core."
                .format(x, y, router_diagnostic.n_dropped_multicast_packets))))
        items.append(ProvenanceDataItem(
            self._add_name(
                names, "Dropped_Multicast_Packets_via_local_transmission"),
            str(router_diagnostic.user_3),
            report=(router_diagnostic.user_3 > 0),
            message=(
                "The router on {}, {} has dropped {} multicast packets that"
                " were transmitted by local cores. This occurs where the "
                "router has no entry associated with the multi-cast key. "
                "Try investigating the keys allocated to the vertices and "
                "the router table entries for this chip.".format(
                    x, y, router_diagnostic.user_3))))
        items.append(ProvenanceDataItem(
            self._add_name(names, "default_routed_external_multicast_packets"),
            str(router_diagnostic.user_2),
            report=(router_diagnostic.user_2 > 0 and
                    ((router_table is not None and
                      router_table.number_of_defaultable_entries == 0) or
                     router_table is None)),
            message=(
                "The router on {}, {} has default routed {} multicast packets,"
                " but the router table did not expect any default routed "
                "packets. This occurs where the router has no entry"
                " associated with the multi-cast key. "
                "Try investigating the keys allocated to the vertices and "
                "the router table entries for this chip.".format(
                    x, y, router_diagnostic.user_2))))

        items.append(ProvenanceDataItem(
            self._add_name(names, "Local_P2P_Packets"),
            str(router_diagnostic.n_local_peer_to_peer_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "External_P2P_Packets"),
            str(router_diagnostic.n_external_peer_to_peer_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "Dropped_P2P_Packets"),
            str(router_diagnostic.n_dropped_peer_to_peer_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "Local_NN_Packets"),
            str(router_diagnostic.n_local_nearest_neighbour_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "External_NN_Packets"),
            str(router_diagnostic.n_external_nearest_neighbour_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "Dropped_NN_Packets"),
            str(router_diagnostic.n_dropped_nearest_neighbour_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "Local_FR_Packets"),
            str(router_diagnostic.n_local_fixed_route_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "External_FR_Packets"),
            str(router_diagnostic.n_external_fixed_route_packets)))
        items.append(ProvenanceDataItem(
            self._add_name(names, "Dropped_FR_Packets"),
            str(router_diagnostic.n_dropped_fixed_route_packets),
            report=router_diagnostic.n_dropped_fixed_route_packets > 0,
            message=(
                "The router on chip {}:{} dropped {} Fixed route packets. "
                "This is indicative of a error within the data extraction "
                "process as this is the only expected user of fixed route "
                "packets.".format(
                    x, y, router_diagnostic.n_dropped_fixed_route_packets))))
        if reinjection_status is not None:
            items.append(ProvenanceDataItem(
                self._add_name(names, "Received_For_Reinjection"),
                reinjection_status.n_dropped_packets))
            items.append(ProvenanceDataItem(
                self._add_name(names, "Missed_For_Reinjection"),
                reinjection_status.n_missed_dropped_packets,
                report=reinjection_status.n_missed_dropped_packets > 0,
                message=(
                    "The extra monitor on {}, {} has missed {} "
                    "packets.".format(
                        x, y, reinjection_status.n_missed_dropped_packets))))
            items.append(ProvenanceDataItem(
                self._add_name(names, "Reinjection_Overflows"),
                reinjection_status.n_dropped_packet_overflows,
                report=reinjection_status.n_dropped_packet_overflows > 0,
                message=(
                    "The extra monitor on {}, {} has dropped {} "
                    "packets.".format(
                        x, y,
                        reinjection_status.n_dropped_packet_overflows))))
            items.append(ProvenanceDataItem(
                self._add_name(names, "Reinjected"),
                reinjection_status.n_reinjected_packets))
            items.append(ProvenanceDataItem(
                self._add_name(names, "Dumped_from_a_Link"),
                str(reinjection_status.n_link_dumps),
                report=reinjection_status.n_link_dumps > 0,
                message=(
                    "The extra monitor on {}, {} has detected that {} packets "
                    "were dumped from a outgoing link of this chip's router."
                    " This often occurs when external devices are used in the "
                    "script but not connected to the communication fabric "
                    "correctly. These packets may have been reinjected "
                    "multiple times and so this number may be a overestimate."
                    .format(x, y, reinjection_status.n_link_dumps))))
            items.append(ProvenanceDataItem(
                self._add_name(names, "Dumped_from_a_processor"),
                str(reinjection_status.n_processor_dumps),
                report=reinjection_status.n_processor_dumps > 0,
                message=(
                    "The extra monitor on {}, {} has detected that {} packets "
                    "were dumped from a core failing to take the packet."
                    " This often occurs when the executable has crashed or"
                    " has not been given a multicast packet callback. It can"
                    " also result from the core taking too long to process"
                    " each packet. These packets were reinjected and so this"
                    " number is likely a overestimate.".format(
                        x, y, reinjection_status.n_processor_dumps))))
        return items

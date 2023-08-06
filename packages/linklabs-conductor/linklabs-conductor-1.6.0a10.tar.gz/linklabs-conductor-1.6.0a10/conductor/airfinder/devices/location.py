""" Represents a Location Beacon. """
from enum import IntEnum

from conductor.airfinder.base import DownlinkMessageSpec
from conductor.airfinder.devices.node import Node


class Schedule():
    """ Represents the Advertising Schedule of a Location Beacon. """
    DAY_S = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday']

    class Day(IntEnum):
        SUNDAY = 0
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6

    def __init__(self, raw=None):
        """ Schedule Constructor

        Args:
            raw (int): The raw 21 byte schedule value.
        """
        self.schedule = [[0x01 for hour in range(24)] for day in range(7)]
        if raw:
            day, hour = 0, 0
            for val in bin(raw)[2:]:
                self.schedule[day][hour] = int(val)
                if hour < 23:
                    hour += 1
                else:
                    hour = 0
                    day += 1

    @property
    def value(self):
        """ Returns the 21-byte schedule as an int. """
        val = ""
        for day in self.schedule:
            for hour in day:
                val += str(hour)
        return int(val, 2)

    def set_hour(self, day, hour, val):
        """ Set a specific hour on a certain day to a value.

        Args:
            day (:class:`.Schedule.Day` or int): The day to modify.
            hour (int): The hour to modify.
            val (bool or int): The value of the hour.
        """
        self.schedule[day][hour] = int(val)

    def set_hour_per_day(self, hour, val):
        """ Set a certain hour to be (in)active every day.

        Args:
            hour (int): the hour that should be affected.
            val (bool or int): True/False, enabled or disabled.
        """
        for day in self.schedule:
            day[hour] = int(val)

    def set_day(self, day, val):
        """ Set all the hours in a day to a certain value.

        Args:
            day (:class:`.Schedule.Day` or int) the day to modify.
            val (bool or int): True/False, enabled or disabled."""
        for hour_i in range(len(self.schedule[day])):
            self.schedule[day][hour_i] = int(val)

    def print_day(self, day):
        """ Debugging tool to print the schedule for the day.

        Args:
            day (:class:`.Schedule.Day`): The day to display.
        """
        for hour_i in range(len(self.schedule[day])):
            print("\tHour {:02}: Advertising = {}"
                  .format(hour_i, bool(self.schedule[day][hour_i])))

    def show_grid(self):
        """ Debugging tool to print the entire schedule. """
        header = ["        |"]
        for day in self.DAY_S:
            header.append("{} |".format(day.center(11)))
        header.append('\n')
        header.append('=' * 100)

        print("".join(header))
        for hour_i in range(24):
            line = []
            line.append("Hour {:2} |".format(hour_i))
            for day in self.schedule:
                line.append("{} |".format(str(bool(day[hour_i])).center(11)))
            print("".join(line))


class LocationDownlinkMessageSpecV1(DownlinkMessageSpec):
    """ Message Spec for Location Beacon v1.1.

    Caution:
        Internal Object
    """

    header = {
        'def': ['msg_type', 'msg_spec_vers'],
        'struct': '>BB',
        'defaults': [0x00, 0x01]
    }

    msg_types = {
            'Configuration': {
                'def': ['mask', 'adv_en', 'schedule', 'heartbeat',
                        'rssi_adj', 'loc_weight', 'loc_group', 'tx_pwr'],
                'struct': '>BB21sIBBBB',
                'defaults': [0x00, 0x01, bytearray(b'\xff' * 21),
                             0x78, 0x00, 0x00, 0x00, 0x00]
            },
            'Reset': {
                'def': ['reset_code'],
                'struct': '>I',
                'defaults': [0xd5837ed6]
            }
    }


class LocationDownlinkMessageSpecV2(LocationDownlinkMessageSpecV1):
    """ Message Spec for Location Beacon v1.2.

    Caution:
        Internal Object
    """

    def __init__(self):
        super().__init__()
        self.header.update({'defaults': [0x00, 0x02]})
        # Same as v1.1 for Downlink


class LocationDownlinkMessageSpecV3(LocationDownlinkMessageSpecV2):
    """ Message Spec for Location Beacon v1.3.

    Caution:
        Internal Object
    """

    def __init__(self):
        super().__init__()
        self.header.update({'defaults': [0x00, 0x03]})
        self.msg_types.update(
                {'UltrasoundChange': {
                        'def': ['mask', 'freq', 'code_len', 'bps_idx',
                                'deviation', 'code_type', 'num_repeat'],
                        'struct': '>BHBBBBB',
                        'defaults': [0x00, 0x0028, 0x07, 0x02, 0x04,
                                     0x00, 0x04]
                }})


class Location(Node):
    """ Represents an Airfinder Location. """
    subject_name = 'Location'
    application = 'e9dcd73daa71fb635f36'

    @classmethod
    def _get_spec(self, vers=None):
        """ Returns: The Message Spec of the Location Beacon. """
        if not vers:
            vers = self.msg_spec_version
        if self.vers.minor == 1:
            return LocationDownlinkMessageSpecV1()
        elif self.vers.minor == 2:
            return LocationDownlinkMessageSpecV2()
        elif self.version.minor == 3:
            return LocationDownlinkMessageSpecV3()
        else:
            raise NotImplementedError

    def configure(self, ttl_s, access_point=None, **kwargs):
        """ Sends a Configuration Change to a Location.

        Args:
            ttl_s (int): The time the SymBLE Endnode has to
                request its Mailbox to receive the Downlink Message.
            access_point (:class:`.AccessPoint`): When specified, the message
                will be targeted at the specified Access Point.
            adv_en (bool): Whether to enable advertising on the Location Beacon
            schedule (:class:`.Schedule`): A Schedule of when the location
                beacon should advertise by hour.
            heartbeat (int): The heartbeat interval of the tag. How often the
                tag will send it's configuration to validate that it is still
                operational.
            rssi_adj (int): An adjustment to the perceived RSSI of the Location
                Beacon.
            loc_weight (int): A value weight to the location algorithm in the
                tag when determining location.
            loc_group (int): A value used to associate (and disassociate)
                locations in a simular phsyical location.
            tx_pwr (int): The transmit power of the Location Beacon.

        Returns:
            :class:`.NodeDownlinkMessage` when sent to all APs, otherwise,
            :class:`.DownlinkMessage` when sent to an individual AP.
        """
        pld = self._get_spec().build('Configuration', **kwargs)
        return self._send_message(pld, ttl_s, access_point)

    @classmethod
    def mulicast_configure(self, ttl_s, vers, access_point=None, **kwargs):
        """ Sends a Configuration Change to all Locations.

        Args:
            ttl_s (int):
                The time the SymBLE Endnode has to request its Mailbox to
                receive the Downlink Message.
            vers (:class:`.Version`): The Message Spec version for the
                constructed message.
            access_point (:class:`.AccessPoint`):
                When specified, the message will be targeted at the specified
                Access Point.
            adv_en (bool): Whether to enable advertising on the Location Beacon
            schedule (:class:`.Schedule`): A Schedule of when the location
                beacon should advertise by hour.
            heartbeat (int): The heartbeat interval of the tag. How often the
                tag will send it's configuration to validate that it is still
                operational.
            rssi_adj (int): An adjustment to the perceived RSSI of the Location
                Beacon.
            loc_weight (int): A value weight to the location algorithm in the
                tag when determining location.
            loc_group (int): A value used to associate (and disassociate)
                locations in a simular phsyical location.
            tx_pwr (int): The transmit power of the Location Beacon.

        Returns:
            :class:`.NodeDownlinkMessage` when sent to all APs, otherwise,
            :class:`.DownlinkMessage` when sent to an individual AP.
        """
        pld = self._get_spec(vers).build('Configuration', **kwargs)
        return self._send_multicast_message(pld, ttl_s, access_point)

    def factory_reset(self, ttl_s, access_point=None):
        """ Will Factory Reset a Location Beacon to its default settings.

        Args:
            ttl_s (int):
                The time the SymBLE Endnode has to request its Mailbox to
                receive the Downlink Message.
            access_point (:class:`.AccessPoint`):
                When specified, the message will be targeted at the specified
                Access Point.

        Returns:
            :class:`.NodeDownlinkMessage` when sent to all APs, otherwise,
            :class:`.DownlinkMessage` when sent to an individual AP.
        """
        pld = self._get_spec().build('Configuration', mask=0x0, adv_en=0x19,
                                     schedule=b'\xeb\x73\x0c\x54\x02\xce\x64'
                                              b'\xc8\x00\x00\x00\x00\x00\x00'
                                              b'\x00\x00\x00\x00\x00\x00\x00',
                                     heartbeat_int=0x0)
        return self._send_message(pld, ttl_s, access_point)

    @classmethod
    def mulicast_factory_reset(self, ttl_s, vers, access_point=None):
        """ Will Factory Reset all Location Beacons to their default settings.

        Args:
            ttl_s (int):
                The time the SymBLE Endnode has to request its Mailbox to
                receive the Downlink Message.
            vers (:class:`.Version`): The Message Spec version for the
                constructed message.
            access_point (:class:`.AccessPoint`):
                When specified, the message will be targeted at the specified
                Access Point.

        Returns:
            :class:`.NodeDownlinkMessage` when sent to all APs, otherwise,
            :class:`.DownlinkMessage` when sent to an individual AP.
        """
        pld = self._get_spec(vers).build('Configuration', mask=0x0,
                                         adv_en=0x19,
                                         schedule=b'\xeb\x73\x0c\x54\x02\xce'
                                                  b'\x64\xc8\x00\x00\x00\x00'
                                                  b'\x00\x00\x00\x00\x00\x00'
                                                  b'\x00\x00\x00',
                                         heartbeat_int=0x0)
        return self._send_multicast_message(pld, ttl_s, access_point)

    def reset(self, ttl_s, access_point=None):
        """ Power Cycle a Location.

        Args:
            ttl_s (int):
                The time the SymBLE Endnode has to request its Mailbox to
                receive the Downlink Message.
            access_point (:class:`.AccessPoint`):
                When specified, the message will be targeted at the specified
                Access Point.

        Returns:
            :class:`.NodeDownlinkMessage` when sent to all APs, otherwise,
            :class:`.DownlinkMessage` when sent to an individual AP.

        """
        pld = self._get_spec().build('Reset')
        return self._send_message(pld, ttl_s, access_point)

    @classmethod
    def multicast_reset(self, ttl_s, vers, access_point=None):
        """ Power Cycle all Locations.

        Args:
            ttl_s (int):
                The time the SymBLE Endnode has to request its Mailbox to
                receive the Downlink Message.
            vers (:class:`.Version`): The Message Spec version for the
                constructed message.
            access_point (:class:`.AccessPoint`):
                When specified, the message will be targeted at the specified
                Access Point.

        Returns:
            :class:`.NodeDownlinkMessage` when sent to all APs, otherwise,
            :class:`.DownlinkMessage` when sent to an individual AP.
        """
        pld = self._get_spec(vers).build('Reset')
        return self._send_multicast_message(pld, ttl_s, access_point)

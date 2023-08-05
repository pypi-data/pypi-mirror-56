#!/usr/bin/env python3
"""Pattoo Data Converter."""

# Standard libraries
from collections import defaultdict
from copy import deepcopy
from operator import attrgetter
import json

# Pattoo libraries
from .variables import (
    DataPointMeta, DataPoint, DeviceDataPoints, DeviceGateway, AgentPolledData)
from .constants import (
    PattooDBrecord,
    DATA_FLOAT, DATA_INT, DATA_COUNT64, DATA_COUNT, DATA_STRING, DATA_NONE)
from pattoo_shared import times
from pattoo_shared import data as lib_data


class ConvertAgentPolledData(object):
    """Converts AgentPolledData object to a standardized dict."""

    def __init__(self, agentdata):
        """Initialize the class.

        Args:
            agentdata: AgentPolledData object of data polled by agent

        Returns:
            None

        """
        # Initialize key variables
        self._data = defaultdict(lambda: defaultdict(dict))
        self._gateway_data = agentdata.data
        self._data['agent_timestamp'] = agentdata.agent_timestamp
        self._data['polling_interval'] = agentdata.polling_interval
        self._data['agent_id'] = agentdata.agent_id
        self._data['agent_program'] = agentdata.agent_program
        self._data['agent_hostname'] = agentdata.agent_hostname
        self._data['gateways'] = self._process()

    def _process(self):
        """Process.

        Args:
            None

        Returns:
            result: Data required

        """
        # Intitialize key variables
        result = {}

        if isinstance(self._gateway_data, list) is True:
            for gwd in self._gateway_data:
                if isinstance(gwd, DeviceGateway) is True:
                    if bool(gwd.valid) is True:
                        # Get information from data
                        gwd_dict = _capd_gwd2dict(gwd)
                        for gateway, values in gwd_dict.items():
                            result[gateway] = values

        # Return
        return result

    def data(self):
        """Return that that should be posted.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self._data


def convert(_data=None):
    """Convert agent cache data to AgentPolledData object.

    Args:
        _data: Agent data dict

    Returns:
        agentdata: AgentPolledData object

    """
    # Initialize key variables
    agent_id = None
    agent_program = None
    agent_hostname = None
    polling_interval = None

    # Get values to instantiate an AgentPolledData object
    (agent_id, agent_program, agent_hostname, polling_interval,
     polled_data, agent_valid) = _valid_agent(_data)
    if agent_valid is False:
        return None
    agentdata = AgentPolledData(
        agent_id, agent_program, agent_hostname, polling_interval)

    # Iterate through devices polled by the agent
    for gateway, gw_dict in sorted(polled_data.items()):
        # Create an populate the DeviceGateway object
        gwd = DeviceGateway(gateway)
        for device, devicedata in sorted(gw_dict['devices'].items()):
            # Append the DeviceDataPoints to the DeviceGateway object
            ddv = _create_ddv(device, devicedata)
            if ddv.valid is True:
                gwd.add(ddv)

        # Append the DeviceGateway to the AgentPolledData object
        if gwd.valid is True:
            agentdata.add(gwd)

    # Return
    if agentdata.valid is False:
        return None
    else:
        return agentdata


def extract(agentdata):
    """Ingest data.

    Args:
        agentdata: AgentPolledData object

    Returns:
        rows: List of named tuples containing data

    """
    # Initialize key variables
    rows = []

    # Only process valid data
    if isinstance(agentdata, AgentPolledData) is True:
        # Return if invalid data
        if bool(agentdata.valid) is False:
            return []

        # Assign agent values
        agent_id = agentdata.agent_id
        agent_program = agentdata.agent_program
        agent_hostname = agentdata.agent_hostname
        polling_interval = agentdata.polling_interval
        agent_program = agentdata.agent_program
        agent_timestamp = agentdata.agent_timestamp

        # Cycle through the data
        for gwd in agentdata.data:
            # Ignore bad data
            if gwd.valid is False:
                continue

            # Get gateway from which data came
            gateway = gwd.device

            for ddv in gwd.data:
                # Ignore bad data
                if ddv.valid is False:
                    continue

                # Get data
                device = ddv.device
                device_type = ddv.device_type
                for _dv in ddv.data:
                    # Assign values to DataPoints
                    metadata = {
                        'agent_id': agent_id,
                        'agent_program': agent_program,
                        'agent_hostname': agent_hostname,
                        'agent_timestamp': agent_timestamp,
                        'polling_interval': polling_interval,
                        'gateway': gateway,
                        'device': device,
                        'device_type': device_type
                    }
                    for key, value in metadata.items():
                        _dv.add(DataPointMeta(key, value))
                    rows.append(_dv)

    # Return
    return rows


def _add_checksum(row):
    """Determine the validity of the Agent's data.

    Args:
        row: PattooDBrecord object

    Returns:
        checksum: Calculated checksum

    """
    json_metadata = json.dumps(row.metadata, sort_keys=True)
    checksum = lib_data.hashstring('''{}{}{}{}{}{}{}{}{}{}\
'''.format(row.agent_id, row.agent_program, row.agent_hostname, row.gateway,
           row.device, row.data_label, row.data_index, row.data_type,
           row.device_type, json_metadata))

    result = PattooDBrecord(
        agent_id=row.agent_id,
        agent_program=row.agent_program,
        agent_hostname=row.agent_hostname,
        data_type=row.data_type,
        polling_interval=row.polling_interval,
        gateway=row.gateway,
        device=row.device,
        device_type=row.device_type,
        metadata=row.metadata,
        data_label=row.data_label,
        data_index=row.data_index,
        checksum=checksum,
        value=row.value,
        agent_timestamp=row.agent_timestamp,
        timestamp=row.timestamp)
    return result


def _valid_agent(_data):
    """Determine the validity of the Agent's data.

    Args:
        _data: Agent data dict

    Returns:
        result: Tuple of (
            agent_id, agent_program, agent_hostname, polled_data, agent_valid)

    """
    # Initialize key variables
    agent_id = None
    agent_program = None
    agent_hostname = None
    polling_interval = None
    polled_data = None
    agent_valid = False

    # Verify values
    if isinstance(_data, dict) is True:
        if 'agent_id' in _data:
            agent_id = _data['agent_id']
        if 'agent_program' in _data:
            agent_program = _data['agent_program']
        if 'agent_hostname' in _data:
            agent_hostname = _data['agent_hostname']
        if 'polling_interval' in _data:
            if isinstance(_data['polling_interval'], int) is True:
                polling_interval = _data['polling_interval']
        if 'gateways' in _data:
            if isinstance(_data['gateways'], dict) is True:
                polled_data = deepcopy(_data['gateways'])

    # Determine validity
    agent_valid = False not in [
        bool(agent_id), bool(agent_program),
        bool(agent_hostname),
        bool(polling_interval), bool(polled_data)]

    # Return
    result = (
        agent_id, agent_program, agent_hostname,
        polling_interval, polled_data, agent_valid)
    return result


def _create_ddv(device, devicedata):
    """Create a DeviceDataPoints object from Agent data.

    Args:
        device: Device polled by agent
        devicedata: Data polled from device by agent

    Returns:
        ddv: DeviceDataPoints object

    """
    # Initialize key variables
    ddv = DeviceDataPoints(device, device_type=None)

    # Ignore invalid data
    if isinstance(devicedata, dict) is True:
        if ('datapoints' in devicedata) and ('device_type' in devicedata):
            # Create a valid DeviceDataPoint object
            device_type = devicedata['device_type']
            ddv = DeviceDataPoints(device, device_type=device_type)

            # Iterate through the expected data_labels in the dict
            datapoint_dict = devicedata['datapoints']
            for data_label, label_dict in sorted(datapoint_dict.items()):
                # Ignore invalid data
                if isinstance(label_dict, dict) is False:
                    continue

                # Validate the presence of required keys, then process
                if ('data' in label_dict) and ('data_type' in label_dict):
                    # Skip invalid data formats
                    if isinstance(label_dict['data'], list) is False:
                        continue

                    # Add to the DeviceDataPoints
                    datapoints = _create_datapoints(data_label, label_dict)
                    ddv.add(datapoints)

    # Return
    return ddv


def _create_datapoints(data_label, label_dict):
    """Create a valid list of DataPoints for a specific label.

    Args:
        data_label: Label for data
        label_dict: Dict of data represented by the data_label

    Returns:
        datapoints: List of DataPoint objects

    """
    # Initialize key variables
    datapoints = []
    data_type = label_dict['data_type']
    found_type = False

    # Skip invalid types
    for next_type in [
            DATA_FLOAT, DATA_INT, DATA_COUNT64, DATA_COUNT,
            DATA_STRING, DATA_NONE]:
        if (data_type == next_type) and (data_type is not True) and (
                data_type is not False):
            found_type = True
    if found_type is False:
        return []

    # Add the data to the DeviceDataPoints
    for item in label_dict['data']:
        if isinstance(item, list) is True:
            if len(item) == 2:
                data_index = item[0]
                value = item[1]

                # Skip invalid numerical data
                if data_type not in (DATA_STRING, DATA_NONE):
                    try:
                        float(value)
                    except:
                        continue

                # Update DataPoint with valid data
                datapoint = DataPoint(
                    value=value,
                    data_label=data_label,
                    data_index=data_index,
                    data_type=label_dict['data_type'])
                datapoints.append(datapoint)

    # Return
    return datapoints


def _capd_gwd2dict(gwd):
    """Create dict representation of DeviceGateway object.

    Args:
        gwd: DeviceGateway object

    Returns:
        result: Representation of DeviceGateway as a dict

    """
    # Intitialize key variables
    result = {}

    # Verify data type
    if isinstance(gwd, DeviceGateway) is True:
        if bool(gwd.valid) is True:
            # Get information from data
            gateway = gwd.device

            # Analyze each DeviceDataPoints  object in data
            gwd_data_dict = {}
            for ddv in gwd.data:
                ddv_data_dict = _capd_ddv2dict(ddv)
                for remote_device, remote_data in sorted(
                        ddv_data_dict.items()):
                    if bool(remote_data) is True and (
                            isinstance(remote_data, dict) is True):
                        gwd_data_dict[remote_device] = remote_data

            # Update the result
            if bool(gwd_data_dict) is True:
                result[gateway] = {
                    'devices': gwd_data_dict
                }

    # Return
    return result


def _capd_ddv2dict(ddv):
    """Create dict representation of DeviceDataPoints object.

    Args:
        ddv: DeviceDataPoints object

    Returns:
        result: Representation of DeviceDataPoints as a dict

    """
    # Intitialize key variables
    result = {}

    # Verify data type
    if isinstance(ddv, DeviceDataPoints) is True:
        if bool(ddv.valid) is True:
            # Get information from data
            device = ddv.device
            device_type = ddv.device_type

            # Pre-populate the result with empty dicts
            datapoints = {}

            # Analyze each DataPoint for the ddv
            for _dvar in ddv.data:
                # Add keys if not already there
                if _dvar.data_label not in datapoints:
                    datapoints[_dvar.data_label] = {}

                # Assign data values to result
                data_tuple = (_dvar.data_index, _dvar.value)
                if 'data' in datapoints[_dvar.data_label]:
                    datapoints[_dvar.data_label][
                        'data'].append(data_tuple)
                else:
                    datapoints[_dvar.data_label][
                        'data_type'] = _dvar.data_type
                    datapoints[_dvar.data_label][
                        'data'] = [data_tuple]

            # Create a dict specific to the the device
            device_dict = {
                'datapoints': datapoints,
                'device_type': device_type
            }

            # Add it all to the result
            result[device] = device_dict

    # Return
    return result

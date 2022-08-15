# switchbot-mqtt - MQTT client controlling SwitchBot button & curtain automators,
# compatible with home-assistant.io's MQTT Switch & Cover platform
#
# Copyright (C) 2020 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import socket
import typing
import ssl

import asyncio_mqtt

from switchbot_mqtt._actors import _ButtonAutomator, _CurtainMotor
from switchbot_mqtt._actors.base import _MQTTCallbackUserdata

_LOGGER = logging.getLogger(__name__)


async def _mqtt_on_connect(
    mqtt_client: asyncio_mqtt.Client,
    userdata: _MQTTCallbackUserdata
) -> None:
    mqtt_broker_host, mqtt_broker_port, *_ = mqtt_client._client.socket().getpeername()
    # https://www.rfc-editor.org/rfc/rfc5952#section-6
    _LOGGER.debug(
        "connected to MQTT broker %s:%d",
        f"[{mqtt_broker_host}]"
        if mqtt_client._client.socket().family == socket.AF_INET6
        else mqtt_broker_host,
        mqtt_broker_port,
    )

    btn_task = _ButtonAutomator.mqtt_subscribe(mqtt_client=mqtt_client, settings=userdata)
    curtain_task = _CurtainMotor.mqtt_subscribe(mqtt_client=mqtt_client, settings=userdata)

    await asyncio.gather(btn_task, curtain_task)


async def _run(
    *,
    mqtt_host: str,
    mqtt_port: int,
    mqtt_disable_tls: bool,
    mqtt_username: typing.Optional[str],
    mqtt_password: typing.Optional[str],
    mqtt_topic_prefix: str,
    retry_count: int,
    device_passwords: typing.Dict[str, str],
    fetch_device_info: bool,
) -> None:
    if not mqtt_username and mqtt_password:
        raise ValueError("Missing MQTT username")

    sec_context = None
    if not mqtt_disable_tls:
        sec_context = ssl.create_default_context()

    async with asyncio_mqtt.Client(
        hostname=mqtt_host, port=mqtt_port,
        username=mqtt_username, password=mqtt_password,
        tls_context=sec_context
    ) as mqtt_client:
        _LOGGER.info(
            "connecting to MQTT broker %s:%d (TLS %s)",
            mqtt_host,
            mqtt_port,
            "disabled" if mqtt_disable_tls else "enabled",
        )

        userdata=_MQTTCallbackUserdata(
            retry_count=retry_count,
            device_passwords=device_passwords,
            fetch_device_info=fetch_device_info,
            mqtt_topic_prefix=mqtt_topic_prefix,
        )

        await _mqtt_on_connect(mqtt_client, userdata)

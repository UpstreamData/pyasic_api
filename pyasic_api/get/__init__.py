from pyasic import get_miner
from fastapi import APIRouter
from enum import Enum

class LEDMode(str, Enum):
    on = "on"
    off = "off"
    toggle = "toggle"
    status = "status"

router = APIRouter(tags=["GET"])

@router.get("/{ip}/get_data/", summary="Get data from one miner")
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    return data.asdict()


hashrate_resp = {200:
                 {"description": "Success",
                  "content": {
                    "application/json": {
                      "example": {
                        "hashrate":91.83,
                        "left_board_hashrate":30.22,
                        "center_board_hashrate":29.52,
                        "right_board_hashrate":30.59}}}}}

@router.get("/{ip}/hashrate/",
            summary="Get hashrate from one miner",
            responses=hashrate_resp)
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    return {
        "hashrate": data.hashrate,
        "left_board_hashrate": data.left_board_hashrate,
        "center_board_hashrate": data.center_board_hashrate,
        "right_board_hashrate": data.right_board_hashrate,
    }


@router.get("/{ip}/fans/", summary="Get fans speeds from one miner")
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    ret_data = {
        "fan_1": data.fan_1,
        "fan_2": data.fan_2,
    }
    if (not data.fan_3 == -1) or (not data.fan_4 == -1):
        ret_data["fan_3"] = data.fan_3
        ret_data["fan_3"] = data.fan_4

    if not data.fan_psu == -1:
        ret_data["fan_psu"] = data.fan_psu

    return ret_data


@router.get("/{ip}/temps/", summary="Get temperatures from one miner")
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    ret_data = {}
    for item in [
        "left_board_temp",
        "left_board_chip_temp",
        "center_board_temp",
        "center_board_chip_temp",
        "right_board_temp",
        "right_board_chip_temp",
        "env_temp",
    ]:
        ret_data[item] = None
        if not data[item] == -1:
            ret_data[item] = data[item]
    return ret_data


@router.get("/{ip}/power/", summary="Get power usage information from one miner")
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    ret_data = {}
    for item in ["wattage", "wattage_limit", "efficiency"]:
        ret_data[item] = None
        if not data[item] == -1:
            ret_data[item] = data[item]
    return ret_data


@router.get("/{ip}/chips/", summary="Get chip counts from one miner")
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    return {
        "left_chips": data.left_chips,
        "center_chips": data.center_chips,
        "right_chips": data.right_chips,
        "total_chips": data.total_chips,
        "ideal_chips": data.ideal_chips,
    }

led_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "on": {
                        "summary": "Light Is On",
                        "value": {"light_status": True, }
                    },
                    "off": {
                        "summary": "Light is Off",
                        "value": {"light_status": False, }
                    },
                }
            }
        }
    },
}

@router.get("/{ip}/led/{led_mode}/",
    summary="Check, toggle, or set the indicator LED state.",
    response_description="The state of the LED following this operation.",
    responses=led_responses)
async def leds(ip, led_mode: LEDMode):
    miner = await get_miner(ip)
    light_status = await miner.check_light()
    if led_mode is LEDMode.status: True
    elif led_mode is LEDMode.toggle:
        if light_status:
            await miner.fault_light_off()
            light_status = False
        else:
            await miner.fault_light_on()
            light_status = True
    elif led_mode is LEDMode.on:
        await miner.fault_light_on()
        light_status = True
    elif led_mode is LEDMode.off:
        await miner.fault_light_off()
        light_status = False
    else: True
    return {"light_status": light_status,}

'''
@router.get("/{ip}/led_toggle/", summary="Toggle the indicator LED status")
async def get_toggle_led(ip):
    miner = await get_miner(ip)
    light_status = await miner.check_light()
    if light_status:
        await miner.fault_light_off()
        light_status = False
    else:
        await miner.fault_light_on()
        light_status = True
    return {
        "light_status": light_status,
    }

@router.get("/{ip}/led_status/", summary="Query the indicator LED status")
async def get_toggle_led(ip):
    miner = await get_miner(ip)
    light_status = await miner.check_light()
    return {
        "light_status": light_status,
    }

@router.get("/{ip}/led_on/", summary="Set the indicator LED status to on")
async def get_toggle_led(ip):
    miner = await get_miner(ip)
    await miner.fault_light_on()
    light_status = await miner.check_light()
    return {
        "light_status": light_status,
    }

@router.get("/{ip}/led_off/", summary="Set the indicator LED status to off")
async def get_toggle_led(ip):
    miner = await get_miner(ip)
    await miner.fault_light_off()
    light_status = await miner.check_light()
    return {
        "light_status": light_status,
    }
'''
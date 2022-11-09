from pyasic import get_miner, MinerData
from fastapi import APIRouter, HTTPException
from enum import Enum


class LEDMode(str, Enum):
    on = "on"
    off = "off"
    toggle = "toggle"
    status = "status"


router = APIRouter(tags=["GET"])


get_data_resp = {
    200: {
        "description": "Success",
        "content": {"application/json": {"example": MinerData("1.1.1.1").asdict()}},
    }
}


@router.get(
    "/{ip}/get_data/", summary="Get data from one miner", responses=get_data_resp
)
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    return data.asdict()


hashrate_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "hashrate": 91.83,
                    "left_board_hashrate": 30.22,
                    "center_board_hashrate": 29.52,
                    "right_board_hashrate": 30.59,
                }
            }
        },
    }
}


@router.get(
    "/{ip}/hashrate/", summary="Get hashrate from one miner", responses=hashrate_resp
)
async def get_ip_hr_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    return {
        "hashrate": data.hashrate,
        "left_board_hashrate": data.left_board_hashrate,
        "center_board_hashrate": data.center_board_hashrate,
        "right_board_hashrate": data.right_board_hashrate,
    }


fans_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "fan_1": 6000,
                    "fan_2": 6000,
                    "fan_3": 6000,
                    "fan_4": 6000,
                }
            }
        },
    }
}


@router.get(
    "/{ip}/fans/", summary="Get fans speeds from one miner", responses=fans_resp
)
async def get_ip_fan_data(ip):
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


temps_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "boards": [
                        {
                            "slot": 0,
                            "board_temp": 60,
                            "chip_temp": 80,
                        },
                        {
                            "slot": 1,
                            "board_temp": 60,
                            "chip_temp": 80,
                        },
                        {
                            "slot": 2,
                            "board_temp": 60,
                            "chip_temp": 80,
                        },
                    ],
                    "env_temp": 40,
                }
            }
        },
    }
}


@router.get(
    "/{ip}/temps/", summary="Get temperatures from one miner", responses=temps_resp
)
async def get_ip_temp_data(ip):
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


power_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "wattage": 3450,
                    "wattage_limit": 3500,
                    "efficiency": 34.5,
                }
            }
        },
    }
}


@router.get(
    "/{ip}/power/",
    summary="Get power usage information from one miner",
    responses=power_resp,
)
async def get_ip_power_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    ret_data = {}
    for item in ["wattage", "wattage_limit", "efficiency"]:
        ret_data[item] = None
        if not data[item] == -1:
            ret_data[item] = data[item]
    return ret_data


chips_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "boards": [
                        {
                            "slot": 0,
                            "chips": 110,
                        },
                        {
                            "slot": 1,
                            "chips": 110,
                        },
                        {
                            "slot": 2,
                            "chips": 0,
                        },
                    ],
                    "ideal_chips": 330,
                    "total_chips": 220,
                }
            }
        },
    }
}


@router.get(
    "/{ip}/chips/", summary="Get chip counts from one miner", responses=chips_resp
)
async def get_ip_chips_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    return {
        "left_chips": data.left_chips,
        "center_chips": data.center_chips,
        "right_chips": data.right_chips,
        "total_chips": data.total_chips,
        "ideal_chips": data.ideal_chips,
    }


errors_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "errors": [
                        {"error_code": 2320, "error_message": "Hashrate is too low."}
                    ]
                }
            }
        },
    }
}


@router.get(
    "/{ip}/errors/", summary="Get error data from one miner", responses=errors_resp
)
async def get_ip_error_data(ip):
    miner = await get_miner(ip)
    errors = await miner.get_errors()
    return {"errors": errors}


led_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "on": {
                        "summary": "Light Is On",
                        "value": {
                            "light_status": True,
                        },
                    },
                    "off": {
                        "summary": "Light is Off",
                        "value": {
                            "light_status": False,
                        },
                    },
                }
            }
        },
    },
}


@router.get(
    "/{ip}/led/{led_mode}/",
    summary="Check, toggle, or set the indicator LED state.",
    response_description="The state of the LED following this operation.",
    responses=led_responses,
)
async def leds(ip, led_mode: LEDMode):
    miner = await get_miner(ip)
    light_status = await miner.check_light()
    if led_mode is LEDMode.status:
        return {"light_status": light_status}
    elif led_mode is LEDMode.toggle:
        if light_status:
            if await miner.fault_light_off():
                return {"light_status": not light_status}
        else:
            if await miner.fault_light_on():
                return {"light_status": not light_status}
        # if the light fails to toggle, light status is the same.
        # could also raise HTTP error here
        return {"light_status": light_status}
    elif led_mode is LEDMode.on:
        if await miner.fault_light_on():
            return {"light_status": True}
        raise HTTPException(status_code=400, detail="Miner failed to activate LED.")
    elif led_mode is LEDMode.off:
        if await miner.fault_light_off():
            return {"light_status": False}
        raise HTTPException(status_code=400, detail="Miner failed to deactivate LED.")


hostname_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {"example": {"hostname": "miner-123456"}}
        },
    }
}


@router.get(
    "/{ip}/hostname",
    description="Get the hostname of a miner",
    responses=hostname_resp,
)
async def get_ip_hostname_data(ip):
    miner = await get_miner(ip)
    hn = await miner.get_hostname()
    return {"hostname": hn}


model_resp = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {"example": {"model": "S9 (BOS)"}}
        },
    }
}


@router.get(
    "/{ip}/model",
    description="Get the model of a miner",
    responses=model_resp,
)
async def get_ip_model_data(ip):
    miner = await get_miner(ip)
    model = await miner.get_model()
    return {"model": model}

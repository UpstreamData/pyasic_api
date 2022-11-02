from pyasic import get_miner
from fastapi import APIRouter

router = APIRouter(tags=["GET"])

@router.get("/{ip}/get_data/", summary="Get data from one miner")
async def get_ip_data(ip):
    miner = await get_miner(ip)
    data = await miner.get_data()
    return data.asdict()


@router.get("/{ip}/hashrate/", summary="Get hashrate from one miner")
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

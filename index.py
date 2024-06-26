import re
import requests, os
from dotenv import load_dotenv, find_dotenv
import json
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()
load_dotenv(find_dotenv())
RPCURL = os.environ.get("RPCURL")
PORT = os.environ.get("APIPORT")

# Placeholder data
latestblock = []
reservecurrencies = []
mempool_res = []
rawtransaction = []
decodedrawtransaction = []
mempool_count = 0
res = []
arr_currencies = [
    {"currencyid": "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV", "ticker": "VRSC"},
    {"currencyid": "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM", "ticker": "DAI.vETH"},
    {"currencyid": "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4", "ticker": "MKR.vETH"},
    {"currencyid": "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X", "ticker": "vETH"},
    {"currencyid": "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE", "ticker": "EURC.vETH"},
    {"currencyid": "i9oCSqKALwJtcv49xUKS2U2i79h1kX6NEY", "ticker": "USDT.vETH"},
    {"currencyid": "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd", "ticker": "USDC.vETH"},
    {"currencyid": "iHax5qYQGbcMGqJKKrPorpzUBX2oFFXGnY", "ticker": "PURE.vETH"},
    {"currencyid": "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU", "ticker": "tBTC.vETH"},
    {"currencyid": "iExBJfZYK7KREDpuhj6PzZBzqMAKaFg7d2", "ticker": "vARRR" },
    {"currencyid": "i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx", "ticker": "Bridge.vETH" },
    {"currencyid": "i4Xr5TAMrDTD99H69EemhjDxJ4ktNskUtc", "ticker": "Switch" },
    {"currencyid": "i9kVWKU2VwARALpbXn4RS9zvrhvNRaUibb", "ticker": "Kaiju"}
]

def send_request(method, url, headers, data):
    response = requests.request(method, url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_bridge_currency_bridgeveth():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Bridge.vETH"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_racecondition():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["RaceCondition"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_kaiju():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Kaiju"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_pure():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Pure"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_switch():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Switch"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def get_bridge_currency_kaiju():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Kaiju"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["bestcurrencystate"]["reservecurrencies"]

def dai_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
    if dai:
        return dai["reserves"]
    return None

def vrsc_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    vrsc = next((item for item in reservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
    if vrsc:
        return vrsc["reserves"]
    return None

def mkr_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    mkr = next((item for item in reservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
    if mkr:
        return mkr["reserves"]
    return None

def eth_reserves():
    reservecurrencies = get_bridge_currency_bridgeveth()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
    if eth:
        return eth["reserves"]
    return None

def pure_reserves():
    reservecurrencies = get_bridge_currency_pure()
    pure = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if pure:
        return pure["reserves"]
    return None

def tbtc_reserves():
    reservecurrencies = get_bridge_currency_kaiju()
    tbtc = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if tbtc:
        return tbtc["reserves"]
    return None

def usdc_reserves():
    reservecurrencies = get_bridge_currency_switch()
    usdc = next((item for item in reservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
    if usdc:
        return usdc["reserves"]
    return None

def eurc_reserves():
    reservecurrencies = get_bridge_currency_switch()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
    if eth:
        return eth["reserves"]
    return None

def get_ticker_by_currency_id(currency_id):
    currency = next((item for item in arr_currencies if item["currencyid"] == currency_id), None)
    if currency:
        return currency["ticker"]
    return "Currency not found"

def get_currencyid_by_ticker(ticker):
    currency = next((item for item in arr_currencies if item["ticker"] == ticker), None)
    if currency:
        return currency["currencyid"]
    return "Currency not found"

def get_imports(currency: str):
    url = RPCURL

    json_data = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getimports",
        "params": [currency]
    }

    response = requests.post(url, json=json_data)
    return response.json()

def getvarrrblocks():
    req = requests.get("https://varrrexplorer.piratechain.com/api/getblockcount")
    return req.text

def get_imports_with_blocks(currency: str, fromblk: int, toblk: int):
    url = RPCURL

    json_data = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getimports",
        "params": [currency, fromblk, toblk]
    }

    response = requests.post(url, json=json_data)
    return response.json()

def get_address_balance(address):
    json_data = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "getaddressbalance",
        "params": [{"addresses": [address]}]
    }

    response = requests.post(RPCURL, json=json_data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data"}

def get_rawtransaction(txid):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getrawtransaction",
            "params": [txid],
            "id": 2
        }
    }
    try:
        response = send_request(**requestData)
        raw_transaction_data = response["result"]["transaction_data"]
    except Exception as error:
        return {"error": str(error)}

    return {"raw_transaction": raw_transaction_data}

def calculate_reserve_balance(currencyid: str, currency: str):
    total_reservein = 0.0
    total_reserveout = 0.0
    json_data = get_imports(currency)

    try:
        results = json_data["result"]
        for result in results:
            importnotarization = result["importnotarization"]
            currencystate = importnotarization["currencystate"]
            currencies = currencystate["currencies"]

            for currency_id, currency_data in currencies.items():
                if currency_id == str(currencyid):
                    if "reservein" in currency_data:
                        total_reservein += currency_data["reservein"]
                    if "reserveout" in currency_data:
                        total_reserveout += currency_data["reserveout"]
        ticker = get_ticker_by_currency_id(str(currencyid))
        return {
            "currencyid": ticker,
            "currency": currency,
            "reservein": total_reservein,
            "reserveout": total_reserveout
        }
    except KeyError as e:
        return {"error": f"KeyError: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

def decode_rawtransaction(hex):
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "decoderawtransaction",
            "params": [hex],
            "id": 2
        }
    }
    try:
        response = send_request(**requestData)
        decoded_transaction_data = response["result"]["decoded_data"]
    except Exception as error:
        return {"error": str(error)}
    return {"decoded_transaction": decoded_transaction_data}

def processTransactionCoinbase(vin, vout):
    is_coinbase = len(vin) == 1 and vin[0].get("coinbase")

    if is_coinbase:
        coinbase_reward_address = ""
        if vout[0]["scriptPubKey"]["addresses"][0] == "RCG8KwJNDVwpUBcdoa6AoHqHVJsA1uMYMR":
            coinbase_reward_address = vout[0]["scriptPubKey"]["addresses"][1]
        else:
            coinbase_reward_address = vout[0]["scriptPubKey"]["addresses"][0]

        return {"address": coinbase_reward_address}

    return None

def processTransactionStaking(vin, vout, coinbase_reward_address):
    try:
        matching_vin = next((v for v in vin if v.get("address") == coinbase_reward_address), None)
        matching_vout = next((v for v in vout if coinbase_reward_address in v["scriptPubKey"]["addresses"]), None)

        if matching_vin and matching_vout:
            staking_amount = matching_vout["value"]
            return {"amount": staking_amount, "address": coinbase_reward_address}
    except Exception as error:
        for vin_entry in vin:
            for vout_entry in vout:
                if (
                    vin_entry.get("valueSat") == vout_entry.get("valueSat")
                    and vin_entry.get("addresses")
                    and vout_entry["scriptPubKey"].get("addresses")
                    and len(vin_entry["addresses"]) == 1
                    and len(vout_entry["scriptPubKey"]["addresses"]) == 1
                    and vin_entry["addresses"][0] == vout_entry["scriptPubKey"]["addresses"][0]
                ):
                    return {"amount": vin_entry["value"], "address": vout_entry["scriptPubKey"]["addresses"][0]}

    return None

def processStakeBlock(transactions, block):
    coinbaseRewardAddress = None
    stakingAmount = None
    block_reward = block.get("reward", {})
    block_height = block.get("height", "")
    block_hash = block.get("hash", "")
    validation_type = block.get("validationtype", "")
    
    new_blocks = []

    for transactionId in transactions:
        try:
            transaction = get_rawtransaction(transactionId)

            if not coinbaseRewardAddress:
                coinbaseReward = processTransactionCoinbase(transaction)
                if coinbaseReward:
                    coinbaseRewardAddress = coinbaseReward["address"]
            if coinbaseRewardAddress:
                staking_reward = processTransactionStaking(transaction, coinbaseRewardAddress)
                if staking_reward:
                    stakingAmount = staking_reward["amount"]
                    new_block = {
                        "blockHeight": block_height,
                        "blockHash": block_hash,
                        "validationType": validation_type,
                        "coinbaseRewardAddress": coinbaseRewardAddress,
                        "stakingAmount": stakingAmount,
                        "stakingAddress": staking_reward["address"],
                        "blockRewards": block_reward
                    }
                    new_blocks.append(new_block)
                    print(new_block)

        except Exception as error:
            print('Error fetching transaction data:', error)

    return new_blocks

def fetchBlocksAndProcess(num_blocks, block_hash):
    current_block_hash = block_hash
    blocks_processed = 0
    request_config_get_block = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getblock",
            "params": [],
            "id": 1
        }
    }

    def process_next_block():
        nonlocal blocks_processed, current_block_hash

        if blocks_processed >= num_blocks:
            return {"result": "Process completed"}
        request_config_get_block["data"]["params"] = [current_block_hash, True]

        try:
            # Simulate sending the request
            response = send_request(request_config_get_block)
            block = response["result"]
            validation_type = block["validationtype"]

            if validation_type == "stake":
                # Replace this with your actual implementation
                processStakeBlock(block)
                blocks_processed += 1

            current_block_hash = block["previousblockhash"]
        except Exception as error:
            return {"error": str(error)}

        return process_next_block()

    # Start the process with the initial call
    return process_next_block()

def diff_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' Thousand', ' Million', ' Billion', ' Trillion'][magnitude])

def getbridgeveth_supply():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Bridge.vETH"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["lastconfirmedcurrencystate"]["supply"]

def getswitch_supply():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Switch"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["lastconfirmedcurrencystate"]["supply"]

def getpure_supply():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Pure"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["lastconfirmedcurrencystate"]["supply"]

def getkaiju_supply():
    requestData = {
        "method": "post",
        "url": RPCURL,
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrency",
            "params": ["Kaiju"],
            "id": 1
        }
    }
    response = send_request(**requestData)
    return response["result"]["lastconfirmedcurrencystate"]["supply"]

def get_currencyconverters_pure():
    networkblocks = latest_block()
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    supply = getpure_supply()
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": ["Pure"],
            "id": 1
        }
    }
    response = send_request(**requestData)

    # Assuming the JSON data is in response['result']
    data = response.get('result')

    # Initialize variables to hold the sums
    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []

    # Accessing specific elements and summing them
    for item in data:
        currency_info = item.get('iHax5qYQGbcMGqJKKrPorpzUBX2oFFXGnY')
        last_notarization = item.get('lastnotarization')

        if currency_info:
            total_initialsupply += currency_info.get('initialsupply', 0)
            total_startblock += currency_info.get('startblock', 0)

        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            currencies = currencystate.get('currencies', {})

            for key, value in currencies.items():
                total_reservein += value.get('reservein', 0)
                total_reserveout += value.get('reserveout', 0)

            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))

    # Calculate the total volume
    volume = total_reservein + total_reserveout

    # Return the extracted values along with the volume
    return {
        "bridge": "Pure",
        "initialsupply": total_initialsupply,
        "supply": supply,
        "startblock": total_startblock,
        "block": networkblocks,
        "blk_volume": volume,
        "vrsc_reserves": reserves[0] * resp,
        "vrsc_price_in_reserves": priceinreserve[0] * resp, 
        "tbtc_reserves": reserves[1] * resp,
        "tbtc_price_in_reserves": priceinreserve[1] * resp,
    }

def get_currencyconverters_bridgeveth():
    networkblocks = latest_block()
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    supply = getbridgeveth_supply()
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": ["Bridge.veth"],
            "id": 1
        }
    }
    response = send_request(**requestData)

    # Assuming the JSON data is in response['result']
    data = response.get('result')

    # Initialize variables to hold the sums
    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []

    # Accessing specific elements and summing them
    for item in data:
        currency_info = item.get('i3f7tSctFkiPpiedY8QR5Tep9p4qDVebDx')
        last_notarization = item.get('lastnotarization')

        if currency_info:
            total_initialsupply += currency_info.get('initialsupply', 0)
            total_startblock += currency_info.get('startblock', 0)

        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            currencies = currencystate.get('currencies', {})

            for key, value in currencies.items():
                total_reservein += value.get('reservein', 0)
                total_reserveout += value.get('reserveout', 0)

            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))

    # Calculate the total volume
    volume = total_reservein + total_reserveout

    # Return the extracted values along with the volume
    return {
        "bridge": "Bridge.veth",
        "initialsupply": total_initialsupply,
        "supply": supply,
        "startblock": total_startblock,
        "block": networkblocks,
        "blk_volume": volume,
        "vrsc_reserves": reserves[0] * resp,
        "vrsc_price_in_reserves": priceinreserve[0] * resp, 
        "dai_reserves": reserves[1] * resp,
        "dai_price_in_reserves": priceinreserve[1] * resp,
        "mkr_reserves": reserves[2] * resp,
        "mkr_price_in_reserves": priceinreserve[2] * resp,
        "eth_reserves": reserves[3] * resp,
        "eth_price_in_reserves": priceinreserve[3] * resp,
    }

def get_currencyconverters_switch():
    networkblocks = latest_block()
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    supply = getswitch_supply()
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": ["Switch"],
            "id": 1
        }
    }
    response = send_request(**requestData)

    # Assuming the JSON data is in response['result']
    data = response.get('result')

    # Initialize variables to hold the sums
    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []

    # Accessing specific elements and summing them
    for item in data:
        currency_info = item.get('i4Xr5TAMrDTD99H69EemhjDxJ4ktNskUtc')
        last_notarization = item.get('lastnotarization')

        if currency_info:
            total_initialsupply += currency_info.get('initialsupply', 0)
            total_startblock += currency_info.get('startblock', 0)

        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            currencies = currencystate.get('currencies', {})

            for key, value in currencies.items():
                total_reservein += value.get('reservein', 0)
                total_reserveout += value.get('reserveout', 0)

            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))

    # Calculate the total volume
    volume = total_reservein + total_reserveout

    # Return the extracted values along with the volume
    return {
        "bridge": "Switch",
        "initialsupply": total_initialsupply,
        "supply": supply,
        "startblock": total_startblock,
        "block": networkblocks,
        "blk_volume": volume,
        "vrsc_reserves": reserves[0] * resp,
        "vrsc_price_in_reserves": priceinreserve[0] * resp, 
        "dai_reserves": reserves[1] * resp,
        "dai_price_in_reserves": priceinreserve[1] * resp,
        "usdc_reserves": reserves[2] * resp,
        "usdc_price_in_reserves": priceinreserve[2] * resp,
        "eurc_reserves": reserves[3] * resp,
        "eurc_price_in_reserves": priceinreserve[3] * resp,
    }

def get_currencyconverters_kaiju():
    networkblocks = latest_block()
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    supply = getkaiju_supply()
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com/",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getcurrencyconverters",
            "params": ["Kaiju"],
            "id": 1
        }
    }
    response = send_request(**requestData)

    # Assuming the JSON data is in response['result']
    data = response.get('result')

    # Initialize variables to hold the sums
    total_initialsupply = 0
    total_startblock = 0
    total_reservein = 0
    total_reserveout = 0
    reserves = []
    priceinreserve = []

    # Accessing specific elements and summing them
    for item in data:
        currency_info = item.get('i9kVWKU2VwARALpbXn4RS9zvrhvNRaUibb')
        last_notarization = item.get('lastnotarization')

        if currency_info:
            total_initialsupply += currency_info.get('initialsupply', 0)
            total_startblock += currency_info.get('startblock', 0)

        if last_notarization:
            currencystate = last_notarization.get('currencystate', {})
            currencies = currencystate.get('currencies', {})

            for key, value in currencies.items():
                total_reservein += value.get('reservein', 0)
                total_reserveout += value.get('reserveout', 0)

            reservecurrencies = currencystate.get('reservecurrencies', [])
            for rc in reservecurrencies:
                reserves.append(rc.get('reserves', 0))
                priceinreserve.append(rc.get('priceinreserve', 0))

    # Calculate the total volume
    volume = total_reservein + total_reserveout

    # Return the extracted values along with the volume
    return {
        "bridge": "Kaiju",
        "initialsupply": total_initialsupply,
        "supply": supply,
        "startblock": total_startblock,
        "block": networkblocks,
        "blk_volume": volume,
        "vrsc_reserves": reserves[0] * resp,
        "vrsc_price_in_reserves": priceinreserve[0] * resp, 
        "usdt_reserves": reserves[1] * resp,
        "usdt_price_in_reserves": priceinreserve[1] * resp,
        "eth_reserves": reserves[2] * resp,
        "eth_price_in_reserves": priceinreserve[2] * resp,
        "tbtc_reserves": reserves[3] * resp,
        "tbtc_price_in_reserves": priceinreserve[3] * resp,
    }

def formatHashrate(hashrate):
    if hashrate < 1000:
        return f"{round(hashrate, 2)}H/s"
    elif hashrate < 1000000:
        return f"{round(hashrate/1000, 2)}kH/s"
    elif hashrate < 1000000000:
        return f"{round(hashrate/1000000, 2)}MH/s"
    elif hashrate < 1000000000000:
        return f"{round(hashrate/1000000000, 2)}GH/s"

def get_reserve_dai_price(reserves):
    return round(dai_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_vrsc_price(reserves):
    return round(vrsc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_mkr_price(reserves):
    return round(mkr_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_eth_price(reserves):
    return round(eth_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_pure_price(reserves):
    return round(pure_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_tbtc_price(reserves):
    return round(tbtc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_usdc_price(reserves):
    return round(usdc_reserves() / reserves, 6) if reserves != 0 else 0.0

def get_reserve_eurc_price(reserves):
    return round(eurc_reserves() / reserves, 6) if reserves != 0 else 0.0

def calculate_total_balances(currency: str):
    total_reservein = 0.0
    total_reserveout = 0.0
    total_conversion_fees = 0.0
    total_primary_currency_in = 0.0
    total_primary_currency_out = 0.0
    json_data = get_imports(currency)

    try:
        results = json_data["result"]
        for result in results:
            importnotarization = result["importnotarization"]
            currencystate = importnotarization["currencystate"]
            currencies = currencystate["currencies"]

            for currency_data in currencies.values():
                total_reservein += currency_data.get("reservein", 0.0)
                total_reserveout += currency_data.get("reserveout", 0.0)
                total_conversion_fees += currency_data.get("conversionfees", 0.0)
                total_primary_currency_in += currency_data.get("primarycurrencyin", 0.0)
                total_primary_currency_out += currency_data.get("primarycurrencyout", 0.0)
        reserves = dai_reserves()
        resp = get_reserve_dai_price(reserves)

        return {
            "DAI price in DAI reserves": resp,
            "total_reservein": f"{int(resp) * total_reservein} DAI",
            "total_reserveout": f"{int(resp) * total_reserveout} DAI",
            "total_conversion_fees": f"{int(resp) * total_conversion_fees} DAI",
            "total_primary_currency_in": f"{int(resp) * total_primary_currency_in} DAI",
            "total_primary_currency_out": f"{int(resp) * total_primary_currency_out} DAI",
        }
    except KeyError as e:
        return {"error": f"KeyError: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

def extract_transfers(currency: str):
    transfers_list = []
    json_data = get_imports(currency)
    try:
        results = json_data.get("result", [])
        for result in results:
            exporttxid = result.get("import", [])
            exporttxid = exporttxid['exporttxid']
            importtxid = result.get("importtxid", [])
            transfers = result.get("transfers", [])
            resp = (transfers, exporttxid, importtxid)
            transfers_list.extend(resp)

        return transfers_list
    except Exception as e:
        return {"error": str(e)}

def getcurrencystate(currency, height):
    url = 'https://rpc.vrsc.komodefi.com/'
    payload = {
        'id': 1,
        'jsonrpc': '2.0',
        'method': 'getcurrencystate',
        "params": [currency, height]
    }
    response = requests.post(url, json=payload).json()
    return response

def aggregate_reserve_data(currencyid, height):
    currencies_data = {
        "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV": {"total_reserve": 0},
        "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X": {"total_reserve": 0},
        "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4": {"total_reserve": 0},
        "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM": {"total_reserve": 0}
    }
    
    for _ in range(1440):
        response = getcurrencystate(currencyid, height)
        for currency_id, data in currencies_data.items():
            currency_info = response['result'][0]['currencystate']['currencies'][currency_id]
            data['total_reserve'] += currency_info['reservein'] + currency_info['reserveout']
        height = str(int(height) - 1)
    
    # Fetch currency names and structure the result
    result = {}
    for currency_id, data in currencies_data.items():
        currency_name = get_ticker_by_currency_id(currency_id)
        result[currency_name] = data['total_reserve']
    
    return result
       
def latest_block():
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getinfo",
            "params": [],
            "id": 3
        }
    }
    try:
        response = send_request(**requestData)
        latestblock = response["result"]["blocks"]
        return latestblock
    except:
        return "Error!!, success: False"

def load_from_json():
    try:
        with open('temp_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Temporary JSON file not found.")
        return None

@app.get("/")
def main():    
    return "result: VerusCoin Multipurpose API running on port {PORT}, an API that knows everything about verus. Use it with responsibility and have fun building your project!!", "success: True"

@app.get('/price/{ticker}')
def price(ticker):
    try:
        resp = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids=verus-coin&vs_currencies={ticker}&include_24hr_change=true")
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/difficulty')
def difficulty():
    try:
        resp = requests.get("https://explorer.verus.io/api/getdifficulty")
        cleanresp = re.sub('"', '', resp.text)
        newresp = diff_format(float(cleanresp))
        return newresp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencystate/{currency}/{height}')
def routegetcurrencystate(currency, height):
    try:
        data = getcurrencystate(currency, height)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/decoderawtransaction/{hex}')
def decode_rawtransaction_route(hex):
    try:
        data = decode_rawtransaction(hex)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getrawtransaction/{txid}')
def get_rawtransaction_route(txid):
    try:
        data = get_rawtransaction(txid)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/blockcount')
def routelatest_block():
    try:
        data = latest_block()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/Bridge.vETH')
def getcurrenciesbridgeveth():
    try:
        reservecurrencies = get_bridge_currency_bridgeveth()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/RaceCondition')
def getcurrenciesracecondition():
    try:
        reservecurrencies = get_bridge_currency_racecondition()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/getcurrencies/Kaiju')
def getcurrencieskaiju():
    try:
        reservecurrencies = get_bridge_currency_kaiju()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/Switch')
def getcurrenciesswitch():
    try:
        reservecurrencies = get_bridge_currency_switch()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/getcurrencies/Kaiju')
def getcurrencieskaiju():
    try:
        reservecurrencies = get_bridge_currency_kaiju()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencies/Pure')
def getcurrenciespure():
    try:
        reservecurrencies = get_bridge_currency_pure()
        return reservecurrencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/dai_reserves')
def getdaireserves():
    try:
        daireserve = dai_reserves()
        return daireserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/vrsc_reserves')
def getvrscreserves():
    try:
        vrscreserve = vrsc_reserves()
        return vrscreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/mkr_reserves')
def getmkrreserves():
    try:
        mkrreserve = mkr_reserves()
        return mkrreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/eth_reserves')
def getethreserves():
    try:
        ethreserve = eth_reserves()
        return ethreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/pure_reserves')
def getpurereserves():
    try:
        purereserve = pure_reserves()
        return purereserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/tbtc_reserves')
def gettbtcreserves():
    try:
        tbtcreserve = tbtc_reserves()
        return tbtcreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/usdc_reserves')
def getusdcreserves():
    try:
        usdcreserve = usdc_reserves()
        return usdcreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/eurc_reserves')
def geteurcreserves():
    try:
        eurcreserve = eurc_reserves()
        return eurcreserve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getticker/{currency_id}')
def get_ticker_route(currency_id):
    try:
        ticker = get_ticker_by_currency_id(currency_id)
        return {"ticker": ticker}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrid/{ticker}')
def get_currid_route(ticker):
    try:
        currid = get_currencyid_by_ticker(ticker)
        return {"currencyid": currid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getrawmempool')
def get_rawmempool_route():
    requestData = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getrawmempool",
            "params": [],
            "id": 2
        }
    }
    try:
        response = send_request(**requestData)
        mempool_res = response["result"]
        mempool_count = len(mempool_res)
        print(mempool_res[0])

    except Exception as error:
        return {"error": str(error)}

    return {
        "mempool_res": mempool_res,
        "mempool_count": mempool_count,
    }

@app.get('/fetchblockhash/{longest_chain}')
def fetch_block_hash_route(longest_chain):
    request_data = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getblockhash",
            "params": [longest_chain],
            "id": 1
        }
    }
    try:
        # Simulate sending the request
        response = send_request(**request_data)
        block_hash_data = response["result"]
    except Exception as error:
        return {"error": str(error)}

    # In your actual implementation, you can replace the simulated response with the real block hash data.
    return {"block_hash": block_hash_data}

@app.get('/fetchtransactiondata/{transaction_id}')
def fetch_transaction_data_route(transaction_id):
    request_config_get_raw_transaction = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "getrawtransaction",
            "params": [transaction_id],
            "id": 1
        }
    }
    try:
        response = send_request(**request_config_get_raw_transaction)
        raw_transaction_data = response["result"]
    except Exception as error:
        return {"error": str(error)}
    request_config_decode_raw_transaction = {
        "method": "post",
        "url": "https://rpc.vrsc.komodefi.com",
        "headers": {"Content-Type": "application/json"},
        "data": {
            "method": "decoderawtransaction",
            "params": [raw_transaction_data],
            "id": 1
        }
    }
    try:
        # Simulate sending the request
        response = send_request(**request_config_decode_raw_transaction)
        decoded_transaction_data = response["result"]
    except Exception as error:
        return {"error": str(error)}
    # In your actual implementation, you can replace the simulated responses with the real transaction data.
    return {"transaction_data": decoded_transaction_data}

@app.get('/getmoneysupply')
def getmoneysupply():
    resp = requests.get("https://explorer.verus.io/ext/getmoneysupply")
    return resp.text, "success: True"

@app.get('/distribution')
def getdistribution():
    resp = requests.get("https://explorer.verus.io/ext/getdistribution")
    return resp.json()

@app.get('/getnethashpower')
def getnethashpower():
    resp = requests.get("https://insight.verus.io/api/getnetworkhashps")
    value = formatHashrate(int(resp.text))
    return value, "success: True"

@app.get('/getweight_bridgeveth')
def getweightbridgeveth():
    resp = get_bridge_currency_bridgeveth()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_racecondition')
def getweightracecondition():
    resp = get_bridge_currency_racecondition()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_kaiju')
def getweightkaiju():
    resp = get_bridge_currency_kaiju()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_switch')
def getweightswitch():
    resp = get_bridge_currency_switch()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getweight_pure')
def getweightpure():
    resp = get_bridge_currency_pure()
    weights = [item['weight'] for item in resp]
    return {'weights': weights}

@app.get('/getbridgedaiprice')
def getbridgedaireserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    dai = next((item for item in reservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
    if dai:
        return dai["priceinreserve"], "success: True"
    return None

@app.get('/getbridgevrscprice')
def getbridgevrscreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    vrsc = next((item for item in reservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
    if vrsc:
        return vrsc["priceinreserve"], "success: True"
    return None

@app.get('/getbridgemkrprice')
def getbridgemkrreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    mkr = next((item for item in reservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
    if mkr:
        return mkr["priceinreserve"], "success: True"
    return None

@app.get('/getbridgeethprice')
def getbridgeethreserveprice():
    reservecurrencies = get_bridge_currency_bridgeveth()
    eth = next((item for item in reservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
    if eth:
        return eth["priceinreserve"], "success: True"
    return None

@app.get('/getbridgepureprice')
def getbridgepurereserveprice():
    reservecurrencies = get_bridge_currency_pure()
    pure = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if pure:
        return pure["priceinreserve"], "success: True"
    return None

@app.get('/getbridgetbtcprice')
def getbridgetbtcreserveprice():
    reservecurrencies = get_bridge_currency_kaiju()
    tbtc = next((item for item in reservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
    if tbtc:
        return tbtc["priceinreserve"], "success: True"
    return None

@app.get('/getbridgeusdcprice')
def getbridgeusdcreserveprice():
    reservecurrencies = get_bridge_currency_switch()
    usdc = next((item for item in reservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
    if usdc:
        return usdc["priceinreserve"], "success: True"
    return None

@app.get('/getbridgeeurcprice')
def getbridgeeurcreserveprice():
    reservecurrencies = get_bridge_currency_switch()
    eurc = next((item for item in reservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
    if eurc:
        return eurc["priceinreserve"], "success: True"
    return None

@app.get('/getdaiveth_daireserveprice')
def getdaivethdaireserveprice():
    reserves = dai_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_daireserveprice')
def getvrscdaireserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_daireserveprice')
def getmkrvethdaireserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getveth_daireserveprice')
def getvethdaireserveprice():
    reserves = eth_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getpure_daireserveprice')
def getpuredaireserveprice():
    reserves = pure_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_daireserveprice')
def gettbtcdaireserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_daireserveprice')
def getusdcdaireserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_daireserveprice')
def geteurcdaireserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_dai_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_vrscreserveprice')
def getdaivethvrscreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_vrscreserveprice')
def getvrscvrscreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_vrscreserveprice')
def getmkrvethvrscreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getveth_vrscreserveprice')
def getvethvrscreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getpure_vrscreserveprice')
def getpurevrscreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_vrscreserveprice')
def gettbtcvrscreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_vrscreserveprice')
def getusdcvrscreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_vrscreserveprice')
def geteurcvrscreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_vrsc_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_mkrreserveprice')
def getdaivethmkrreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_mkrreserveprice')
def getvrscmkrreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_mkrreserveprice')
def getmkrvethmkrreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getveth_mkrreserveprice')
def getvethmkrreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getpure_mkrreserveprice')
def getpuremkrreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_mkrreserveprice')
def gettbtcmkrreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_mkrreserveprice')
def getusdcmkrreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_mkrreserveprice')
def geteurcmkrreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_mkr_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_vethreserveprice')
def getdaivethvethreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_vethreserveprice')
def getvrscvethreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_vethreserveprice')
def getmkrvethvethreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getveth_vethreserveprice')
def getvethvethreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getpure_vethreserveprice')
def getpurevethreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_vethreserveprice')
def gettbtcvethreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_vethreserveprice')
def getusdcvethreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_vethreserveprice')
def geteurcvethreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_eth_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_purereserveprice')
def getdaivethpurereserveprice():
    reserves = dai_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_purereserveprice')
def getvrscpurereserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_purereserveprice')
def getmkrvethpurereserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getveth_purereserveprice')
def getvethpurereserveprice():
    reserves = eth_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_purereserveprice')
def gettbtcpurereserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getpure_purereserveprice')
def getpurepurereserveprice():
    reserves = pure_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_tbtcreserveprice')
def gettbctbtcrereserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_tbtc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_purereserveprice')
def getusdcpurereserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_tbtcreserveprice')
def getusdctbtcrereserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_tbtc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_tbtcreserveprice')
def geteurctbtcrereserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_tbtc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_purereserveprice')
def geteurcpurereserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_pure_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_usdcreserveprice')
def getdaivethusdcreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_usdcreserveprice')
def getvrscusdcreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_usdcreserveprice')
def getmkrvethusdcreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getveth_usdcreserveprice')
def getvethusdcreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getpure_usdcreserveprice')
def getpureusdcreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_usdcreserveprice')
def gettbtcusdcreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_usdcreserveprice')
def getusdcusdcreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_usdcreserveprice')
def geteurcusdcreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_usdc_price(reserves)
    return resp, "success: True"

@app.get('/getdaiveth_eurcreserveprice')
def getdaivetheurcreserveprice():
    reserves = dai_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getvrsc_eurcreserveprice')
def getvrsceurcreserveprice():
    reserves = vrsc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getmkrveth_eurcreserveprice')
def getmkrvetheurcreserveprice():
    reserves = mkr_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getveth_eurcreserveprice')
def getvetheurcreserveprice():
    reserves = eth_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getpure_eurcreserveprice')
def getpureeurcreserveprice():
    reserves = pure_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/gettbtc_eurcreserveprice')
def gettbctheurcreserveprice():
    reserves = tbtc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getusdc_eurcreserveprice')
def getusdceurcreserveprice():
    reserves = usdc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/geteurc_eurcreserveprice')
def geteurceurcreserveprice():
    reserves = eurc_reserves()
    resp = get_reserve_eurc_price(reserves)
    return resp, "success: True"

@app.get('/getimports/{currency}')
def routegetimports(currency: str):
    # newfromblk = int(fromblk)
    # newtoblk = int(toblk)
    try:
        newcurrency = str(currency)
        response = get_imports(newcurrency)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getimports_blk/{currency}/{fromblk}/{toblk}/')
def routegetimports_blk(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = get_imports_with_blocks(newcurrency, newfromblk, newtoblk)
    return response

@app.get('/getvolume/{currencyid}/{currency}/{fromblk}/{toblk}')
def routegetvolume(currencyid: str, currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    newcurrencyid = str(currencyid)
    response = calculate_reserve_balance(newcurrencyid, newcurrency, newfromblk, newtoblk)
    return response, "success: True"

@app.get('/gettotalvolume/{currency}/{fromblk}/{toblk}')
def routegettotalvolume(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = calculate_total_balances(newcurrency, newfromblk, newtoblk)
    return response, "success: True"

@app.get('/gettransactions/{currency}/{fromblk}/{toblk}')
def routegettxns(currency: str, fromblk: int, toblk: int):
    newfromblk = int(fromblk)
    newtoblk = int(toblk)
    newcurrency = str(currency)
    response = extract_transfers(newcurrency, newfromblk, newtoblk)
    return response

@app.get('/getaddressbalance/{address}')
def routegetaddressbalance(address: str):
    newaddress = str(address)
    response = get_address_balance(newaddress)
    return response

@app.get('/getbasketinfo/')
def routegetbasketsupply():
    try:
        bridgevethbasket = get_currencyconverters_bridgeveth()
        purebasket = get_currencyconverters_pure()
        switchbasket = get_currencyconverters_switch()
        kaijubasket = get_currencyconverters_kaiju()
        varrr_blkheight = getvarrrblocks()
        data = [
            bridgevethbasket,
            purebasket,
            switchbasket,
            kaijubasket,
            {
                "basket": "bridge.varrr",
                "height": int(varrr_blkheight),
                "supply": 74853.99232919
            }
        ]
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/getcurrencyvolumes')
def routegetcurrencyvolumes():
    try:
        data = load_from_json()
        jsond = {
            "data": data,
            "success": True
        }
        return jsond
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/market/allTickers/')
def routegetvrscdai():
    try:
        url = 'https://explorer.verus.io/api/getblockcount'
        height = requests.get(url).text
        reserves = dai_reserves()
        newreserves = vrsc_reserves()
        mkrreserves = mkr_reserves()
        ethreserves = eth_reserves()
        usdcreserves = usdc_reserves()
        eurcreserves = eurc_reserves()
        purereserves = pure_reserves()
        tbtcreserves = tbtc_reserves()
        ethprice = get_reserve_eth_price(ethreserves)
        mkrprice = get_reserve_mkr_price(mkrreserves)
        vrscprice = get_reserve_vrsc_price(newreserves)
        daiprice = get_reserve_dai_price(reserves)
        usdcprice = get_reserve_usdc_price(usdcreserves)
        eurcprice = get_reserve_eurc_price(eurcreserves)
        pureprice = get_reserve_pure_price(purereserves)
        tbtcprice = get_reserve_tbtc_price(tbtcreserves)
        bridgevethreservecurrencies = get_bridge_currency_bridgeveth()
        raceconditionreservecurrencies = get_bridge_currency_racecondition()
        kaijubasketreservecurrencies = get_bridge_currency_kaiju()
        purebasketreservecurrencies = get_bridge_currency_pure()
        switchbasketreservecurrencies = get_bridge_currency_switch()
        vrsc = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "i5w5MuNik5NtLcYmNzcvaoixooEebB6MGV"), None)
        VRSCBridgeReservePrice = vrsc['priceinreserve']
        dai = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "iGBs4DWztRNvNEJBt4mqHszLxfKTNHTkhM"), None)
        DAIBridgeReservePrice = dai['priceinreserve']
        mkr = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "iCkKJuJScy4Z6NSDK7Mt42ZAB2NEnAE1o4"), None)
        MKRBridgeReservePrice = mkr['priceinreserve']
        eth = next((item for item in bridgevethreservecurrencies if item["currencyid"] == "i9nwxtKuVYX4MSbeULLiK2ttVi6rUEhh4X"), None)
        ETHBridgeReservePrice = eth['priceinreserve']
        pure = next((item for item in purebasketreservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
        PUREBridgeReservePrice = pure['priceinreserve']
        tbtc = next((item for item in kaijubasketreservecurrencies if item["currencyid"] == "iS8TfRPfVpKo5FVfSUzfHBQxo9KuzpnqLU"), None)
        tbtcBridgeReservePrice = tbtc['priceinreserve']
        usdc = next((item for item in switchbasketreservecurrencies if item["currencyid"] == "i61cV2uicKSi1rSMQCBNQeSYC3UAi9GVzd"), None)
        usdcBridgeReservePrice = usdc['priceinreserve']
        eurc = next((item for item in switchbasketreservecurrencies if item["currencyid"] == "iC5TQFrFXSYLQGkiZ8FYmZHFJzaRF5CYgE"), None)
        EURCBridgeReservePrice = eurc['priceinreserve']
        
        ETHDAITotalBridgePrice = ETHBridgeReservePrice + DAIBridgeReservePrice
        ETHDAITotalPrice = ethprice + daiprice
        ETHMKRTotalBridgePrice = ETHBridgeReservePrice + MKRBridgeReservePrice
        ETHMKRTotalPrice = ethprice + mkrprice
        ETHVRSCTotalBridgePrice = ETHBridgeReservePrice + VRSCBridgeReservePrice
        ETHVRSCTotalPrice = ethprice + vrscprice
        ETHPURETotalBridgePrice = ETHBridgeReservePrice + PUREBridgeReservePrice
        ETHPURETotalPrice = ethprice + pureprice
        ETHTBTTCTotalBridgePrice = ETHBridgeReservePrice + tbtcBridgeReservePrice
        ETHTBTTCTotalPrice = ethprice + tbtcprice
        ETHTBTTCTotalBridgePrice = ETHBridgeReservePrice + usdcBridgeReservePrice
        ETHTBTTCTotalPrice = ethprice + usdcprice
        ETHEURCTotalBridgePrice = ETHBridgeReservePrice + EURCBridgeReservePrice
        ETHEURCTotalPrice = ethprice + eurcprice
        MKRDAITotalBridgePrice = MKRBridgeReservePrice + DAIBridgeReservePrice
        MKRDAITotalPrice = mkrprice + daiprice
        MKRVRSCTotalBridgePrice = MKRBridgeReservePrice + VRSCBridgeReservePrice
        MKRVRSCTotalPrice = mkrprice + vrscprice
        MKRETHTotalBridgePrice = MKRBridgeReservePrice + ETHBridgeReservePrice
        MKRETHTotalPrice = mkrprice + ethprice
        MKRPURETotalBridgePrice = MKRBridgeReservePrice + PUREBridgeReservePrice
        MKRPURETotalPrice = mkrprice + pureprice
        MKRTBTTCTotalBridgePrice = MKRBridgeReservePrice + tbtcBridgeReservePrice
        MKRTBTTCTotalPrice = mkrprice + tbtcprice
        MKRTBTTCTotalBridgePrice = MKRBridgeReservePrice + usdcBridgeReservePrice
        MKRTBTTCTotalPrice = mkrprice + usdcprice
        MKREURCTotalBridgePrice = MKRBridgeReservePrice + EURCBridgeReservePrice
        MKREURCTotalPrice = mkrprice + eurcprice
        DAIVRSCTotalBridgePrice = DAIBridgeReservePrice + VRSCBridgeReservePrice
        DAIVRSCTotalPrice = daiprice + vrscprice
        DAIMKRTotalBridgePrice = DAIBridgeReservePrice + MKRBridgeReservePrice
        DAIMKRTotalPrice = daiprice + mkrprice
        DAIETHTotalBridgePrice = DAIBridgeReservePrice + ETHBridgeReservePrice
        DAIETHTotalPrice = daiprice + ethprice
        DAIPURETotalBridgePrice = DAIBridgeReservePrice + PUREBridgeReservePrice
        DAIPURETotalPrice = daiprice + pureprice
        DAITBTTCTotalBridgePrice = DAIBridgeReservePrice + tbtcBridgeReservePrice
        DAITBTTCTotalPrice = daiprice + tbtcprice
        DAITBTTCTotalBridgePrice = DAIBridgeReservePrice + usdcBridgeReservePrice
        DAITBTTCTotalPrice = daiprice + usdcprice
        DAIEURCTotalBridgePrice = DAIBridgeReservePrice + EURCBridgeReservePrice
        DAIEURCTotalPrice = daiprice + eurcprice
        VRSCDAITotalBridgePrice = VRSCBridgeReservePrice + DAIBridgeReservePrice
        VRSCDAITotalPrice = vrscprice + daiprice
        VRSCMKRTotalBridgePrice = VRSCBridgeReservePrice + MKRBridgeReservePrice
        VRSCMKRTotalPrice = vrscprice + mkrprice
        VRSCETHTotalBridgePrice = VRSCBridgeReservePrice + ETHBridgeReservePrice
        VRSCETHTotalPrice = vrscprice + ethprice
        VRSCPURETotalBridgePrice = VRSCBridgeReservePrice + PUREBridgeReservePrice
        VRSCPURETotalPrice = vrscprice + pureprice
        VRSCTBTTCTotalBridgePrice = VRSCBridgeReservePrice + tbtcBridgeReservePrice
        VRSCTBTTCTotalPrice = vrscprice + tbtcprice
        VRSCTBTTCTotalBridgePrice = VRSCBridgeReservePrice + usdcBridgeReservePrice
        VRSCTBTTCTotalPrice = vrscprice + usdcprice
        VRSCEURCTotalBridgePrice = VRSCBridgeReservePrice + EURCBridgeReservePrice
        VRSCEURCTotalPrice = vrscprice + eurcprice
        bridgevethbalances = calculate_total_balances("Bridge.vETH")
        raceconditionbalances = calculate_total_balances("RaceCondition")
        kaijubasketbalances = calculate_total_balances("Kaiju")
        purebasketbalances = calculate_total_balances("Pure")
        switchbasketbalances = calculate_total_balances("Switch")
        bridgevolume = load_from_json()
        VRSC = bridgevolume["VRSC"]
        vETH = bridgevolume["vETH"]
        MKRvETH = bridgevolume["MKR.vETH"]
        DAIvETH = bridgevolume["DAI.vETH"]
        usdcvETH = bridgevolume["USDC.vETH"]
        EURCvETH = bridgevolume["EURC.vETH"]
        PUREvETH = 74441.97612458
        tbtcvETH = bridgevolume["tBTC.vETH"]
        response = [
            {
                "symbol": "VRSC-DAI",
                "symbolName": "VRSC-DAI",
                "DAIPrice": daiprice, 
                "VRSCPrice": vrscprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * daiprice} DAI",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * daiprice} DAI",
                "TotalBridgePrice": f"{VRSCDAITotalBridgePrice * daiprice} DAI",
                "TotalPrice": f"{VRSCDAITotalPrice * daiprice} DAI",
                "PairVolume": f"{VRSC + DAIvETH} DAI"
            },
            {
                "symbol": "VRSC-MKR",
                "symbolName": "VRSC-MKR",
                "MKRPrice": mkrprice,
                "VRSCPrice": vrscprice,
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": f"{VRSCMKRTotalBridgePrice * mkrprice} MKR",
                "TotalPrice": f"{VRSCMKRTotalPrice * mkrprice} MKR",
                "PairVolume": f"{VRSC + MKRvETH * mkrprice} MKR"

            },
            {
                "symbol": "VRSC-ETH",
                "symbolName": "VRSC-ETH",
                "ETHPrice": ethprice,
                "VRSCPrice": vrscprice,
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * ethprice} ETH",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * ethprice} ETH",
                "TotalBridgePrice": f"{VRSCETHTotalBridgePrice * ethprice} ETH",
                "TotalPrice": f"{VRSCETHTotalPrice * ethprice} ETH",
                "PairVolume": f"{VRSC + vETH * ethprice} ETH"
            },
            {
                "symbol": "VRSC-PURE",
                "symbolName": "VRSC-PURE",
                "PUREPrice": pureprice,
                "VRSCPrice": vrscprice,
                "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * pureprice} PURE",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * pureprice} PURE",
                "TotalBridgePrice": f"{VRSCPURETotalBridgePrice * pureprice} PURE",
                "TotalPrice": f"{VRSCPURETotalPrice * pureprice} PURE",
                "PairVolume": f"{VRSC + PUREvETH * pureprice} PURE"
            },
            {
                "symbol": "VRSC-tBTC",
                "symbolName": "VRSC-tBTC",
                "tBTCPrice": tbtcprice,
                "VRSCPrice": vrscprice,
                "tBTCBridgeReservePrice": f"{tbtcBridgeReservePrice * tbtcprice} tBTC",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * tbtcprice} tBTC",
                "TotalBridgePrice": f"{VRSCTBTTCTotalBridgePrice * tbtcprice} tBTC",
                "TotalPrice": f"{VRSCTBTTCTotalPrice * tbtcprice} tBTC",
                "PairVolume": f"{VRSC + tbtcvETH * tbtcprice} tBTC"
            },
            {
                "symbol": "VRSC-USDC",
                "symbolName": "VRSC-USDC",
                "usdcPrice": usdcprice,
                "VRSCPrice": vrscprice,
                "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * usdcprice} USDC",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * usdcprice} USDC",
                "TotalBridgePrice": f"{VRSCTBTTCTotalBridgePrice * usdcprice} USDC",
                "TotalPrice": f"{VRSCTBTTCTotalPrice * usdcprice} USDC",
                "PairVolume": f"{VRSC + usdcvETH * usdcprice} USDC"
            },
            {
                "symbol": "VRSC-EURC",
                "symbolName": "VRSC-EURC",
                "EURCPrice": eurcprice,
                "VRSCPrice": vrscprice,
                "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * eurcprice} EURC",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * eurcprice} EURC",
                "TotalBridgePrice": f"{VRSCEURCTotalBridgePrice * eurcprice} EURC",
                "TotalPrice": f"{VRSCEURCTotalPrice * eurcprice} EURC",
                "PairVolume": f"{VRSC + EURCvETH * eurcprice} EURC"
            },
            {
                "symbol": "ETH-DAI",
                "symbolName": "ETH-DAI",
                "DAIPrice": daiprice,
                "ETHPrice": ethprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * daiprice} DAI",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * daiprice} DAI",
                "TotalBridgePrice": f"{ETHDAITotalBridgePrice * daiprice} DAI",
                "TotalPrice": f"{ETHDAITotalPrice * daiprice} DAI",
                "PairVolume": f"{vETH + DAIvETH} DAI"
            },
            {
                "symbol": "ETH-MKR",
                "symbolName": "ETH-MKR",
                "MKRPrice": mkrprice,
                "ETHPrice": ethprice,
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": f"{ETHMKRTotalBridgePrice * mkrprice} MKR",
                "TotalPrice": f"{ETHMKRTotalPrice * mkrprice} MKR",
                "PairVolume": f"{vETH + MKRvETH * mkrprice} MKR"
            },
            {
                "symbol": "ETH-VRSC",
                "symbolName": "ETH-VRSC",
                "VRSCPrice": vrscprice,
                "ETHPrice": ethprice,
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * vrscprice} VRSC",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * vrscprice} VRSC",
                "TotalBridgePrice": f"{ETHVRSCTotalBridgePrice * vrscprice} VRSC",
                "TotalPrice": f"{ETHVRSCTotalPrice * vrscprice} VRSC",
                "PairVolume": f"{vETH + VRSC * vrscprice} VRSC"
            },
            {
                "symbol": "ETH-PURE",
                "symbolName": "ETH-PURE",
                "PUREPrice": pureprice,
                "ETHPrice": ethprice,
                "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * pureprice} PURE",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * pureprice} PURE",
                "TotalBridgePrice": f"{ETHPURETotalBridgePrice * pureprice} PURE",
                "TotalPrice": f"{ETHPURETotalPrice * pureprice} PURE",
                "PairVolume": f"{vETH + PUREvETH * pureprice} PURE"
            },
            {
                "symbol": "ETH-TBTC",
                "symbolName": "ETH-TBTC",
                "TBTCPrice": tbtcprice,
                "ETHPrice": ethprice,
                "TBTCBridgeReservePrice": f"{tbtcBridgeReservePrice * tbtcprice} TBTC",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * tbtcprice} TBTC",
                "TotalBridgePrice": f"{ETHTBTTCTotalBridgePrice * tbtcprice} TBTC",
                "TotalPrice": f"{ETHTBTTCTotalPrice * tbtcprice} TBTC",
                "PairVolume": f"{vETH + tbtcvETH * tbtcprice} TBTC"
            },
            {
                "symbol": "ETH-USDC",
                "symbolName": "ETH-USDC",
                "usdcPrice": usdcprice,
                "ETHPrice": ethprice,
                "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * usdcprice} USDC",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * usdcprice} USDC",
                "TotalBridgePrice": f"{ETHTBTTCTotalBridgePrice * usdcprice} USDC",
                "TotalPrice": f"{ETHTBTTCTotalPrice * usdcprice} USDC",
                "PairVolume": f"{vETH + usdcvETH * usdcprice} USDC"
            },
            {
                "symbol": "ETH-EURC",
                "symbolName": "ETH-EURC",
                "EURCPrice": eurcprice,
                "ETHPrice": ethprice,
                "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * eurcprice} EURC",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * eurcprice} EURC",
                "TotalBridgePrice": f"{ETHEURCTotalBridgePrice * eurcprice} EURC",
                "TotalPrice": f"{ETHEURCTotalPrice * eurcprice} EURC",
                "PairVolume": f"{vETH + EURCvETH * eurcprice} EURC"
            },
            {
                "symbol": "DAI-MKR",
                "symbolName": "DAI-MKR",
                "DAIPrice": daiprice,
                "MKRPrice": mkrprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * mkrprice} MKR",
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": F"{DAIMKRTotalBridgePrice * mkrprice} MKR",
                "TotalPrice": F"{DAIMKRTotalPrice * mkrprice} MKR",
                "PairVolume": f"{DAIvETH + MKRvETH * mkrprice} MKR"
            },
            {
                "symbol": "DAI-ETH",
                "symbolName": "DAI-ETH",
                "DAIPrice": daiprice,
                "ETHPrice": ethprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * ethprice} ETH",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * ethprice} ETH",
                "TotalBridgePrice": f"{DAIETHTotalBridgePrice * ethprice} ETH",
                "TotalPrice": f"{DAIETHTotalPrice * ethprice} ETH",
                "PairVolume": f"{DAIvETH + vETH * ethprice} ETH"

            },
            {
                "symbol": "DAI-VRSC",
                "symbolName": "DAI-VRSC",
                "DAIPrice": daiprice,
                "VRSCPrice": vrscprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * vrscprice} VRSC",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * vrscprice} VRSC",
                "TotalBridgePrice": f"{DAIVRSCTotalBridgePrice * vrscprice} VRSC",
                "TotalPrice": f"{DAIVRSCTotalPrice * vrscprice} VRSC",
                "PairVolume": f"{DAIvETH + VRSC * vrscprice} VRSC"
            },
            {
                "symbol": "DAI-PURE",
                "symbolName": "DAI-PURE",
                "DAIPrice": daiprice,
                "PUREPrice": pureprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * pureprice} PURE",
                "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * pureprice} PURE",
                "TotalBridgePrice": f"{DAIPURETotalBridgePrice * pureprice} PURE",
                "TotalPrice": f"{DAIPURETotalPrice * pureprice} PURE",
                "PairVolume": f"{DAIvETH + PUREvETH * pureprice} PURE"
            },
            {
                "symbol": "DAI-TBTC",
                "symbolName": "DAI-TBTC",
                "DAIPrice": daiprice,
                "TBTCPrice": tbtcprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * tbtcprice} TBTC",
                "TBTCBridgeReservePrice": f"{tbtcBridgeReservePrice * tbtcprice} TBTC",
                "TotalBridgePrice": f"{DAITBTTCTotalBridgePrice * tbtcprice} TBTC",
                "TotalPrice": f"{DAITBTTCTotalPrice * tbtcprice} TBTC",
                "PairVolume": f"{DAIvETH + tbtcvETH * tbtcprice} TBTC"
            },
            {
                "symbol": "DAI-USDC",
                "symbolName": "DAI-USDC",
                "DAIPrice": daiprice,
                "usdcPrice": usdcprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * usdcprice} USDC",
                "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * usdcprice} USDC",
                "TotalBridgePrice": f"{DAITBTTCTotalBridgePrice * usdcprice} USDC",
                "TotalPrice": f"{DAITBTTCTotalPrice * usdcprice} USDC",
                "PairVolume": f"{DAIvETH + usdcvETH * usdcprice} USDC"
            },
            {
                "symbol": "DAI-EURC",
                "symbolName": "DAI-EURC",
                "DAIPrice": daiprice,
                "EURCPrice": eurcprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * eurcprice} EURC",
                "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * eurcprice} EURC",
                "TotalBridgePrice": f"{DAIEURCTotalBridgePrice * eurcprice} EURC",
                "TotalPrice": f"{DAIEURCTotalPrice * eurcprice} EURC",
                "PairVolume": f"{DAIvETH + EURCvETH * eurcprice} EURC"
            },
            {
                "symbol": "MKR-ETH",
                "symbolName": "MKR-ETH",
                "MKRPrice": mkrprice,
                "ETHPrice": ethprice,
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * ethprice} ETH",
                "ETHBridgeReservePrice": f"{ETHBridgeReservePrice * ethprice} ETH",
                "TotalBridgePrice": f"{MKRETHTotalBridgePrice * ethprice} ETH",
                "TotalPrice": f"{MKRETHTotalPrice * ethprice} ETH",
                "PairVolume": f"{MKRvETH + vETH * ethprice} ETH"
            },
            {
                "symbol": "MKR-VRSC",
                "symbolName": "MKR-VRSC",
                "MKRPrice": mkrprice,
                "VRSCPrice": vrscprice,
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * vrscprice} VRSC",
                "VRSCBridgeReservePrice": f"{VRSCBridgeReservePrice * vrscprice} VRSC",
                "TotalBridgePrice": f"{MKRVRSCTotalBridgePrice * vrscprice} VRSC",
                "TotalPrice": f"{MKRVRSCTotalPrice * vrscprice} VRSC",
                "PairVolume": f"{MKRvETH + VRSC * vrscprice} VRSC"
            },
            {
                "symbol": "MKR-DAI",
                "symbolName": "MKR-DAI",
                "DAIPrice": daiprice,
                "MKRPrice": mkrprice,
                "DAIBridgeReservePrice": f"{DAIBridgeReservePrice * mkrprice} MKR",
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": f"{MKRDAITotalBridgePrice * mkrprice} MKR",
                "TotalPrice": f"{MKRDAITotalPrice * mkrprice} MKR",
                "PairVolume": f"{MKRvETH + DAIvETH * mkrprice} MKR"
            },
            {
                "symbol": "MKR-PURE",
                "symbolName": "MKR-PURE",
                "PUREPrice": pureprice,
                "MKRPrice": mkrprice,
                "PUREBridgeReservePrice": f"{PUREBridgeReservePrice * mkrprice} MKR",
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": f"{MKRPURETotalBridgePrice * mkrprice} MKR",
                "TotalPrice": f"{MKRPURETotalPrice * mkrprice} MKR",
                "PairVolume": f"{MKRvETH + PUREvETH * mkrprice} MKR"
            },
            {
                "symbol": "MKR-TBTC",
                "symbolName": "MKR-TBTC",
                "TBTCPrice": tbtcprice,
                "MKRPrice": mkrprice,
                "TBTCBridgeReservePrice": f"{tbtcBridgeReservePrice * mkrprice} MKR",
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": f"{MKRTBTTCTotalBridgePrice * mkrprice} MKR",
                "TotalPrice": f"{MKRTBTTCTotalPrice * mkrprice} MKR",
                "PairVolume": f"{MKRvETH + tbtcvETH * mkrprice} MKR"
            },
            {
                "symbol": "MKR-USDC",
                "symbolName": "MKR-USDC",
                "usdcPrice": usdcprice,
                "MKRPrice": mkrprice,
                "usdcBridgeReservePrice": f"{usdcBridgeReservePrice * mkrprice} MKR",
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": f"{MKRTBTTCTotalBridgePrice * mkrprice} MKR",
                "TotalPrice": f"{MKRTBTTCTotalPrice * mkrprice} MKR",
                "PairVolume": f"{MKRvETH + usdcvETH * mkrprice} MKR"
            },
            {
                "symbol": "MKR-EURC",
                "symbolName": "MKR-EURC",
                "EURCPrice": eurcprice,
                "MKRPrice": mkrprice,
                "EURCBridgeReservePrice": f"{EURCBridgeReservePrice * mkrprice} MKR",
                "MKRBridgeReservePrice": f"{MKRBridgeReservePrice * mkrprice} MKR",
                "TotalBridgePrice": f"{MKREURCTotalBridgePrice * mkrprice} MKR",
                "TotalPrice": f"{MKREURCTotalPrice * mkrprice} MKR",
                "PairVolume": f"{MKRvETH + EURCvETH * mkrprice} MKR"
            },
        {"Total Bridge Balances": [
            {"Bridge.vETH": bridgevethbalances},
            {"PureBasket": purebasketbalances},
            {"SwitchBasket": switchbasketbalances},
            {"KaijuBasket": kaijubasketbalances},
        ]},
        {"24hr Currency Volume": bridgevolume},
        ]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(PORT))

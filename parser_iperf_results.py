import json


def parser_iperf_results(data, err, status):
    error = err
    result = [el for el in data.decode.splitlines()]
    status = status
    data_for_json = {'error': error, 'result': result, 'status': status}
    res_json = json.dumps(data_for_json)
    return res_json

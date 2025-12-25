import json

def process_json_files(filenameA, filenameB, filenameC):
    try:
        with open(filenameA, 'r', encoding='utf-8') as file:
            dataA = json.load(file)
        with open(filenameB, 'r', encoding='utf-8') as file:
            dataB = json.load(file)
        with open(filenameC, 'r', encoding='utf-8') as file:
            dataC = json.load(file)
        return dataA, dataB, dataC
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return None, None, None


def main(f: dict, s: dict, t, curCel: float) -> float:
    in_terms_list = []
    out_terms_list = []

    if isinstance(f, dict) and f:
        in_terms_list = list(f.values())[0]
    if isinstance(s, dict) and s:
        out_terms_list = list(s.values())[0]

    in_terms = {}
    for term in in_terms_list:
        term_id = term.get("id")
        pts = term.get("points", [])
        if term_id is not None and isinstance(pts, list):
            in_terms[term_id] = sorted(pts, key=lambda p: p[0])

    out_terms = {}
    for term in out_terms_list:
        term_id = term.get("id")
        pts = term.get("points", [])
        if term_id is not None and isinstance(pts, list):
            out_terms[term_id] = sorted(pts, key=lambda p: p[0])

    if not in_terms or not out_terms:
        return 0.0

    x = float(curCel)
    input_mu = {}

    for term_id, pts in in_terms.items():
        mu = 0.0
        if not pts:
            input_mu[term_id] = 0.0
            continue
        if x <= pts[0][0]:
            mu = float(pts[0][1])
        elif x >= pts[-1][0]:
            mu = float(pts[-1][1])
        else:
            for i in range(len(pts) - 1):
                x0, y0 = pts[i]
                x1, y1 = pts[i + 1]
                if x0 <= x <= x1:
                    if x1 == x0:
                        mu = float(y0)
                    else:
                        mu = float(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
                    break

        input_mu[term_id] = mu

    activation_output = {}

    if isinstance(t, list):
        for rule in t:
            if not isinstance(rule, (list, tuple)) or len(rule) < 2:
                continue
            in_id = rule[0]
            out_id = rule[1]
            mu_in = input_mu.get(in_id, 0.0)
            if mu_in <= 0.0:
                continue
            prev = activation_output.get(out_id, 0.0)
            if mu_in > prev:
                activation_output[out_id] = mu_in

    if not activation_output:
        return 0.0

    min_x = None
    max_x = None
    for pts in out_terms.values():
        for xx, _ in pts:
            xx = float(xx)
            if min_x is None or xx < min_x:
                min_x = xx
            if max_x is None or xx > max_x:
                max_x = xx

    if min_x is None or max_x is None or min_x == max_x:
        return 0.0

    steps = 1000
    step = (max_x - min_x) / steps
    if step <= 0:
        step = 1.0

    mu_values = []
    cur_x = min_x

    while cur_x <= max_x + 1e-9:
        mu_agg = 0.0
        for out_id, pts in out_terms.items():
            alpha = activation_output.get(out_id, 0.0)
            if alpha <= 0.0:
                continue

            mu_y = 0.0
            if cur_x <= pts[0][0]:
                mu_y = float(pts[0][1])
            elif cur_x >= pts[-1][0]:
                mu_y = float(pts[-1][1])
            else:
                for i in range(len(pts) - 1):
                    x0, y0 = pts[i]
                    x1, y1 = pts[i + 1]
                    if x0 <= cur_x <= x1:
                        if x1 == x0:
                            mu_y = float(y0)
                        else:
                            mu_y = float(y0 + (y1 - y0) * (cur_x - x0) / (x1 - x0))
                        break

            if mu_y > alpha:
                mu_y = alpha
            if mu_y > mu_agg:
                mu_agg = mu_y

        mu_values.append((cur_x, mu_agg))
        cur_x += step

    max_mu = max(mu for _, mu in mu_values)
    if max_mu <= 0.0:
        return 0.0

    eps = 1e-9
    for x_val, mu_val in mu_values:
        if mu_val >= max_mu - eps:
            return float(x_val)

    return float(min_x)

if __name__ == "__main__":
    z = ""
    x = ""
    y = ""
    a, b, c = process_json_files(z, x, y)


    aa = {'температура': [{'id': 'холодно', 'points': [[0, 1], [18, 1], [22, 0], [50, 0]]}, {'id': 'комфортно', 'points': [[18, 0], [22, 1], [24, 1], [26, 0]]}, {'id': 'жарко', 'points': [[0, 0], [24, 0], [26, 1], [50, 1]]}]}
    bb = {'температура': [{'id': 'слабый', 'points': [[0, 0], [0, 1], [5, 1], [8, 0]]}, {'id': 'умеренный', 'points': [[5, 0], [8, 1], [13, 1], [16, 0]]}, {'id': 'интенсивный', 'points': [[13, 0], [18, 1], [23, 1], [26, 0]]}]}
    cc = [['холодно', 'интенсивный'], ['комфортно', 'умеренный'], ['жарко', 'слабый']] 
    temp = 30.0
    
    print(main(aa, bb, cc, temp))



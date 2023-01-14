def eval_query(query: str, sections: dict, cur_header: list, vals: list, f_type=False):
    local = {}
    # local["utils"] = utils # TODO load utilities functions.
    local["O"] = sections
    for key in sections:
        local[key] = sections[key]
    for key in sections:
        sections[key].set_user(cur_header, vals)
    if f_type:
        return query.format(**local)
    return eval(query, local)

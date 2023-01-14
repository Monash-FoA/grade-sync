class COMP_CONFIG:
    compute_scripts = []

    @classmethod
    def make_utils(cls):
        import sys
        import importlib.util
        class Utils:
            pass
        u = Utils()
        for i, script in enumerate(cls.compute_scripts):
            spec = importlib.util.spec_from_file_location(f"utils_{i}", script)
            module = importlib.util.module_from_spec(spec)
            # sys.modules[f"utils_{i}"] = module
            spec.loader.exec_module(module)
            for key in module.__dict__.keys():
                setattr(u, key, getattr(module, key))
        return u

def eval_query(query: str, sections: dict, cur_header: list, vals: list, f_type=False):
    local = {}
    local["utils"] = COMP_CONFIG.make_utils()
    local["O"] = sections
    for key in sections:
        local[key] = sections[key]
    for key in sections:
        sections[key].set_user(cur_header, vals)
    if f_type:
        return query.format(**local)
    return eval(query, local)

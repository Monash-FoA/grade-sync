def gen_feedback_2022_nov_a2(O):
    return f"""\
--- CODE FEEDBACK ---
Please check with the Ed submission of {O["info"]["Group Member Marked"]} to see fine grain comments.
{O["ed"]["feedback_text"]}

--- INTERVIEW FEEDBACK ---
Please see your individual feedback spreadsheet for more info.

--- SUMMARY ---
Code section: {O["ed"]["ed_mark"]}
Interview mark: {O["interview"]["Interview Mark"]}
Peer Evaluation mark: {O["peer"]["Peer Evaluation Grade"]}
Number of peers which evaluated you: {O["peer"]["#Students Rated"]}
Final mark: {O["comp"]["Total Mark"]}
"""

def gen_feedback_2022_nov_a3(O):
    return f"""\
--- CODE FEEDBACK ---
Please check with the Ed submission of {O["info"]["Group Member Marked"]} to see fine grain comments.
{O["ed"]["feedback_text"]}

--- INTERVIEW FEEDBACK ---
Please see your individual feedback spreadsheet for more info.

--- SUMMARY ---
Code section: {O["ed"]["ed_mark"]}
Interview mark: {O["interview"]["Interview Mark"]}
Peer Evaluation mark: {O["peer"]["Peer Evaluation Grade"]}
Number of peers which evaluated you: {O["peer"]["#Students Rated"]}
Final mark: {O["comp"]["Total Mark"]}
"""

def gen_mark_2022_nov_a2(O):
    group_mark = float(O["ed"]["ed_mark"] or 0)
    int_mark = float(O["interview"]["Interview Mark"] or 0)
    eval_mark = float(O["peer"]["Peer Evaluation Grade"] or 0)
    eval_n_students = int(O["peer"]["#Students Rated"] or 0)

    eval_agg = eval_mark * eval_n_students + 100 * (3 - eval_n_students)
    eval_mult = min(1, (eval_agg / 300) + 0.2)
    adjusted_group = round(group_mark * eval_mult, 2)
    final_mark = adjusted_group + round(int_mark, 2)
    return final_mark

def gen_mark_2022_nov_a3(O):
    group_mark = float(O["ed"]["ed_mark"] or 0)
    int_mark = float(O["interview"]["Interview Mark"] or 0)
    eval_mark = float(O["peer"]["Peer Evaluation Grade"] or 0)
    eval_n_students = int(O["peer"]["#Students Rated"] or 0)

    eval_agg = eval_mark * eval_n_students + 100 * (3 - eval_n_students)
    eval_mult = min(1, (eval_agg / 300) + 0.2)
    adjusted_group = round(group_mark * eval_mult, 2)
    final_mark = adjusted_group + round(int_mark, 2)
    return final_mark

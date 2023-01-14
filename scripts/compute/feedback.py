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
Final mark: {O["comp"]["Total Mark"]}
"""

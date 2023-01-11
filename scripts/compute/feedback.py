def gen_feedback_2022_a2(O):
    return f"""\
--- CODE FEEDBACK ---
Please check with the Ed submission of {O["Info"]["Group Member Marked"]} to see fine grain comments.
{O["Ed"]["feedback_text"]}

--- INTERVIEW FEEDBACK ---
Please see your individual feedback spreadsheet for more info.

--- SUMMARY ---
Code section: {O["Ed"]["ed_mark"]}
Interview mark: {O["INT"]["Interview Mark"]}
Final mark: {O["C1"]["Total Mark"]}
"""

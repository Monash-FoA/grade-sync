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

def gen_mark_2023_s1_a1(O):
    ed_mark = float(O["comp"]["fixed_ed_mark"] or 0)
    breach_mult = float(O["overrides"]["AI Breach Multiplier"])
    int_mark = float(O["interview"]["Interview Total"] or 0)
    late_penalty = float(O["comp"]["late_penalty"] or 0)
    final_mark = max(0, (ed_mark - late_penalty) * breach_mult) + round(int_mark, 2)
    return final_mark

def fix_t1_complex(ed):
    return min(2, float(ed["Task 1 - Complexity Analysis"] or 0))

def fix_total(O):
    return float(O["ed"]["ed_mark"]) - float(O["ed"]["Task 1 - Complexity Analysis"] or 0) + float(O["comp"]["fix_t1_complex"])

def gen_feedback_2023_s1_a1(O):
    ed_t1 = (
        float(O["ed"]["Task 1 - Approach"] or 0) +
        float(O["ed"]["Task 1 - Styling / Typing & Documentation"] or 0) +
        float(O["ed"]["Task 1 - Tests"] or 0) +
        float(O["comp"]["fix_t1_complex"] or 0)
    )
    ed_t2 = (
        float(O["ed"]["Task 2 - Approach"] or 0) +
        float(O["ed"]["Task 2 - Styling / Typing & Documentation"] or 0) +
        float(O["ed"]["Task 2 - Tests"] or 0) +
        float(O["ed"]["Task 2 - Complexity Analysis"] or 0)
    )
    ed_t3 = (
        float(O["ed"]["Task 3 - Approach"] or 0) +
        float(O["ed"]["Task 3 - Styling / Typing & Documentation"] or 0) +
        float(O["ed"]["Task 3 - Tests"] or 0) +
        float(O["ed"]["Task 3 - Complexity Analysis"] or 0)
    )
    ed_mark = float(O["comp"]["fixed_ed_mark"] or 0)
    late_penalty = float(O["comp"]["late_penalty"] or 0)
    breach_mult = float(O["overrides"]["AI Breach Multiplier"])
    int_q1 = float(O["interview"]["Q1"] or 0)
    int_q2 = float(O["interview"]["Q2"] or 0)
    int_q3 = float(O["interview"]["Q3"] or 0)
    int_q4 = float(O["interview"]["Q4"] or 0)
    int_q5 = float(O["interview"]["Q5"] or 0)
    int_q6 = float(O["interview"]["Q6"] or 0)
    int_mark = float(O["interview"]["Interview Total"] or 0)
    final_mark = max(0, (ed_mark - late_penalty) * breach_mult) + round(int_mark, 2)

    feedback_ed = O["ed"]["feedback_text"]
    return f"""\
A1 Feedback:

Ed Mark: {ed_t1}/10+{ed_t2}/20+{ed_t3}/20 = {ed_mark}/50 {'* breach multiplier of ' + str(breach_mult) + ' = ' + str(ed_mark * breach_mult) if breach_mult != 1 else ''}
Interview Mark: {int_q1}/10 + {int_q2}/10 + {int_q3}/10 + {int_q4}/10 + {int_q5}/10 + {int_q6}/10
    Removing worst answer gives {int_mark}/50
Late Penalty: {late_penalty}
Final Mark: {final_mark}/100

Remember to check the inline feedback comments given on Ed.
General feedback:
{feedback_ed}
"""

def percent_marked_a1_ed(ed):
    keys = [
        "Task 1 - Approach",
        "Task 1 - Styling / Typing & Documentation",
        "Task 1 - Tests",
        "Task 1 - Complexity Analysis",
        "Task 2 - Approach",
        "Task 2 - Styling / Typing & Documentation",
        "Task 2 - Tests",
        "Task 2 - Complexity Analysis",
        "Task 3 - Approach",
        "Task 3 - Styling / Typing & Documentation",
        "Task 3 - Tests",
        "Task 3 - Complexity Analysis",
    ]
    non_zero_found = False
    for key in keys:
        if ed[key] not in [0, ""]:
            non_zero_found = True
    return non_zero_found * 100

def percent_marked_a1_int(int):
    keys = [
        "Q1",
        "Q2",
        "Q3",
        "Q4",
        "Q5",
        "Q6",
    ]
    marked = len(keys)
    for key in keys:
        try:
            float(int[key])
        except:
            marked -= 1
    return round(marked / len(keys) * 100)

def gen_mark_2023_s1_a2(O):
    ed_mark = float(O["ed"]["ed_mark"] or 0)
    int_mark = float(O["interview"]["Interview Total"] or 0)
    late_penalty = float(O["comp"]["late_penalty"] or 0)
    solo = O["overrides"]["Solo Mark"]
    if solo:
        # Calculate the ed mark differently.
        ed_t1 = (
            float(O["ed"]["Task 1 - Tests"] or 0)
        )
        ed_t2 = (
            float(O["ed"]["Task 2 - Approach"] or 0) +
            float(O["ed"]["Task 2 - Tests"] or 0) +
            float(O["ed"]["Task 2 - Complexity"] or 0)
        )
        ed_t3 = (
            float(O["ed"]["Task 3 - Approach"] or 0) +
            float(O["ed"]["Task 3 - Tests"] or 0) +
            float(O["ed"]["Task 3 - Complexity"] or 0)
        )
        ed_t5 = (
            float(O["ed"]["Task 5 - Approach"] or 0) +
            float(O["ed"]["Task 5 - Tests"] or 0) +
            float(O["ed"]["Task 5 - Complexity"] or 0)
        )
        ed_t7 = (
            float(O["ed"]["Task 7 - Approach"] or 0) +
            float(O["ed"]["Task 7 - Tests"] or 0)
        )
        ed_penalty = float(O["ed"]["Formatting Penalty"] or 0)
        new_sum = ed_t1 + ed_t2 + ed_t3 + ed_t5 + ed_t7 + ed_penalty
        ed_mark = round(new_sum * 50 / 36, 2)
    final_mark = max(0, ed_mark - late_penalty) + round(int_mark, 2)
    return final_mark

def gen_feedback_2023_s1_a2(O):
    ed_t1 = (
        float(O["ed"]["Task 1 - Tests"] or 0)
    )
    ed_t2 = (
        float(O["ed"]["Task 2 - Approach"] or 0) +
        float(O["ed"]["Task 2 - Tests"] or 0) +
        float(O["ed"]["Task 2 - Complexity"] or 0)
    )
    ed_t3 = (
        float(O["ed"]["Task 3 - Approach"] or 0) +
        float(O["ed"]["Task 3 - Tests"] or 0) +
        float(O["ed"]["Task 3 - Complexity"] or 0)
    )
    ed_t4 = (
        float(O["ed"]["Task 4 - Approach"] or 0) +
        float(O["ed"]["Task 4 - Tests"] or 0) +
        float(O["ed"]["Task 4 - Complexity"] or 0)
    )
    ed_t5 = (
        float(O["ed"]["Task 5 - Approach"] or 0) +
        float(O["ed"]["Task 5 - Tests"] or 0) +
        float(O["ed"]["Task 5 - Complexity"] or 0)
    )
    ed_t6 = (
        float(O["ed"]["Task 6 - Approach"] or 0) +
        float(O["ed"]["Task 6 - Tests"] or 0) +
        float(O["ed"]["Task 6 - Complexity"] or 0)
    )
    ed_t7 = (
        float(O["ed"]["Task 7 - Approach"] or 0) +
        float(O["ed"]["Task 7 - Tests"] or 0)
    )
    ed_penalty = float(O["ed"]["Formatting Penalty"] or 0)
    solo = O["overrides"]["Solo Mark"]
    ed_mark = float(O["ed"]["ed_mark"] or 0)
    if solo:
        new_sum = ed_t1 + ed_t2 + ed_t3 + ed_t5 + ed_t7 + ed_penalty
        ed_mark = round(new_sum * 50 / 36, 2)
    late_penalty = float(O["comp"]["late_penalty"] or 0)
    int_q1 = float(O["interview"]["Q1"] or 0)
    int_q2 = float(O["interview"]["Q2"] or 0)
    int_q3 = float(O["interview"]["Q3"] or 0)
    int_q4 = float(O["interview"]["Q4"] or 0)
    int_q5 = float(O["interview"]["Q5"] or 0)
    int_q6 = float(O["interview"]["Q6"] or 0)
    int_q1_feedback = O["interview"]["Q1 Feedback"]
    int_q2_feedback = O["interview"]["Q2 Feedback"]
    int_q3_feedback = O["interview"]["Q3 Feedback"]
    int_q4_feedback = O["interview"]["Q4 Feedback"]
    int_q5_feedback = O["interview"]["Q5 Feedback"]
    int_q6_feedback = O["interview"]["Q6 Feedback"]
    int_mark = float(O["interview"]["Interview Total"] or 0)
    final_mark = max(0, ed_mark - late_penalty) + round(int_mark, 2)
    student_marked = O["ed"]["marked_user"]

    feedback_ed = O["ed"]["feedback_text"]
    ed_line = f"Ed Mark: {ed_t1}/4+{ed_t2}/8+{ed_t3}/10+{ed_t4}/8+{ed_t5}/8+{ed_t6}/6+{ed_t7}/6 {f'{ed_penalty}' if ed_penalty != 0 else ''}= {ed_mark}/50"
    if solo:
        ed_line = f"Ed Mark: {ed_t1}/4+{ed_t2}/8+{ed_t3}/10+{ed_t5}/8+{ed_t7}/6 = {new_sum}/36 {f'{ed_penalty}' if ed_penalty != 0 else ''}= {ed_mark}/50"
    return f"""\
A2 Feedback:

{ed_line}
Interview Mark: {int_q1}/10 + {int_q2}/10 + {int_q3}/10 + {int_q4}/10 + {int_q5}/10 + {int_q6}/10
    Removing worst answer gives {int_mark}/50
Late Penalty: {late_penalty}
Final Mark: {final_mark}/100

Your submission on ed was marked for the student {student_marked}. Remember to check the inline feedback comments given on Ed.
Code feedback:
{feedback_ed}

Interview feedback:
Q1: {int_q1_feedback}
Q2: {int_q2_feedback}
Q3: {int_q3_feedback}
Q4: {int_q4_feedback}
Q5: {int_q5_feedback}
Q6: {int_q6_feedback}
"""

def percent_marked_a2_ed(ed):
    keys = [
        "Task 1 - Tests",
        "Task 2 - Approach",
        "Task 2 - Tests",
        "Task 2 - Complexity",
        "Task 3 - Approach",
        "Task 3 - Tests",
        "Task 3 - Complexity",
        "Task 4 - Approach",
        "Task 4 - Tests",
        "Task 4 - Complexity",
        "Task 5 - Approach",
        "Task 5 - Tests",
        "Task 5 - Complexity",
        "Task 6 - Approach",
        "Task 6 - Tests",
        "Task 6 - Complexity",
        "Task 7 - Approach",
        "Task 7 - Tests",
    ]
    non_zero_found = False
    for key in keys:
        if ed[key] not in [0, ""]:
            non_zero_found = True
    return non_zero_found * 100

def gen_mark_2023_s1_a3(O):
    ed_t1 = (
        float(O["ed"]["Task 1 - Approach"] or 0) +
        float(O["ed"]["Task 1 - Tests"] or 0) +
        float(O["ed"]["Task 1 - Complexity"] or 0)
    )
    ed_t2 = (
        float(O["ed"]["Task 2 - Approach"] or 0) +
        float(O["ed"]["Task 2 - Tests"] or 0) +
        float(O["ed"]["Task 2 - Complexity"] or 0)
    )
    ed_t3 = (
        float(O["ed"]["Task 3 - Approach"] or 0) +
        float(O["ed"]["Task 3 - Tests"] or 0) +
        float(O["ed"]["Task 3 - Complexity"] or 0)
    )
    ed_t4 = (
        float(O["ed"]["Task 4 - Approach"] or 0) +
        float(O["ed"]["Task 4 - Tests"] or 0)
    )
    ed_t5 = (
        float(O["ed"]["Task 5 - Approach"] or 0) +
        float(O["ed"]["Task 5 - Tests"] or 0) +
        float(O["ed"]["Task 5 - Complexity"] or 0)
    )
    ed_penalty = float(O["ed"]["Formatting Penalty"] or 0)
    int_mark = float(O["interview"]["Interview Total"] or 0)
    late_penalty = float(O["comp"]["late_penalty"] or 0)
    solo = O["overrides"]["Solo Mark"]
    if solo:
        # Calculate the ed mark differently.
        new_sum = ed_t1 + ed_t2 + ed_t3 + ed_t5 + ed_penalty
        ed_mark = round(new_sum * 50 / 42, 2)
    else:
        ed_mark = ed_t1 + ed_t2 + ed_t3 + ed_t4 + ed_t5 + ed_penalty
    final_mark = max(0, ed_mark - late_penalty) + round(int_mark * 5, 2)
    return final_mark

def gen_feedback_2023_s1_a3(O):
    ed_t1 = (
        float(O["ed"]["Task 1 - Approach"] or 0) +
        float(O["ed"]["Task 1 - Tests"] or 0) +
        float(O["ed"]["Task 1 - Complexity"] or 0)
    )
    ed_t2 = (
        float(O["ed"]["Task 2 - Approach"] or 0) +
        float(O["ed"]["Task 2 - Tests"] or 0) +
        float(O["ed"]["Task 2 - Complexity"] or 0)
    )
    ed_t3 = (
        float(O["ed"]["Task 3 - Approach"] or 0) +
        float(O["ed"]["Task 3 - Tests"] or 0) +
        float(O["ed"]["Task 3 - Complexity"] or 0)
    )
    ed_t4 = (
        float(O["ed"]["Task 4 - Approach"] or 0) +
        float(O["ed"]["Task 4 - Tests"] or 0)
    )
    ed_t5 = (
        float(O["ed"]["Task 5 - Approach"] or 0) +
        float(O["ed"]["Task 5 - Tests"] or 0) +
        float(O["ed"]["Task 5 - Complexity"] or 0)
    )
    ed_penalty = float(O["ed"]["Formatting Penalty"] or 0)
    late_penalty = float(O["comp"]["late_penalty"] or 0)
    solo = O["overrides"]["Solo Mark"]
    if solo:
        # Calculate the ed mark differently.
        new_sum = ed_t1 + ed_t2 + ed_t3 + ed_t5 + ed_penalty
        ed_mark = round(new_sum * 50 / 42, 2)
    else:
        ed_mark = ed_t1 + ed_t2 + ed_t3 + ed_t4 + ed_t5 + ed_penalty
    int_q1 = float(O["interview"]["Q1"] or 0)
    int_q2 = float(O["interview"]["Q2"] or 0)
    int_q3 = float(O["interview"]["Q3"] or 0)
    int_q1_feedback = O["interview"]["Q1 Feedback"]
    int_q2_feedback = O["interview"]["Q2 Feedback"]
    int_q3_feedback = O["interview"]["Q3 Feedback"]
    int_mark = float(O["interview"]["Interview Total"] or 0)
    final_mark = max(0, ed_mark - late_penalty) + round(int_mark * 5, 2)
    student_marked = O["ed"]["marked_user"]

    feedback_ed = O["ed"]["feedback_text"]
    ed_line = f"Ed Mark: {ed_t1}/14+{ed_t2}/6+{ed_t3}/10+{ed_t4}/8+{ed_t5}/12 {f'{ed_penalty}' if ed_penalty != 0 else ''}= {ed_mark}/50"
    if solo:
        ed_line = f"Ed Mark: {ed_t1}/14+{ed_t2}/6+{ed_t3}/10+{ed_t5}/12 = {new_sum}/36 {f'{ed_penalty}' if ed_penalty != 0 else ''}= {ed_mark}/50"
    return f"""\
A3 Feedback:

{ed_line}
Interview Mark: {int_q1}/5 + {int_q2}/5 + {int_q3}/5
    Removing worst answer gives {int_mark}/10
Late Penalty: {late_penalty}
Final Mark: {final_mark}/100

Your submission on ed was marked for the student {student_marked}. Remember to check the inline feedback comments given on Ed.
Code feedback:
{feedback_ed}

Interview feedback:
Q1: {int_q1_feedback}
Q2: {int_q2_feedback}
Q3: {int_q3_feedback}
"""

def percent_marked_a3_ed(ed):
    keys = [
        "Task 1 - Approach",
        "Task 1 - Tests",
        "Task 1 - Complexity",
        "Task 2 - Approach",
        "Task 2 - Tests",
        "Task 2 - Complexity",
        "Task 3 - Approach",
        "Task 3 - Tests",
        "Task 3 - Complexity",
        "Task 4 - Approach",
        "Task 4 - Tests",
        "Task 5 - Approach",
        "Task 5 - Tests",
        "Task 5 - Complexity",
    ]
    non_zero_found = False
    for key in keys:
        if ed[key] not in [0, ""]:
            non_zero_found = True
    return non_zero_found * 100

def percent_marked_a3_int(int):
    keys = [
        "Q1",
        "Q2",
        "Q3",
    ]
    marked = len(keys)
    for key in keys:
        try:
            float(int[key])
        except:
            marked -= 1
    return round(marked / len(keys) * 100)

def gen_mark_2023_s2_a1(O):
    ed_t1 = (
        float(O["ed"]["Task 1 - Approach"] or 0) +
        float(O["ed"]["Task 1 - Tests"] or 0)
    )
    ed_t2 = (
        float(O["ed"]["Task 2 - Approach"] or 0) +
        float(O["ed"]["Task 2 - Tests"] or 0) +
        float(O["ed"]["Task 2 - Complexity"] or 0)
    )
    ed_t3 = (
        float(O["ed"]["Task 3 - Approach"] or 0) +
        float(O["ed"]["Task 3 - Tests"] or 0) +
        float(O["ed"]["Task 3 - Complexity"] or 0)
    )
    ed_t4 = (
        float(O["ed"]["Task 4 - Approach"] or 0) +
        float(O["ed"]["Task 4 - Tests"] or 0) +
        float(O["ed"]["Task 4 - Complexity"] or 0)
    )
    ed_t5 = (
        float(O["ed"]["Task 5 - Approach"] or 0) +
        float(O["ed"]["Task 5 - Tests"] or 0) +
        float(O["ed"]["Task 5 - Complexity"] or 0)
    )
    ed_t5_adv = (
        float(O["ed"]["Task 5[ADV] - Approach"] or 0) +
        float(O["ed"]["Task 5[ADV] - Tests"] or 0) +
        float(O["ed"]["Task 5[ADV] - Complexity"] or 0)
    )

    unit_code = O["info"]["Unit Code"]
    assert unit_code in ["FIT1008", "FIT2085", "FIT1054"]

    if unit_code == "FIT1054":
        total_mark = ed_t1 + ed_t2 + ed_t3 + ed_t4 + ed_t5 + ed_t5_adv
        total_mark /= 60
        total_mark = f"{100*total_mark:.2f}"
    else:
        total_mark = ed_t1 + ed_t2 + ed_t3 + ed_t4 + ed_t5
        total_mark /= 50
        total_mark = f"{100*total_mark:.2f}"

    return total_mark

def account_for_late_penalty(O):
    total_mark = float(O["comp"]["Total Mark"])
    # This is out of 50, so scale to a percentage
    late_penalty = float(O["comp"]["late_penalty"]) * 2
    ai_mult = float(O["override"]["AI Mult"] or "1")
    # academic_integrity = O["override"]["AI Case"]
    # if academic_integrity:
    #     return 0
    return round(max(0, (total_mark - late_penalty)) * ai_mult / 2, 2)

def gen_feedback_2023_s2_a1(O):
    ed_t1 = (
        float(O["ed"]["Task 1 - Approach"] or 0) +
        float(O["ed"]["Task 1 - Tests"] or 0)
    )
    ed_t2 = (
        float(O["ed"]["Task 2 - Approach"] or 0) +
        float(O["ed"]["Task 2 - Tests"] or 0) +
        float(O["ed"]["Task 2 - Complexity"] or 0)
    )
    ed_t3 = (
        float(O["ed"]["Task 3 - Approach"] or 0) +
        float(O["ed"]["Task 3 - Tests"] or 0) +
        float(O["ed"]["Task 3 - Complexity"] or 0)
    )
    ed_t4 = (
        float(O["ed"]["Task 4 - Approach"] or 0) +
        float(O["ed"]["Task 4 - Tests"] or 0) +
        float(O["ed"]["Task 4 - Complexity"] or 0)
    )
    ed_t5 = (
        float(O["ed"]["Task 5 - Approach"] or 0) +
        float(O["ed"]["Task 5 - Tests"] or 0) +
        float(O["ed"]["Task 5 - Complexity"] or 0)
    )
    ed_t5_adv = (
        float(O["ed"]["Task 5[ADV] - Approach"] or 0) +
        float(O["ed"]["Task 5[ADV] - Tests"] or 0) +
        float(O["ed"]["Task 5[ADV] - Complexity"] or 0)
    )

    marker = O["info"]["Marker"]
    unit_code = O["info"]["Unit Code"]
    assert unit_code in ["FIT1008", "FIT2085", "FIT1054"]

    total_mark = float(O["comp"]["Total Mark"])
    submitted = O["ed"]["submitted"]
    student_due_date = O["info"]["Due Date"]
    final_mark = O["comp"]["actual_total_mark"]
    feedback_text = O["ed"]["feedback_text"]

    academic_integrity = O["override"]["AI Case"]
    ai_mult = float(O["override"]["AI Mult"] or "1")

    # This is out of 50, so scale to a percentage
    late_penalty = float(O["comp"]["late_penalty"]) * 2

    if unit_code == "FIT1054":
        mark_string = f"{ed_t1}/6 + {ed_t2}/6 + {ed_t3}/16 + {ed_t4}/10 + {ed_t5}/12 + {ed_t5_adv}/10"
    else:
        mark_string = f"{ed_t1}/6 + {ed_t2}/6 + {ed_t3}/16 + {ed_t4}/10 + {ed_t5}/12"

    feedback = f"""\
Marks: {mark_string} = {total_mark}%
Your Marker was {marker}.
You submitted on {submitted} with a due date of {student_due_date}, and so received a {late_penalty}% late penalty.
So the final mark is {final_mark*2}% = {final_mark}/50

Written Feedback: {feedback_text}
"""

    if ai_mult != 1:
        feedback = f"Your submission is recognised for academic integrity issues and so received a multiplier of {ai_mult}.\n\n" + feedback

    return feedback

def percent_marked_2023_s2_a1_ed(O):
    keys = [
        "Task 1 - Approach",
        "Task 1 - Tests",
        "Task 2 - Approach",
        "Task 2 - Tests",
        "Task 2 - Complexity",
        "Task 3 - Approach",
        "Task 3 - Tests",
        "Task 3 - Complexity",
        "Task 4 - Approach",
        "Task 4 - Tests",
        "Task 4 - Complexity",
        "Task 5 - Approach",
        "Task 5 - Tests",
        "Task 5 - Complexity",
    ]
    if O["info"]["Unit Code"] == "FIT1054":
        keys.extend([
            "Task 5[ADV] - Approach",
            "Task 5[ADV] - Tests",
            "Task 5[ADV] - Complexity",
        ])
    non_zero_found = 0
    for key in keys:
        if O["ed"][key] not in [""]:
            non_zero_found += 1
    return non_zero_found / len(keys) * 100

# Interview stuff
def gen_mark_2023_s2_a12(O):
    marks = [
        float(O["interview"][f"Q{x} Mark"] or 0)
        for x in range(1, 7)
    ]
    feedback = [
        O["interview"][f"Q{x} Feedback"]
        for x in range(1, 7)
    ]
    mult = float(O["interview"]["Multiplier"] or 1)

    total_mark = sum(marks) - min(marks)

    return total_mark * mult

def plain_text(t:str):
    return (t or "")\
        .replace("&#160;", "-")\
        .replace("&amp;", "&")


def gen_feedback_2023_s2_a12(O):
    marks = [
        float(O["interview"][f"Q{x} Mark"] or 0)
        for x in range(1, 7)
    ]
    feedback = [
        plain_text(O["interview"][f"Q{x} Feedback"])
        for x in range(1, 7)
    ]
    responses = [
        plain_text(O["interview"][f"Q{x} Response"])
        for x in range(1, 7)
    ]
    mult = float(O["interview"]["Multiplier"] or 1)

    ignoring_mult = sum(marks) - min(marks)
    final_grade = gen_mark_2023_s2_a12(O)

    question_text = "\n\n".join(f"Q{x}: {marks[x-1]}/10. Response: {responses[x-1]} Feedback: {feedback[x-1]}" for x in range(1, 7))

    mult_text = f"Your final grade is {final_grade}/50" if mult == 1 else f"Your interview received a multipler of {mult}, so you actual final grade is {final_grade}/50"

    return question_text + "\n\n" + mult_text

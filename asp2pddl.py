import json
import os
import subprocess

# 运行 Clingo 命令并获取输出
def run_clingo(problem_name):
    result = subprocess.run(
        ["clingo", f"data/problems/{problem_name}.lp", "data/rules.lp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout

def is_variable(name):
    # 检查变量名称是否符合一般变量命名规范
    return name.isidentifier() and not name.startswith('_')

def generate_pddl(domain_name, problem_name):
    # 读取 Clingo 输出
    clingo_output = run_clingo(problem_name)
    print("Clingo Output:\n", clingo_output)  # 打印 Clingo 输出

    # 初始化 ASP 模型列表
    asp_model = []

    # 找到包含 "Answer:" 的行并提取下一行
    for line in clingo_output.splitlines():
        if line.startswith("Answer:"):
            next_line_index = clingo_output.splitlines().index(line) + 1
            if next_line_index < len(clingo_output.splitlines()):
                answer_line = clingo_output.splitlines()[next_line_index]
                for atom in answer_line.split():
                    if not atom.startswith('_'):
                        asp_model.append(atom)
            break

    print("ASP Model Extracted:\n", asp_model)  # 打印提取的 ASP 模型

    # 加载 goals 对象
    with open('data/goals.json', 'r') as file:
        goals = json.load(file)

    # 初始化字符串
    str_init = ""
    str_goal = ""

    # 初始化对象字典
    objects = {
        "var_type": [],
        "var": []
    }

    # 初始化所有变量
    all_vars = []

    # 处理目标
    for goal in goals:
        objects["var_type"].append(goal)
        for var in goals[goal]["required_information"]:
            objects["var_type"].append(goals[goal]["required_information"][var]["type"])
            all_vars.append(var)

    # 处理 ASP 原子
    for atom in asp_model:
        parts = atom.split('(')
        goal_var = parts[0]

        if len(parts) > 1:
            arguments = parts[1][:-1].split(',')

            if goal_var == "goal":
                objects["var"].append(arguments[0])
                str_init += f"    (has_type {arguments[0]} {arguments[1]})\n"
                for arg in goals[arguments[1]]["required_information"]:
                    arg_var = f"{arguments[0]}_{arg}"
                    arg_type = goals[arguments[1]]["required_information"][arg]["type"]
                    pred_name = goals[arguments[1]]["required_information"][arg]["predicate"]

                    objects["var"].append(arg_var)
                    str_init += f"    (has_type {arg_var} {arg_type})\n"
                    str_goal += f"    ({pred_name} {arguments[0]} {arg_var})\n"

            elif goal_var in all_vars:
                var = f"{arguments[0]}_{goal_var}"
                if is_variable(arguments[1]): 
                    str_init += f"    (value_assign {var} {arguments[1]})\n"
                    str_init += f"    (disable_get_info_api {var})\n"
                else:
                    str_init += f"    (has_value {var})\n"
                    str_init += f"    (value {var} {arguments[1]})\n"    
                # str_goal += f"    ({goal_var} {arguments[0]} {var})\n"

    # 拼接 PDDL
    pddl_output = f"(define (problem {problem_name})\n" \
                  f"  (:domain {domain_name})\n\n" \
                  f"  (:objects\n" \
                  f"    {' '.join(objects['var'])} - var\n" \
                  f"    {' '.join(objects['var_type'])} - var_type\n" \
                  f"  )\n\n" \
                  f"  (:init\n" \
                  f"{str_init}  )\n\n" \
                  f"  (:goal\n" \
                  f"    (and\n" \
                  f"{str_goal}    )\n" \
                  f"  )\n" \
                  f")"

    # 将生成的 PDDL 保存为 problem.pddl 文件
    if not os.path.exists("results"):
        os.makedirs("results")

    with open(f"results/{problem_name}.pddl", 'w') as pddl_file:
        pddl_file.write(pddl_output)

    print("Generated PDDL saved to problem.pddl")  # 确认文件已保存

    return pddl_output

def execute_sgplan(domain_name,problem_name):
    # 执行 sgplan522 命令
    command = f"./sgplan522/sgplan522 -o data/{domain_name}.pddl -f results/{problem_name}.pddl -out results/{problem_name}_plan"

    print("Executing command:", command)  # 打印执行的命令

    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印 sgplan522 的输出
    if result.stdout:
        print("SGPlan Output:\n", result.stdout)
    if result.stderr:
        print("SGPlan Error:\n", result.stderr)

# 调用函数并打印结果
domain_name = "query2plan"  # 域名
problem_name = "problem_1"  # 问题名
pddl_result = generate_pddl(domain_name, problem_name)
execute_sgplan(domain_name, problem_name)  # 执行 sgplan522

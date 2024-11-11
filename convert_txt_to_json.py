import json
import os
from comment_utils import State


def convert_txt_to_json(filename: str):
    name, _ = os.path.splitext(filename)
    name = os.path.split(name)[-1]

    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    # Split
    data_list = data.split("\n\n")
    # Extract total points
    data_dict = {"total_points": {"actual": float(data_list[0]), "max": float(data_list[0])}, "compile_error": False}
    # Extract classes (including codestyle and bonus)
    class_list = [i.splitlines() for i in data_list[1:]]
    class_data = []
    for c in class_list:
        title = c[0]
        title_list = title.split(sep=", ")
        title_points = float(title_list[0])
        title_text = title_list[1]
        d = {"title": title_text, "points": {"actual": title_points, "max": title_points}}
        task_list = []
        for task in c[1:]:
            t_list = task.split(sep=", ")
            t_points = float(t_list[0])
            t_title = t_list[1]
            t = {"title": t_title, "points": {"actual": t_points, "max": t_points}}
            task_list.append(t)
        d["tasks"] = task_list
        class_data.append(d)
    data_dict["classes"] = class_data
    with open(os.path.join(os.getcwd(), "templates", name + ".json"), "w", encoding="utf-8") as f:
        json.dump(data_dict, f, indent=4, ensure_ascii=False)


def main():
    path_to_templates = "txt_templates"
    files = [os.path.join(path_to_templates, i) for i in os.listdir(path_to_templates)]
    for i in files:
        convert_txt_to_json(i)

    # s = State(json_file="data/2024-10-30_04-color/Programmieraufgabe 4 - 04-color-Korrektur/Abgaben/Team 210343/state.json")
    # print(s.comment)


if __name__ == '__main__':
    main()

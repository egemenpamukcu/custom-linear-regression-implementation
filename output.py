'''
Linear regression assignment

Generate sample output
'''

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, line-too-long
# pylint: disable-msg= too-many-branches, wrong-import-position
# pylint: disable-msg= assignment-from-none

import sys
import os

# Handle the fact that the grading code may not
# be in the same directory as implementation
sys.path.insert(0, os.getcwd())

from regression import DataSet, Model, compute_single_var_models, \
  compute_all_vars_model, compute_best_pair, forward_selection, \
  validate_model

def format_list_of_models(task_num, models, include_R2=True,

                          gen_html=False):
    '''
    Format a list of models

    Input:
        tabs: number of spaces to indent
        models: list of model dictionaries

    Returns: string
    '''
    if gen_html:
        s = ":Task {}:\n".format(task_num)
        tabs = ""
        nl = "|br|\n"
    else:
        s = "Task {}\n".format(task_num)
        tabs = "    "
        nl = "\n"

    if not models:
        s += (tabs + "Function did not return any models" + nl)
    else:
        for m in models:
            if m is None:
                s += (tabs + "Function returned None instead of a Model" + nl)
                break
            if not isinstance(m, Model):
                s += (tabs + "Function returned something that is not a model: {}".format(type(m)) + nl)
                break


            s += (tabs + str(m) + " " + nl)
            if include_R2:
                if not hasattr(m, "R2"):
                    s += (tabs + "Function returned a Model object without an R2 attribute" + nl)
                else:
                    s += tabs + "R2: {} ".format(m.R2) + nl

    print(s)


def go(dataset, gen_html):
    '''
    Put together the work for all the tasks

    Inputs: the dataset
    '''
    models = compute_single_var_models(dataset)
    format_list_of_models("2a", models, gen_html=gen_html)

    model = compute_all_vars_model(dataset)
    format_list_of_models("2b", [model], gen_html=gen_html)

    best_bivariate_model = compute_best_pair(dataset)
    format_list_of_models("3", [best_bivariate_model], gen_html=gen_html)

    models = forward_selection(dataset)
    format_list_of_models("4", models, gen_html=gen_html)

    #best_model = None
    # best_model = choose_best_model(dataset)
    # format_list_of_models("4", [best_model], include_adj_R2=True, gen_html=gen_html)

    if gen_html:
        gh = ":"
        tabs = ""
        nl = " |br|\n"
    else:
        gh = ""
        tabs = "    "
        nl = "\n"

    s = gh + "Task 5{}\n".format(gh)
    if models is None:
        s += tabs + "Can't test this until Task 4 is implemented" + nl
    else:
        for model in models:
            testing_R2 = validate_model(dataset, model)

            s += tabs + str(model) + nl
            s += tabs + "Training R2: {}".format(model.R2) + nl
            s += tabs + "Testing R2: {}".format(testing_R2) + nl

    print(s)


if __name__ == "__main__":
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python3 output <dataset directory name> [gen_html]", file=sys.stderr)
        sys.exit(0)

    ds = DataSet(sys.argv[1])
    go(ds, gen_html=(len(sys.argv) == 3))

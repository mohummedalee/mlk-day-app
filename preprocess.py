import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
import pandas as pd
from scipy.stats import pearsonr
import sys
from pprint import pprint
import operator
import math
from plot_utils import pval_format, load_file
import json
import os
import numpy as np
from utils import hour_summed, get_err

DATA_DIR = '%s/data/'
CONTENT = ["b_o_f", "b_o_m", "b_y_f", "b_y_m", "w_o_f", "w_o_m", "w_y_f", "w_y_m", "beach",
    "skatepark", "basketball", "baseball", "violin", "nightclub", "mansion", "library",
    "gym", "street-fashion", "old-watch", "new-watch", "old-car", "new-car", "old-men-fashion",
    "new-men-fashion", "old-phone", "new-phone", "police", "firefighter", "soldier", "doctor",
    "construction-worker", "professor", "business-executive", "hipster", "school-teacher",
    "programmer", "protester", "science-lab", "computer", "graduation", "college-student", "panel-discussion", "lecture"]



def load_experiment_gender(experiment, root):
    exp_w = 0
    exp_m = 0

    exp_m += load_file(DATA_DIR%root + 'original/' + experiment+'-n' + '/' + experiment+'-n' + '-men.txt')['reach'].iloc[-1]
    exp_w += load_file(DATA_DIR%root + 'flipped/' + experiment+'-f' + '/' + experiment+'-f' + '-women.txt')['reach'].iloc[-1]
    exp_m += load_file(DATA_DIR%root + 'original/' + experiment+'-n' + '/' + experiment+'-n' + '-men.txt')['reach'].iloc[-1]
    exp_w += load_file(DATA_DIR%root + 'flipped/' + experiment+'-f' + '/' + experiment+'-f' + '-women.txt')['reach'].iloc[-1]

    frac_men = exp_m/(exp_w+exp_m)
    N = exp_w+exp_m
    err = get_err(frac_men, N)
    return  frac_men, exp_m, exp_w, err


def load_experiment_race(experiment, root):
    exp_w = 0
    exp_b = 0

    exp_w += load_file(DATA_DIR%root + 'original/' + experiment+'-n' + '/' + experiment+'-n' + '-white.txt')['reach'].iloc[-1]
    exp_w += load_file(DATA_DIR%root + 'flipped/' + experiment+'-f' + '/' + experiment+'-f' + '-white.txt')['reach'].iloc[-1]
    exp_b += load_file(DATA_DIR%root + 'original/' + experiment+'-n' + '/' + experiment+'-n' + '-black.txt')['reach'].iloc[-1]
    exp_b += load_file(DATA_DIR%root + 'flipped/' + experiment+'-f' + '/' + experiment+'-f' + '-black.txt')['reach'].iloc[-1]

    frac_white = exp_w/(exp_w+exp_b)
    N = exp_w+exp_b
    err = get_err(frac_white, N)
    return  frac_white, exp_w, exp_b, err

def main(root):
    out = {}
    fracs_race = {}
    fracs_gender = {}
    races = ['White','Black']
    titles = ['Basketball','College','Computer','Beach', 'College 2', 'Firefighter', 'Police', 'Science Lab', 'Skatepark', 'Soldier', 'Violin']
    titles = CONTENT
    f, ax = plt.subplots()

    for idx, description in enumerate(CONTENT):
        frac, n_white, n_black, err = load_experiment_race(description, root)
        fracs_race[description] = frac
        frac_g, n_male, n_female, err = load_experiment_gender(description, root)
        fracs_gender[description] = frac_g
        ax.errorbar([frac], [len(CONTENT)-1-idx], fmt='o', xerr=err)

        out[description] = {
            'male': str(n_male),
            'female': str(n_female),
            'black': str(n_black),
            'white': str(n_white),
            'frac_white': str(frac),
            'frac_men': str(frac_g)
        }

    ax.set_xlabel('Estimated fraction of white users in the audience')
    # ax.set_yticks([0, 1, 2])
    ax.set_yticks(list(range(len(CONTENT))))
    # ax.set_ylim(-.5, 2.5)
    ax.set_yticklabels(titles[::-1])
    ax.grid(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # f.set_size_inches(settings.FIG_WIDTH, settings.FIG_HEIGHT/2)
    print('estimated fraction of white users:')
    pprint(sorted(fracs_race.items(), key=operator.itemgetter(1), reverse=True))
    print('\nfraction of men:')
    pprint(sorted(fracs_gender.items(), key=operator.itemgetter(1), reverse=True))
    # f.savefig('%s/mlk-race-pilot.pdf'%root, bbox_inches='tight')

    # save for the web app
    # pprint(out)
    with open('experiment_stats.json', 'w') as wh:
        json.dump(out, wh, indent=2)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        root = '.'
    else:
        root = sys.argv[-1]

    main(root)

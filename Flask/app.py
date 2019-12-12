import json

from flask import Flask, render_template
import pandas as pd
import numpy as np


app = Flask(__name__)

# Create a list of the column names corresponding with the number of choices in df
choices = ["player.choice_" + str(i) for i in range(1, 9)]
# Select the other columns we want
cols = ['player.id_in_group', 'player.risk', 'session.code']
# Merge the two lists
usecols = cols + choices

# Create the dataframe from CSV
df = pd.read_csv('data/risk_lottery_2019-12-11.csv', usecols=usecols)

# We only want the data from the relevant session
df = df.loc[df['session.code'] == '32nbns7y']

# Delete empty sessions
df = df.dropna()

# Drop an irrelevant entry (Last Entry in Session)
df = df.drop(df.index[-1])

aggregate = df.iloc[:, 2:10]


def safe_choices(df):
    list = []
    # Get the number of entries in the specified column
    n = df.shape[0]
    for choice in choices:
        list.append(np.sum(df[choice] == 0) / n)
    return list


safeChoices = safe_choices(aggregate)

risk_averse = [1, 1, 1, 1, 1, 1, 1, 1]
risk_neutral = [1, 1, 1, 0, 0, 0, 0, 0]
risk_loving = [0, 0, 0, 0, 0, 0, 0, 0]


@app.route("/")
def index():
    chart_df = pd.DataFrame({'safeChoice': safeChoices, 'riskNeutral': risk_neutral})
    chart_data = chart_df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    return render_template("index.html", data=data)


# @app.route('/participant/<participant_id>', methods=['GET'])
# def show_partcipant(participant_id):
#     for user in participant_id:
#         participant_id = user
#     return render_template('user.html', participant_id=participant_id)


if __name__ == '__main__':
    app.run()

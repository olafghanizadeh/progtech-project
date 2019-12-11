from flask import Flask, render_template, json, request, redirect, url_for
import c3pyo as c3
import pandas as pd
import numpy as np

app = Flask(__name__)

# Create a list of the column names corresponding with the number of choices in df
choices = ["player.choice_" + str(i) for i in range(1, 9)]
# Select the other columns we want
cols = ['player.id_in_group', 'player.name', 'player.risk', 'session.code']
# Merge the two lists
usecols = cols + choices

# Create the dataframe from CSV
df = pd.read_csv('../Data/risk_lottery_2019-12-11.csv', usecols=usecols)
# We only want the data from the relevant session
df = df.loc[df['session.code'] == '32nbns7y']

# Delete empty sessions
df = df.dropna()


# A function to replace the numeric values with a more humanreadable output
def replace_numeric(df):
    for choice in choices:
        df[choice].replace({0: 'A', 1: 'B'}, inplace=True)

    df['player.risk'].replace({1.0: 'Risk Averse', 2.0: 'Risk Neutral', 3.0: 'Risk Loving'}, inplace=True)

    return df


chosen_profile = [0, 0, 0, 0, 1, 1, 1, 1]

aggregate = df.iloc[:, 3:11]
choice = [choice for choice in range(1, 9)]


def safe_choices_plot(df):
    list = []
    n = df.shape[0]
    for choice in choices:
        list.append(np.sum(df[choice] == 0) / n)
    return list


y1 = safe_choices_plot(aggregate)

display_df = df['player.name'].to_list()

user_id = df['player.id_in_group'].to_list()


#user_choices = df.iloc[:, 1:11]
#user_choices = replace_numeric(user_choices)


#user_choices = user_choices.to_html()



def get_line_chart_json():
    # data
    x = [i for i in range(1, 9)]
    x_ticks = ['Choice ' + str(i) for i in range(1, 9)]
    y2 = [1, 1, 1, 0, 0, 0, 0, 0]

    # chart
    chart = c3.LineChart()
    chart.legend_position('inset')
    chart.plot(x, y1, label='Safe Choices')
    chart.plot(x, y2, label='Risk Neutral')
    chart.ylabel('Safe Choices')
    chart.bind_to('line_chart_div')

    return chart.json()




@app.route("/", methods=['GET', 'POST'])
def index():
    chart_json = get_line_chart_json()

    return render_template("index.html", chart_json=chart_json)


@app.route('/participant/<participant_id>', methods=['GET'])
def show_partcipant(participant_id):
    for user in participant_id:
        participant_id = user
    return render_template('user.html', participant_id=participant_id)




if __name__ == '__main__':
    app.run()

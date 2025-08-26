from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField, TimeField, URLField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name ', validators=[DataRequired()])
    url = URLField('Location URL ', validators=[DataRequired()])
    open_time = StringField('Opening Time ', validators=[DataRequired()])
    close_time = StringField('Closing Time ', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating ', choices=[('☕'),('☕☕'),('☕☕☕'),('☕☕☕☕'),('☕☕☕☕☕')], validators=[DataRequired()])
    wifi_rating = SelectField('WIFI Rating ', choices=[('✘'),('💪'),('💪💪'),('💪💪💪'),('💪💪💪💪'),('💪💪💪💪💪')], validators=[DataRequired()])
    power_rating = SelectField('Power Rating ', choices=[('✘'),('🔌'),('🔌🔌'),('🔌🔌🔌'),('🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe = form.cafe.data
        url = form.url.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_rating = form.power_rating.data


        new_row = [cafe, url, open_time, close_time, coffee_rating, wifi_rating, power_rating]
        with open('cafe-data.csv', mode='a', encoding='utf-8', newline='') as cafe_data:
            writer = csv.writer(cafe_data)
            writer.writerow(new_row)

        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

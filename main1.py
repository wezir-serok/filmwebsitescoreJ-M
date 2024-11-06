from flask import Flask, render_template, request
import csv
import requests

app = Flask(__name__)

# Replace 'filtered_output.csv' with your CSV file name
csv_file = 'filtered_output.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    movie_title = request.form['movie_title'].strip().lower()
    imdb_ids = []

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            if row[2].strip().lower() == movie_title:
                imdb_ids.append(row[0])

    if imdb_ids:
        url = "https://movies-ratings2.p.rapidapi.com/ratings"
        headers = {
            "x-rapidapi-key": "0c200b2a67msh8bd7b1959ea26aep101309jsn3140216e37e3",
            "x-rapidapi-host": "movies-ratings2.p.rapidapi.com"
        }

        results = []
        for imdb_id in imdb_ids:
            querystring = {"id": imdb_id}
            response = requests.get(url, headers=headers, params=querystring)

            if response.status_code == 200:
                results.append(response.json())
            else:
                results.append({"error": f"Failed to get details for IMDb ID {imdb_id}. Status code: {response.status_code}"})

        return render_template('results.html', movie_title=movie_title.title(), imdb_ids=imdb_ids, results=results)
    else:
        return render_template('index.html', error=f"Movie '{movie_title.title()}' not found in the CSV file.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

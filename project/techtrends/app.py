import sqlite3
import logging
import sys
from datetime import datetime

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
def get_db_connection():
    """This function connects to database with the name database.db."""    

    # In case the same reviewer sees this resubmission-
    # For better or worse, today's libraries will create an empty sqlite database file when this connection is attempted
    # If the running process has the correct permissions, it will come into existence with the connection attempt.
    # I know because I tried to delete the file to create the right conditions in the /healthz endpoints, but it didn't work!
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    app.config['count'] = app.config['count'] + 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

app.config['count'] = 0

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.debug("%s Article %s not found", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), post_id)
      return render_template('404.html'), 404
    else:
      app.logger.debug("%s Article %s retrieved!", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), post['title'])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.debug("%s About Us loaded", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.debug("%s New article created: %s", datetime.now().strftime("%d/%m/%Y %H:%M:%S"), title)
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthcheck():
    try:
        connection = get_db_connection()
        post_count = connection.execute('SELECT count(id) FROM posts')
        row = post_count.fetchone()
        connection.close()
        response = app.response_class(
                response=json.dumps({"result":"OK - healthy"}),
                status=200,
                mimetype='application/json'
        )
        app.logger.debug('Health request successfull')
        return response
    except Exception as inst:
        response = app.response_class(
                response=json.dumps({"result":"ERROR - unhealthy"}),
                status=500,
                mimetype='application/json'
        )
        app.logger.debug('Health request failed')
        return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = connection.execute('SELECT count(id) FROM posts')
    row = post_count.fetchone()
    connection.close()
    response = app.response_class(
            response=json.dumps({"post_count": row[0], "db_connection_count": app.config['count']}),
            status=200,
            mimetype='application/json'
    )
    app.logger.debug('Metrics request successfull')
    return response

# start the application on port 3111
if __name__ == "__main__":
   stdout_handler = logging.StreamHandler(stream=sys.stdout)
   stderr_handler = logging.StreamHandler(stream=sys.stderr)
   logging.basicConfig(encoding='utf-8', level=logging.DEBUG, handlers=[stdout_handler,stderr_handler])
   app.run(host='0.0.0.0', port='3111')

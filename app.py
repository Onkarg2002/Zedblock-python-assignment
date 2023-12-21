from flask import Flask, render_template, request, redirect, url_for
from models import Post, db
from flask import render_template, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    posts = Post.query.all()
    print(posts)
    return render_template('home.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Handle form submission for adding a new post
        title = request.form['title']
        content = request.form['content']

        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

    posts = Post.query.all()
    return render_template('admin.html', posts=posts)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post_to_delete = Post.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('admin'))

# Add admin routes for CRUD operations
# ...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add sample data
        sample_post = Post(title='Sample Post', content='This is a sample blog post.')
        db.session.add(sample_post)
        db.session.commit()

    app.run(debug=True)


from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)


# Helper function to read posts
def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


# Helper function to save posts
def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # 1. Fetch form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # 2. Load existing posts to append to the list
        blog_posts = load_posts()

        # 3. Generate a unique ID (e.g., finding the max ID and adding 1)
        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1
        else:
            new_id = 1

        # 4. Create the new post dictionary and append it
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)

        # 5. Save back to the JSON file
        save_posts(blog_posts)

        # 6. Redirect to home page
        return redirect(url_for('index'))

    # If it's a GET request, display the form
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load the current posts
    blog_posts = load_posts()

    # Find the blog post with the given id and remove it from the list
    for i, post in enumerate(blog_posts):
        if post['id'] == post_id:
            del blog_posts[i]
            break

    # Save the updated list back to the JSON file
    save_posts(blog_posts)

    # Redirect back to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = load_posts()

    # Find the specific post by ID
    post = next((p for p in blog_posts if p['id'] == post_id), None)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        save_posts(blog_posts)

        # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
import sqlite3 as sql



conn = sql.connect("database.db",check_same_thread=False)



cur = conn.cursor()

cur.execute("""
            create table if not exists image(
    id  Integer primary key,
    image_data BLOB nullable)
""")

cur.execute("INSERT INTO image (image_data) values(?)",["bheadfshtgrfdgthggefares"])
conn.commit()





@app.route('/pagi')
def users():
    users = User.query.all()
    print(users)
    results = [users.format() for user in users]
    return jsonify({
    'success':True,
    'results':results,
    'count':len(results)
    })


def paginate(items, page_size= 10, page_number=1):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    return items[start_index:end_index]

# Example usage:
all_users = list(range(1, 101))  # Imagine you have 100 toys numbered 1 to 100
page_size = 10  # You want to see 10 toys per page
page_number = 1  # You want to see the first page

# current_page = paginate(all_users, page_size, page_number)
# print(f"Page {page_number}: {current_page}")


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    lga = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    image = db.relationship('Image', backref='user', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.LargeBinary, nullable=True)


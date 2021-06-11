from flask import render_template
from flask import request
from app import app
import sqlite3
import math


@app.route('/')
@app.route('/index')
def index():
    page = int(request.args.get('page', 1))
    COMMENT_PER_PAGE = 20
    OFFSET = (page -1) * COMMENT_PER_PAGE
    client = sqlite3.connect("database.db")
    cursor = client.execute("SELECT count(*), * from COMMENT")
    NUM_COMMENTS = 0
    for row in cursor:
        NUM_COMMENTS = int(row[0])
        break
    TOTAL_PAGES = math.ceil((NUM_COMMENTS / COMMENT_PER_PAGE))
    invalid_next = [page + i for i in range(1, 5) if page +i <= TOTAL_PAGES]
    meta_infor = {
        'has_next': (page + 1) <= TOTAL_PAGES,
        'has_prev': (page - 1) > 0,
        'current_page': page,
        'invalid_prev': sorted([page - i for i in range(1, 5) if page -i > 0]),
        'invalid_next': invalid_next,
        'last_page': TOTAL_PAGES if (TOTAL_PAGES not in invalid_next and page < TOTAL_PAGES) else None

    }


    with open("meta.info", "r") as f:
        lines = f.readlines()[0]
        topic_title, topic_author, topic_time = lines.split("###")
        meta_infor['topic_title'] = topic_title
        meta_infor['topic_author'] = topic_author
        meta_infor['topic_time'] = topic_time

    cursor = client.execute("SELECT id, content from COMMENT ORDER BY id LIMIT {} OFFSET {}".format(COMMENT_PER_PAGE, OFFSET))
    comments = []
    for row in cursor:
        comments.append({'comment_id': row[0], 'comment_content': row[1]})
    return render_template('index.html', comments=comments, meta=meta_infor)

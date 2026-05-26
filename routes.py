from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from model import UserModel, CategoryMaster, BlogComment, BlogModel, db, login
from sqlalchemy import func
import os
from dotenv import load_dotenv

global_all_category_no = None
global_all_category_name = None

load_dotenv()
app = Flask(__name__)

app.secret_key=os.getenv('SECRET_KEY')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogDB.db"

app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db.init_app(app)
login.init_app(app)
login.login_view = "login"


def get_categories():
    global global_all_category_no, global_all_category_name
    all_category_info = db.session.query(
        CategoryMaster.category_id, CategoryMaster.category_name
    )
    all_category_info = list(all_category_info)
    global_all_category_no, global_all_category_name = zip(*all_category_info)


with app.app_context():
    db.create_all()
    # call the function
    get_categories()


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if current_user.is_authenticated:
            return redirect("/")  ##
        if request.method == "POST":
            email = request.form.get("email")
            username = request.form.get("username")
            password = request.form.get("password")
            if UserModel.query.filter_by(email=email).first():
                flash("this email is already exists", "error")
                return redirect(url_for('register'))
                # return "this email is already exists"

            user = UserModel(email=email, username=username)
            # send password for hashing
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Register Successfull", "success")
            return redirect("/login")
    except:
        db.session.rollback()
    return render_template("register.html")



# LOGIN
# get data
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if current_user.is_authenticated:
            return redirect("/")  ##
        if request.method == "POST":
            email = request.form.get("email")
            user = UserModel.query.filter_by(email=email).first()
            if user is not None and user.check_password(request.form.get("password")):
                login_user(user)
                flash("Login Successfully", "success")
                return redirect("/")
            flash("User Not Registered", "error")
            return render_template("register.html")
        # return render_template("login.html")
    except Exception as e:
        db.session.rollback()
    return render_template("login.html")
    


# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("User Logged Out", "success")
    return redirect("/register")


# BLOGS
@app.route("/")
def blogs():
    if current_user.is_authenticated:
        return render_template("blogs_home.html")
    return redirect("view_all_blogs")


@app.route("/create_blog", methods=["GET", "POST"])
@login_required
def create_blog():
    try:
        if request.method == "POST":
            category_id = request.form.get("category_id")
            blog_text = request.form.get("blog_text")
            if not blog_text:
                db.session.rollback()
                flash("Blog Cannot create", "warning")
                return redirect("/")
            today = datetime.now()
            blog_userid = current_user.id
            blog_readcount = 0
            blog_ratecount = 0
            newBlog = BlogModel(
                category_id=category_id,
                blog_user_id=blog_userid,
                blog_cont=blog_text,
                blog_date=today,
                blog_readcount=blog_readcount,
                blog_ratecount=blog_ratecount,
            )
            db.session.add(newBlog)
            db.session.commit()
            flash("Blog Created successfully", "success")
            return redirect("/")
    except Exception as e:
        db.session.rollback()
        flash("Couldnt create the blog","error")
    return render_template(
            "create_blog.html",
            all_category_id=global_all_category_no,
            all_category_name=global_all_category_name,
        )


# VIEW BLOGS of only current users own written
@app.route("/view_blog")
@login_required
def view_blog():
    all_self_blog = BlogModel.query.filter(BlogModel.blog_user_id == current_user.id)
    return render_template(
        "view_blog.html",
        all_self_blog=all_self_blog,
        all_categories=global_all_category_name,
    )


# UPDATE AND DELETE
@app.route(
    "/self_blog_detail/<int:blog_model_id>/<string:blog_model_category>",
    methods=["POST", "GET"],
)
@login_required
def self_blog_detail(blog_model_id, blog_model_category):
    try:
        blog = BlogModel.query.get(blog_model_id)
        # check if user come with post
        if request.method == "POST":
            if request.form["action"] == "Update":
                blog.blog_cont = request.form.get("blog_cont")
                msg = "Blog Updated Successfully"
            else:
                BlogModel.query.filter_by(id=blog_model_id).delete()
                msg = "Blog Deleted Successfully"
            db.session.commit()
            flash(msg,"success")
            return redirect("/view_blog")
    except Exception as e:
        db.session.rollback()
    return render_template(
        "self_blog_detail.html",
        blog_id=blog_model_id,
        blog_categories=blog_model_category,
        blog_cont=blog.blog_cont,
    )


# VIEW ALL BLOGS users avalible on this website
@app.route("/view_all_blogs")
def view_all_blogs():
    all_blogs = BlogModel.query.all()
    all_users = UserModel.query.all()
    return render_template(
        "view_all_blogs.html",
        all_blogs=all_blogs,
        all_users=all_users,
        all_category=global_all_category_name,
    )


@app.route(
    "/blog_detail/<int:blog_id>/<string:username>/<string:category>",
    methods=["GET", "POST"],
)
def blog_detail(blog_id, username, category):
    # fetch the blog id from blogModel
    blog = BlogModel.query.get(blog_id)
    if request.method == "GET":
        if current_user.id != blog.blog_user_id:
            blog.blog_readcount += 1
            db.session.commit()
        rating = (
            db.session.query(func.avg(BlogComment.blog_rate))
            .filter(BlogComment.blog_id == int(blog_id))
            .first()[0]
        )
        return render_template(
            "/blog_detail.html",
            blog=blog,
            rating=rating,
            author=username,
            category=category,
        )
    else:
        rate = request.form.get("rating")
        comment = request.form.get("comment")
        blog_id = request.form.get("blog_id")
        old_comment = (
            BlogComment.query.filter(BlogComment.blog_id == blog_id)
            .filter(BlogComment.commnet_userid == current_user.id)
            .first()
        )
        today = datetime.now()
        if old_comment == None:
            blog.blog_ratecount += 1
            # and create new comment
            new_comment = BlogComment(
                blog_id=blog_id,
                commnet_userid=current_user.id,
                blog_comment=comment,
                blog_rate=rate,
                blog_comment_date=today,
            )
            db.session.add(new_comment)
        else:
            old_comment.blog_comment = comment
            old_comment.blog_rate = rate
        db.session.commit()
        return redirect("/")


# CATEGORY
@app.route("/category")
@login_required
def category():
    return render_template("category.html")

@app.route("/add_category", methods=["POST", "GET"])
def add_category():
    try:
        category_name = request.form.get("category_name").capitalize().strip()
        if not category_name:
            db.session.rollback()
            return redirect("/add_category")
        if CategoryMaster.query.filter_by(category_name=category_name).first():
            flash("This Category is alredy exists", "warning")
            return redirect(url_for('category'))
        data = CategoryMaster(category_name=category_name)
        db.session.add(data)
        db.session.commit()
        flash("category Created successfully","success")
        # return redirect("add_category")
    except Exception as e:
        db.session.rollback()
        flash("The Category Couldn't added", "error")
    return redirect(url_for('category'))


@app.route("/view_category")
def view_category():
    all_data = CategoryMaster.query.all()
    return render_template("view_category.html", all_data=all_data)


if __name__ == "__main__":
    app.run(port=5001)

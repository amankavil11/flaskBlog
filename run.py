from flaskBlog import create_app

app = create_app()

if __name__ == "__main__":
    #default port 5000 on MACOSX in use for airplay
    app.run(debug=True, port=8001)

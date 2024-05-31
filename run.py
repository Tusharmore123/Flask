from flask_blog import app

if __name__=="__main__":
    
    app.debug=True#explicitly setting flask in debug mode
    # we can set the debug mode implicitly by setting the environment variable
    app.run()
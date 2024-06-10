from flask_blog import create_app
app=create_app()
if __name__=="__main__":
    
    #explicitly setting flask in debug mode
    # we can set the debug mode implicitly by setting the environment variable
    app.run(debug=True)
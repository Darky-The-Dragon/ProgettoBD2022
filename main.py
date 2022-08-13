from website import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
    #  automatically reruns the server when we rewrite the code

from resurety_homework.app import add_resources, app

if __name__ == "__main__":
    add_resources()
    app.run(host='0.0.0.0', port=5001, debug=True)
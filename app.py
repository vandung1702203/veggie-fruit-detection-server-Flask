from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import model_predict
import os
from werkzeug.utils import secure_filename

file_path = ""


def create_app():
    app = Flask(__name__)
    class_names = model_predict.GetClassNames()
    UPLOAD_FOLDER = 'static/uploads/'
    app.secret_key = "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/get_img', methods=['POST'])
    def upload_image():
        if 'file' not in request.files:
            flash('No file path')
            return jsonify({
                'error': "Not file"
            })
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'error': "No image selected for uploading"
            })
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            label = model_predict.vegetable_predict(class_names, file)
            os.remove(file_path)
            vegetable = {
                'name': label
            }
            return jsonify(vegetable)
        else:
            
            return jsonify({
                'error': "Allowed image types are - png, jpg, jpeg, gif"
            })
    # @app.route('/upload')
    # def get_img():

    @app.route('/display/<filename>')
    def display_image(filename):
        return redirect(url_for('static', filename='uploads/' + filename), code=301)

    @app.route('/show_pic')
    def show_images():
        image_names = os.listdir('./static/uploads')
        return render_template("gallery.html", image_names=image_names)

    return app
# if __name__ == "__main__":
#     app.run(debug=True)

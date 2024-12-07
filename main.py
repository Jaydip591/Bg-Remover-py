from flask import Flask,render_template, url_for, request,flash
import os
from werkzeug.utils import secure_filename
import cv2 as cv
from PIL import Image
from rembg import remove
app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.secret_key = os.urandom(24) 
         
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html",title= 'Home')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/edit' , methods=["GET", "POST"])
def edit():
    
    if request.method == 'POST':
            operation = request.form.get('operation')
            if 'file' not in request.files:
                flash('No file selected')
                return render_template('home.html')

            file = request.files['file']

            if  operation== 'Select':
                flash('select a choice first')
                return render_template('home.html')
            if file.filename == '':
                
                flash('select a file First ')
                return render_template('home.html')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                out_image=process_image(filename,operation)
                flash(f"Uploaded successfully")
                return render_template('home.html',final_image=out_image)

            else:
                flash('File type is not allowed')
                return "File type error"
    return render_template('home.html', )
def process_image(filename, operation):
    print(f'The {filename} and the op is {operation}')
    img=cv.imread(f"static/uploads/{filename}")
    match operation:
        case "ctogray":
            gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            out_image=f'static/processed/{filename}'
            cv.imwrite(out_image, gray_image)    
            return out_image
        case "ctopng":
             new_string = filename[:-4] 
             out_image=f'static/processed/{new_string}.png'
             cv.imwrite(out_image,img)
             return out_image
        case "ctopdf":
            new_string = filename[:-4] 
           
            img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img_rgb)
            out_image=f'static/processed/{new_string}.pdf'
            
            pil_image.save(out_image, 'PDF')
            return out_image
        case "removebg":
            rimage = remove(img)
            out_image=f'static/processed/{filename}'
            
            cv.imwrite(out_image,rimage)
            
            # cv.imshow(out_image)
            return out_image
@app.route('/about')
def about():
    return render_template('about.html', title= 'About')
if __name__ == '__main__':
    app.run(debug=True)

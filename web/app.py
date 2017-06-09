from flask import Flask, render_template, request, make_response
from jinja2 import Template
from translate import Translator
app = Flask(__name__)

t = Translator()

ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/idkr", methods=['GET', 'POST'])
def idkr():
	target = ""
	source = ""
	romanize = ""
	other = ""
	translations = ""
	if request.method == 'POST':
		source = request.form['source']
		preSource = t.preprocessID(source.encode("utf-8"))
		target = t.translateIDKR(preSource.encode("utf-8")).replace("%","")
		# other = "Other Translations:"
		# translations = "hahahaha"
		romanize = t.romanizeHangul(target.encode("utf-8"))
		# print t.translateIDKR(source)
	language = ["ID - KR", "KR - ID"]
	links = ["idkr", "krid"]

	# method = ["Baseline", "POS Tag", "Additional", "Additional POS Tag"]
	return render_template('idkr.html', lang = language, link = links, source = source, target = target, romanize=romanize, other = other, translations = translations)

@app.route('/krid', methods=['GET', 'POST'])
def krid():
	target = ""
	source = ""
	if request.method == 'POST':
		source = request.form['source']
		preSource = t.preprocessKR(source.encode("utf-8"))
		# other = "Other Translations:"
		# translations = "hahahaha"
		# print t.translateKRID(source.encode("utf-8"))
		target = t.translateKRID(preSource.encode("utf-8")).replace("%","")
		
	language = ["ID - KR", "KR - ID"]
	links = ["idkr", "krid"]

	# method = ["Baseline", "POS Tag", "Additional", "Additional POS Tag"]
	return render_template('krid.html', lang = language, link = links, source = source,  target = target, other = other, translations = translations)

@app.route('/document', methods=['GET', 'POST'])
def doc():
	target = ""
	source = ""
	if request.method == 'POST':
		trans = request.form['lang']
		source = request.files['file']
		
		result = ""
		lines = source.readlines()
		for line in lines:
			if trans == "idkr":
				preSource = t.preprocessID(line.decode("utf-8"))
				print preSource
				print t.translateIDKR(preSource.encode("utf-8")) + "\n"
				result += t.translateIDKR(preSource.encode("utf-8")) + "\n"

			else:
				preSource = t.preprocessKR(line)
				result += t.translateKRID(preSource.encode("utf-8")) + "\n"


		response = make_response(result)
		response.headers["Content-Disposition"] = "attachment; filename=translation.txt"
		return response
		# target = t.translateKRID(source.encode("utf-8"))
		# print t.translateKRID(source.encode("utf-8")).decode("utf-8")
	language = ["ID - KR", "KR - ID"]
	links = ["idkr", "krid"]

	# method = ["Baseline", "POS Tag", "Additional", "Additional POS Tag"]
	return render_template('doc.html', lang = language, link = links, source = source,  target = target)

if __name__ == "__main__":
    app.run()
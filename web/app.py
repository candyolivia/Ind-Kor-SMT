from flask import Flask, render_template, request, make_response
from jinja2 import Template
from translate import Translator
from additionalProcess import Additional

app = Flask(__name__)

t = Translator()
a = Additional()

ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/idkr", methods=['GET', 'POST'])
def idkr():
	target = ""
	source = ""
	romanize = ""
	if request.method == 'POST':
		source = request.form['source']
		if source != "":
			preSource = t.preprocessID(source.encode("utf-8"))
			reorder = a.reorderIndonesia(preSource.encode("utf-8"))
			try:
				trans = a.translateReorderedIDKR(preSource.encode("utf-8"),reorder).replace("  ", "").replace("%","")
			except Exception, e:
				trans = a.translateReorderedIDKR(preSource.encode("utf-8"),reorder).replace("  ", "").decode("utf-8").replace("%","")
			target = a.transIndNE(a.postTranslate(0,trans)).replace("! ! !","!")
			romanize = t.romanizeHangul(target.encode("utf-8"))
	language = ["ID - KR", "KR - ID"]
	links = ["idkr", "krid"]
	return render_template('idkr.html', lang = language, link = links, source = source, target = target, romanize=romanize)

@app.route('/krid', methods=['GET', 'POST'])
def krid():
	target = ""
	source = ""
	if request.method == 'POST':
		source = request.form['source']
		if source != "":
			preSource = t.preprocessKR(source.encode("utf-8"))
			reorder = a.reorderKorea(preSource.encode("utf-8"))
			try:
				trans = a.translateReorderedKRID(preSource.encode("utf-8"),reorder).replace("  ", "").replace("%","")
			except Exception, e:
				trans = a.translateReorderedKRID(preSource.encode("utf-8"),reorder).replace("  ", "").decode("utf-8").replace("%","")
			target = a.transKorNE(a.postTranslate(1,trans))

	language = ["ID - KR", "KR - ID"]
	links = ["idkr", "krid"]
	return render_template('krid.html', lang = language, link = links, source = source,  target = target)

@app.route('/document', methods=['GET', 'POST'])
def doc():
	target = ""
	source = ""
	if request.method == 'POST':
		trans = request.form['lang']
		source = request.files['file']

		result = ""
		lines = source.readlines()
		if trans == "idkr":
			for line in lines:
				preSource = t.preprocessID(line.decode("utf-8"))
				reorder = a.reorderIndonesia(preSource.encode("utf-8"))
				try:
					trans = a.translateReorderedIDKR(preSource.encode("utf-8"),reorder).replace("  ", "").replace("%","")
				except Exception, e:
					trans = a.translateReorderedIDKR(preSource.encode("utf-8"),reorder).replace("  ", "").decode("utf-8").replace("%","")
				target = a.postTranslate(0,trans)
				result += target + "\n"

		elif trans == "krid":
			for line in lines:
				preSource = t.preprocessKR(line)
				reorder = a.reorderKorea(preSource.encode("utf-8"))
				try:
					trans = a.translateReorderedKRID(preSource.encode("utf-8"),reorder).replace("  ", "").replace("%","")
				except Exception, e:
					trans = a.translateReorderedKRID(preSource.encode("utf-8"),reorder).replace("  ", "").decode("utf-8").replace("%","")
				target = a.transKorNE(a.postTranslate(1,trans))
				result += target + "\n"
		response = make_response(result)
		response.headers["Content-Disposition"] = "attachment; filename=translation.txt"
		return response
	language = ["ID - KR", "KR - ID"]
	links = ["idkr", "krid"]
	return render_template('doc.html', lang = language, link = links)

if __name__ == "__main__":
    app.run()
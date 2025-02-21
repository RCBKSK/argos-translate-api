from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

app = Flask(__name__)

# Download and install translation models (only needed once)
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == "en" and x.to_code == "es", available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

@app.route('/')
def home():
    return "Argos Translate API is running!"

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('q')
    source = data.get('source')
    target = data.get('target')
    translated_text = argostranslate.translate.translate(text, source, target)
    return jsonify({"translatedText": translated_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

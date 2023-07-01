import re

import argostranslate.package
import argostranslate.translate
import translatehtml


class Translator:
    def __init__(self, from_code="en", to_code="ru"):
        print('Downloading and installing Argos Translate package')
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        available_package = list(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )[0]
        download_path = available_package.download()
        argostranslate.package.install_from_path(download_path)

        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = list(filter(lambda x: x.code == from_code, installed_languages))[0]
        to_lang = list(filter(lambda x: x.code == to_code, installed_languages))[0]
        self.translation = from_lang.get_translation(to_lang)

    def translate(self, text):
        html = self.text2html(text=text)
        translated_soap = translatehtml.translate_html(self.translation, html)
        return str(translated_soap), html

    def text2html(self, text,
                  pattern=r'("?”?.+?)(\.\.\.?|\.\)?|!\.?\.?|\?\.?\.?|\n\n)',
                  replacepattern=r'<p>\1\2</p>'):
        text1 = text[:].replace('"', ' ')
        text1 = text1.replace('”', ' ')
        result = re.sub(pattern, replacepattern, text1,
                        flags=re.DOTALL | re.UNICODE)
        # r'("?”?.+?)(\.\.\.|\.\)?|!\.?\.?|\?\.?\.?|\n\n?|,|;)'
        # r'("?”?.*?)(\n\n)'
        return f"<html>{result}</html>"

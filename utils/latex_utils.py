def escape_latex(text):
    replacements = {
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def build_resume(template, hiring):
    return template.replace("__TOHIRINGMANAGER__", hiring)
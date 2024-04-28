from config import DefaultConfig


def allowed_file(filename: str):
    if "." not in filename:
        return False

    [_, file_extension] = filename.split(".")
    return file_extension.lower() in DefaultConfig.ALLOWED_EXTENSIONS

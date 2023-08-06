# main.py
# deploy this for everyone and other apps!
import fifteenrock
import client_file


def main(context, event):
    return context.Response(body=client_file._main(event),
                            headers={},
                            content_type='text/json',
                            status_code=200)

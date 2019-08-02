import dash
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, Response
import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        success, image = self.video.read()
        # ret, jpeg = cv2.imencode('.jpg', image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Video', image)
        # return jpeg.tobytes()



def gen(camera):
    while True:
        frame = camera.get_frame()
        # cv2.imshow('Video', frame)

        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

@server.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


app.layout = html.Div([
    html.H1("Webcam Test"),
    # html.Img(src="/video_feed")
    html.Video(src="/video_feed")
])

if __name__ == '__main__':
    app.run_server(debug=True)
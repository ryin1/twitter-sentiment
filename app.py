from flask import Flask, render_template, request, redirect, url_for, json
import time
import bs4
import requests

# Create app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        # render homepage template
        return render_template('boot.html')
    else:
        # grab POST form data
        data = request.form

        # parse as json
        jsondata = json.dumps(data, separators=(',', ':'))
        if 'topic' in jsondata:
            stream_time = float(data['time'][0])
            start = time.time()
            while time.time() - start < stream_time:
                # analysis here
                #
                #
                #
                #
                #
                pass
            analysis_data = [1, 2, 6, 7, 27]
            new_data = json.loads(jsondata)
            new_data['data'] = analysis_data
            jsondata = json.dumps(new_data, separators=(',', ':'))
            return redirect((url_for('log', data=jsondata, mode='debug')))
        elif 'username' in jsondata:
            # analysis here
            #
            #
            #
            #
            #
            return redirect((url_for('log', data=jsondata, mode='debug')))


@app.route('/log/<data>/<mode>')
def log(data, mode):
    jsondata = json.loads(data)
    if 'username' in jsondata:
        username = jsondata['username'][0]
        req = requests.get('https://twitter.com/' + username)
        response_text = req.text
        bs = bs4.BeautifulSoup(response_text)
        profile_image_url = bs.find_all(class_='ProfileAvatar-container u-block js-tooltip profile-picture media-thumbnail', href=True)[0]['href']
        # render homepage template
        return render_template('success.html', username=username, profile_image_url=profile_image_url)
    elif 'topic' in jsondata:
        topic = jsondata['topic'][0]
        # render homepage template
        return render_template('stream.html', topic=topic, data=jsondata['data'])
    else:
        # render homepage template
        return render_template('boot.html')


def main():
    global poop
    global analysis_data
    poop = False
    analysis_data = dict()
    app.debug = True
    app.run()


if __name__ == "__main__":
    main()

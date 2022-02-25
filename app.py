import time
from flask import Flask, request, jsonify
from agora_token_builder import RtcTokenBuilder

app = Flask(__name__)

appId = '{agora_app_id}'
appCertificate = '{agora_app_certificate}'

active_channels = {}


@app.route('/token', methods=['GET'])
def get_token():
    channel_name = request.args['channel']
    uid = request.args['uid']
    if channel_name in active_channels.keys():
        if uid in active_channels[channel_name]:
            return jsonify({'error': 'already registered'})
        role = 2
        active_channels[channel_name].append(uid)
    else:
        active_channels[channel_name] = [uid]
        role = 1
    privilegeExpiredTs = time.time() + 1
    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channel_name, uid, role, privilegeExpiredTs)
    return jsonify({'token': token})


@app.route('/channels', methods=['GET'])
def channel():
    return active_channels


@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    channel_name = request.args['channel']
    uid = request.args['uid']
    if channel_name in active_channels.keys():
        if uid in active_channels[channel_name]:
            active_channels[channel_name].remove(uid)
            if active_channels[channel_name] == []:
                active_channels.pop(channel_name)
            return jsonify({'sucess': 'user removed'})
    return jsonify({'error': 'user not subscribed'})


if __name__ == '__main__':
    app.run(debug=True)

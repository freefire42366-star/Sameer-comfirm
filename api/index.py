from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Credits: sameerpar
@app.route('/api/send-otp', methods=['GET'])
def send_otp():
    token = request.args.get('access_token')
    email = request.args.get('email')
    headers = {"User-Agent": "GarenaMSDK/4.0.35", "Content-Type": "application/x-www-form-urlencoded"}
    payload = {"email": email, "access_token": token, "app_id": "100067", "region": "BD", "locale": "en_PK"}
    r = requests.post("https://100067.connect.garena.com/game/account_security/bind:send_otp", data=payload, headers=headers)
    return jsonify(r.json())

@app.route('/api/bind', methods=['GET'])
def bind_confirm():
    token = request.args.get('access_token')
    email = request.args.get('email')
    otp = request.args.get('otp')
    password = "SameerPar123@" # Default Security Pass
    
    headers = {"User-Agent": "GarenaMSDK/4.0.35", "Content-Type": "application/x-www-form-urlencoded", "X-GA-SDK-VERSION": "4.0.35"}
    
    # Auto-Identity Bypass (Critical for FB)
    id_res = requests.post("https://100067.connect.garena.com/game/account_security/bind:verify_identity", data={"access_token": token, "app_id": "100067", "region": "BD"}, headers=headers).json()
    id_token = id_res.get("identity_token", "")

    # Verifier Token check
    v_res = requests.post("https://100067.connect.garena.com/game/account_security/bind:verify_otp", data={"email": email, "otp": otp, "access_token": token, "region": "BD"}, headers=headers).json()
    v_token = v_res.get("verifier_token")

    if not v_token: return jsonify({"success": False, "msg": "OTP Wrong", "raw": v_res})

    # Final Binding Protocol
    final_payload = {
        "email": email, "password": password, "app_id": "100067", "access_token": token,
        "verifier_token": v_token, "identity_token": id_token, "region": "BD",
        "locale": "en_PK", "bind_type": "1", "reg_source": "facebook", "grant_type": "bind"
    }
    rf = requests.post("https://100067.connect.garena.com/game/account_security/bind:create_bind_request", data=final_payload, headers=headers)
    return jsonify(rf.json())

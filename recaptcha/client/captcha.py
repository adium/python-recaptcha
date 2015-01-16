import urllib2, urllib, json

API_SSL_SERVER="https://www.google.com/recaptcha/api"
API_SERVER="http://www.google.com/recaptcha/api"
VERIFY_SERVER="www.google.com"

class RecaptchaResponse(object):
    def __init__(self, is_valid, error_code=None):
        self.is_valid = is_valid
        self.error_code = error_code

def displayhtml (public_key,
                 use_ssl = False,
                 error = None):
    """Gets the HTML to display for reCAPTCHA

    public_key -- The public api key
    use_ssl -- Should the request be sent over ssl?
    error -- An error message to display (from RecaptchaResponse.error_code)"""

    error_param = ''
    if error:
        error_param = '&error=%s' % error

    if use_ssl:
        server = API_SSL_SERVER
    else:
        server = API_SERVER

    return """<script src="https://www.google.com/recaptcha/api.js" async defer></script>
              <div class="g-recaptcha" data-sitekey="%(PublicKey)s"></div>
              <noscript>
                  <div style="width: 302px; height: 352px;">
                    <div style="width: 302px; height: 352px; position: relative;">
                      <div style="width: 302px; height: 352px; position: absolute;">
                        <iframe src="https://www.google.com/recaptcha/api/fallback?k=%(PublicKey)s"
                                frameborder="0" scrolling="no"
                                style="width: 302px; height:352px; border-style: none;">
                        </iframe>
                      </div>
                      <div style="width: 250px; height: 80px; position: absolute; border-style: none;
                                  bottom: 21px; left: 25px; margin: 0px; padding: 0px; right: 25px;">
                        <textarea id="g-recaptcha-response" name="g-recaptcha-response"
                                  class="g-recaptcha-response"
                                  style="width: 250px; height: 80px; border: 1px solid #c1c1c1;
                                         margin: 0px; padding: 0px; resize: none;" value="">
                        </textarea>
                      </div>
                    </div>
                  </div>
                </noscript>""" % {
        'PublicKey' : public_key,
        }


def submit (recaptcha_response_field,
            private_key,
            remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request
    
    recaptcha_response_field -- The value of recaptcha_response_field from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """

    if not (recaptcha_response_field and len (recaptcha_response_field)):
        return RecaptchaResponse (is_valid = False, error_code = 'incorrect-captcha-sol')
    

    def encode_if_necessary(s):
        if isinstance(s, unicode):
            return s.encode('utf-8')
        return s

    params = {
      'secret': private_key,
      'response': recaptcha_response_field,
      'remoteip': remoteip
    }

    request = urllib2.Request (
        url = "https://%s/recaptcha/api/siteverify?%s" % (VERIFY_SERVER, urllib.urlencode(params)),
        headers = {
            "User-agent": "reCAPTCHA Python"
            }
        )
    
    httpresp = urllib2.urlopen (request)

    return_values = json.load(httpresp)
    httpresp.close();

    return_code = return_values ["success"]

    if (return_code == True):
        return RecaptchaResponse (is_valid=True)
    else:
        return RecaptchaResponse (is_valid=False, error_code = return_values ["error-codes"])

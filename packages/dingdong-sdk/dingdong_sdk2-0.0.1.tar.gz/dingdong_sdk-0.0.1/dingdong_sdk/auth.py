import requests
import requests.adapters
import urllib3.util

_CAS_URL = 'https://cas.apiit.edu.my'
_CAS_VALIDATE_URL = _CAS_URL + '/'
_DINGDONG_SERVICE_URL = 'https://dingdong.apu.edu.my/'

_tgt = None
_cas_session = None


def _requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504, 401),
                            session=requests.Session()):
    retry = urllib3.util.Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def _get_cas_session():
    global _cas_session
    if _cas_session is None:
        _cas_session = _requests_retry_session()
    return _cas_session


def _generate_tgt(username, password):
    resp = _get_cas_session().post(
        _CAS_URL + '/cas/v1/tickets',
        data={
            'username': username,
            'password': password
        }
    )

    assert resp.status_code == 201, 'Invalid Credentials'

    return resp.headers['Location']


def _generate_st(username, password):
    global _tgt

    if _tgt is None:
        _tgt = _generate_tgt(username, password)

    resp = _get_cas_session().post(
        _tgt,
        data={
            'service': _DINGDONG_SERVICE_URL
        }
    )

    if resp.status_code == 404:
        _tgt = _generate_tgt(username, password)

        resp = _get_cas_session().post(
            _tgt,
            data={
                'service': _DINGDONG_SERVICE_URL
            }
        )

    return resp.text


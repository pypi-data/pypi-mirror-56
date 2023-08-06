"""
The DingDong SDK helps make your life (and mine) easier by providing
a set of easy to use functions to interact with the backend.
"""
import requests
import requests.adapters
import urllib3.util
import typing
from dingdong_sdk import auth

__version__ = '0.0.3'
_dingdong_url = {
    'staging': 'https://t1s1s6hl4g.execute-api.ap-southeast-1.amazonaws.com/staging/dingdong',
    'prod': 'https://api.apiit.edu.my/dingdong'
}

_dingdong_session = None


def _requests_retry_session(retries=0, backoff_factor=0.3, status_forcelist=(500, 502, 504, 401),
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


def _get_dingdong_session():
    global _dingdong_session
    if _dingdong_session is None:
        _dingdong_session = _requests_retry_session()
    return _dingdong_session


class DingDong:
    """
    Main class of DingDong.
    """
    username: str
    password: str
    stage: str

    def __init__(self, username: str, password: str, stage: str = 'prod') -> None:
        """
        This is where your authorised CAS credentials goes to.
        You may also use the staging endpoint by specifying `stage` to `staging`.
        >>> dingdong = DingDong(username='thebestusername', password='verysecurepassword')
        """
        self.username = username
        self.password = password
        self.stage = stage

    def send_message(
            self,
            title: str,
            delivery_methods: typing.Sequence[str],
            non_html_content: str,
            html_content: str,
            display_name: str,
            category_name: str,
            subcategory_name: str,
            targets: typing.Sequence[str],
            display_email: typing.Optional[str] = False,
            send_to_personal_email: typing.Optional[bool] = False,
    ):
        """
        Send a message

        :param title: String. Title of the message
        :param delivery_methods: List. A list containing the delivery methods. For example, ['email', 'push']
        :param non_html_content: String. The non html content for push notification and old email clients
        :param html_content: String. The main content for the message
        :param display_name: String. Also known as sender name
        :param category_name: String. This is used for preferences in APSpace.
        :param subcategory_name: String. This is used for preferences in APSpace.
        :param targets: List. A list of targets. For example, ["TP123456", "UC1F1904CS(DA)"]
        :param display_email: String. Only specify when you are sending an email.
        :param send_to_personal_email: Boolean. Only specify when you are sending an email. By default it is false.

        >>> dingdong = DingDong(username='thebestusername', password='verysecurepassword')
        >>> dingdong.send_message(
        >>>     targets=['TP123456'],
        >>>     title='This is a test message',
        >>>     delivery_methods=['push', 'email'],
        >>>     non_html_content='This is a test',
        >>>     html_content='This is a test. Please ignore this message.',
        >>>     display_name='TestDisplay',
        >>>     category_name='TestCategory',
        >>>     subcategory_name='TestSubcategory',
        >>>     display_email='testemail@apu.edu.my',
        >>>     send_to_personal_email=True
        >>> )
        """
        assert not isinstance(delivery_methods, str), 'type should not be str'
        assert not isinstance(targets, str), 'targets should not be str'
        assert set(delivery_methods) <= {'email', 'push', 'sms'}, 'Only email, push, sms type is supported'
        assert self.stage in {'staging', 'prod'}, \
            'Stage specified is invalid. Only staging or prod is supported.'

        if 'email' not in delivery_methods:
            assert not send_to_personal_email, 'send_to_personal_email only supported when sending email'
            assert not display_email, 'display_email only supported when sending email'

        if self.stage == 'staging':
            print('[DingDong] You are now using staging resources.'
                  ' This is only for testing purposes. Please never ever do this in a production environment. :)')

        dingdong_session = _get_dingdong_session()
        dingdong_url = _dingdong_url[self.stage] + '/staff/new'

        payload = {
            'title': title,
            'non_html_content': non_html_content,
            'html_content': html_content,
            'type': delivery_methods,
            'category': category_name,
            'subcategory': subcategory_name,
            'display_name': display_name,
            'to': targets
        }

        if 'email' in delivery_methods:
            payload['display_email'] = display_email
            payload['send_to_personal_email'] = send_to_personal_email

        st = auth._generate_st(username=self.username, password=self.password)

        resp = dingdong_session.post(
            dingdong_url,
            params={
                'ticket': st
            },
            json=payload,
            timeout=10
        )

        assert resp.status_code == 201, f'Something went wrong. Response: {resp.json()}'

        return resp.json()

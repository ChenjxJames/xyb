def dx_identify_code(tel, code):
    # 短信应用SDK AppID
    appid = 0  # SDK AppID是1400开头

    # 短信应用SDK AppKey
    appkey = ""

    # 需要发送短信的手机号码
    phone_numbers = [str(tel)]

    # 短信模板ID，需要在短信应用中申请
    template_id = 311413  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
    # templateId 7839 对应的内容是"您的验证码是: {1}"
    # 签名
    sms_sign = "东聿隹"

    from qcloudsms_py import SmsSingleSender
    from qcloudsms_py.httpclient import HTTPError

    ssender = SmsSingleSender(appid, appkey)
    params = [code]  # 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
    result = {}
    try:
        result = ssender.send_with_param(86, phone_numbers[0],
                                         template_id, params, sign=sms_sign, extend="",
                                         ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)

    bool_result = False
    if result['result'] == 0:
        bool_result = True

    return bool_result


if __name__ == '__main__':
    print(dx_identify_code("18816551820", "99999"))
